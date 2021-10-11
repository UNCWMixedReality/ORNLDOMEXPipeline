# NOTE: Ensure you're using logging where it would be useful. The Log level is
# declared in __main__, but stick to [info] for high level things "Extracted x amount of files"
# and [debug] for things that will be helpful when stuff breaks, like all FileNotFound errors


class TextExtractor(object):
    def __init__(self):
        pass

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
        return None

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

        return None

    def hash_and_cache_output(self, output: str) -> tuple[bool, int]:
        """
        Given: A file path and an output strung
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

        return None

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

        return None

    def _extract_text_from_pdf_file(self, file_path: str) -> str:
        """
        Given: A .pdf file path
        Return: All lines in a string

        Notes:
            - For now, images can be ignored
            - Table data can also be ignored
        """

        return None

    def _crawl_directory(self, directory: str, depth: int) -> list:
        """
        Given: A directory path and depth
        Return: A list of all valid files in that directory down to the defined depth
        """

        return None

    def _expand_contractions(self, contracted_text: str) -> str:
        """
        Given: A string containing text
        Return: A copy of the string with all contractions expanded

        Notes:
            - See here for implementation:
            - https://towardsdatascience.com/text-summarization-using-deep-neural-networks-e7ee7521d804
        """

        return None

    def _generate_hash(self, string_to_hash: str) -> int:
        """
        Given: A string
        Return: a SHA256 hash based on said string
        """

        return None
