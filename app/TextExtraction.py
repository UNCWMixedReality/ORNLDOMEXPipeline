# NOTE: Ensure you're using logging where it would be useful. The Log level is
# declared in __main__, but stick to [info] for high level things "Extracted x amount of files"
# and [debug] for things that will be helpful when stuff breaks, like all FileNotFound errors
import os
import glob
import hashlib
import json
import re
import shutil
from typing import Dict
import textract
from zipfile import ZipInfo
from zipfile import ZipFile as zp
from shutil import rmtree

# Module Level Vars
MAX_ZIP_SIZE = 4 * 1000 * 1000


class TextExtractor(object):
    def __init__(self):
        self.methods = {
            ".txt": self._extract_text_from_txt_file,
            (".docx", ".doc"): self._extract_text_from_word_file,
            ".pdf": self._extract_text_from_pdf_file,
        }
        self.extensions = [".txt", ".docx", ".doc", ".pdf"]
        for extension in self.methods:
            if isinstance(extension, str):
                self.extensions.append(extension)
            else:
                for ext in extension:
                    self.extensions.append(ext)

    # Public methods
    def extract_text_from_single_file(self, file_path: str) -> str:
        """
        Given: A file path
        Return: A String containing all extracted text
        Steps:
            1. Test to ensure path is valid
            2. Determine which file type has been received
            3. If the file type is supported, pass to appropriate method
            4. Return Results
        """

        results = None
        if os.path.exists(file_path):
            for extension, func in self.methods.items():
                if isinstance(extension, str):
                    if file_path.endswith(extension):
                        results = func(file_path)
                        break
                else:
                    found = False
                    for ext in extension:
                        if file_path.endswith(ext):
                            results = func(file_path)
                            found = True
                            break
                    if found:
                        break
            else:
                raise ValueError(
                    f"Unsupported extension. Supported file types are: {self.extensions}"
                )
        else:
            raise FileNotFoundError(file_path)
        return results.strip()

    def extract_text_from_all_files_in_directory(
        self, parent_directory: str, depth: int
    ) -> dict:
        """
        Given: A parent directory and 1-indexed depth
        Return: A dictionary of results, with the key being the path and value
                being a string of all text in the file

        Notes:
            - Feel free to switch between 0 or 1 indexed, just ensure that
              exceptions are properly handled (passing 0 to 1 indexed function)
            - Would recommend the builtin glob package
            - Some work has been done here already, feel free to pull useful lines
              from ./deprecate/DocumentIngestion.py
        """

        # Check depth and valid parent directory
        if depth == 0:
            raise ValueError("Desired Depths should be 1 indexed")

        if not os.path.exists(parent_directory):
            raise FileNotFoundError("The specified parent directory does not exist")

        # Grab all of our paths
        targets = self._crawl_directory(parent_directory, depth)

        # Extract text from each
        output_dict = {}
        for file_path in targets:
            output_dict[file_path] = self.extract_text_from_single_file(file_path)

        return output_dict

    def extract_text_from_a_zip_directory(self, zip_path: str, depth=None) -> Dict:
        """
        Given: a file path to a zip directory
        Return: A dictionary containing all data within the directory

        Steps:
            - Check the uncompressed size of the directory to avoid zip-bombs
            - Extract the directory a temporary location
            - Find the maximum depth
            - Pass temporary location to self.extract_all_files_from_directory
            - Delete temporary location
            - Return values to caller

        Notes:
            - Size check only really works for very basic zip bombs and naive approaches.
            Would flounder under any sort of pressure. This should not be a trusted as a
            true last line of defense. Don't run this outside of a resource-capped container
        """

        if not os.path.exists(zip_path):
            raise FileNotFoundError("The specified zip path does not exist")

        working_zip = zp(zip_path, "r")
        working_zip.testzip()

        # check for potential overflow
        file_info = working_zip.infolist()

        file_sizes = [t_file.file_size / 1000 for t_file in file_info]

        if sum(file_sizes) > MAX_ZIP_SIZE:
            raise RuntimeError(
                f"Uncompressed Zip file would exceed maximum directory size of {MAX_ZIP_SIZE / 1000 / 1000}GB."
            )

        # create a temp directory for peace of mind on deletion later
        #   - Happy to let Errors bubble to top since this will be run as a job
        os.makedirs("temp_file_location", exists_ok=False)

        working_zip.extractall(path="temp_file_location")

        depth = self._get_depth("temp_file_location")

        output = self.extract_text_from_all_files_in_directory(
            "temp_file_location", depth
        )

        shutil.rmtree("temp_file_location")

        return output

    def hash_and_cache_output(self, output: str) -> tuple[bool, int]:
        """
        Given: A file path and an output string
        Return: A boolean representing whether this has existed already or not

        Steps:
            - Hash the output
            - Pass hash and output to database object to check if hash exists
            - Return the output from the database object
        """

    # Private methods
    def _extract_text_from_txt_file(self, file_path: str) -> str:
        """
        Given: A .txt file path
        Return: All lines in a string
        """
        output = None

        with open(file_path, "r") as ifile:
            output = ifile.readlines()

        output = "".join(output)

        return self._normalize_output(output)

    def _extract_text_from_word_file(self, file_path: str) -> str:
        """
        Given: A .doc or .docx file path
        Return: All lines in a string

        Notes:
            - Should support all word document file types back to say the early 2000's
            - For now, images can be ignored
            - Table data can also be ignored
            - Feel free to split into multiple helper methods if necessary
        """

        output = None

        output = textract.process(file_path, encoding="ascii")
        output = output.decode("utf8")

        return self._normalize_output(output)

    def _extract_text_from_pdf_file(self, file_path: str) -> str:
        """
        Given: A .pdf file path
        Return: All lines in a string

        Notes:
            - For now, images can be ignored
            - Table data can also be ignored
        """

        output = None

        output = textract.process(file_path, encoding="ascii")
        output = output.decode("utf8")

        return self._normalize_output(output)

    def _normalize_output(self, output: str) -> str:
        targets = ["\n", "\t", "\r", "'\n'"]

        output = output.strip()
        for t in targets:
            output = output.replace(t, "")

        return output

    def _crawl_directory(self, directory: str, depth: int) -> list:
        """
        Given: A directory path and depth
        Return: A list of all valid files in that directory down to the defined depth
        """

        # Generate our pattern
        patterns = self._generate_glob_patterns(directory, depth)

        # Grab a list of all the possible files
        all_valid_paths = []
        for file_type_pattern in patterns:
            all_valid_paths = [*glob.glob(file_type_pattern), *all_valid_paths]

        return all_valid_paths

    def _expand_contractions(self, contracted_text: str) -> str:
        """
        Given: A string containing text
        Return: A copy of the string with all contractions expanded

        Notes:
            - See here for implementation:
            - https://towardsdatascience.com/text-summarization-using-deep-neural-networks-e7ee7521d804
        """
        with open("contractions.json", "r") as f:
            cList = json.load(f)
        c_re = re.compile(f'({"|".join(cList.keys())})')
        return c_re.sub(lambda match: cList[match.group(0)], contracted_text.lower())

    def _generate_hash(self, string_to_hash: str) -> str:
        """
        Given: A string
        Return: a SHA256 hash based on said string
        """

        return hashlib.sha256(string_to_hash.encode()).digest().hex()

    def _generate_glob_patterns(self, parent_directory: str, depth: int) -> list:

        while parent_directory[-1] in ("/", "\\"):
            parent_directory = parent_directory[:-1]

        if parent_directory[1] in [":"]:
            # This is supposed to handle drive letters, but hasn't been needed
            pass

        elif parent_directory[0] not in ("/", "\\"):
            parent_directory = "/" + parent_directory

        glob_patterns = []
        for ext in self.extensions:
            for current_depth in range(1, depth + 1):
                glob_patterns.append(f'{parent_directory}{"/*" * current_depth}{ext}')

        return glob_patterns

    def _get_depth(self, path, depth=0):
        """
        Recursively derive the maximum depth of a given directory
        Lifted From: https://stackoverflow.com/a/46921890
        """
        if not os.path.isdir(path):
            return depth
        maxdepth = depth
        for entry in os.listdir(path):
            fullpath = os.path.join(path, entry)
            maxdepth = max(maxdepth, self._get_depth(fullpath, depth + 1))
        return maxdepth
