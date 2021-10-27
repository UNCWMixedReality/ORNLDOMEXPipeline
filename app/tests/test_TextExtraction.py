from app.TextExtraction import TextExtractor
import re
import os
from hashlib import sha256
import pytest

# File Extraction
# def test_valid_txt_file_path(new_text_extractor, expected_output, app_directory):
#     new_output = new_text_extractor.extract_text_from_single_file(
#         app_directory + "/tests/test_data/goldilocks.txt"
#     )

#     assert new_output == expected_output


# def test_invalid_txt_file_path(new_text_extractor):
#     with pytest.raises(FileNotFoundError):
#         new_text_extractor.extract_text_from_single_file("/foo/bar")


# def test_single_simple_docx_file(new_text_extractor, expected_output, app_directory):
#     new_output = new_text_extractor.extract_text_from_single_file(
#         app_directory + "/tests/test_data/goldilocks_only.docx"
#     )

#     assert new_output == expected_output


# def test_single_simple_doc_file(new_text_extractor, expected_output, app_directory):
#     new_output = new_text_extractor.extract_text_from_single_file(
#         app_directory + "/tests/test_data/goldilocks_only.doc"
#     )

#     assert new_output == expected_output


# def test_single_complex_docx_file(new_text_extractor, expected_output, app_directory):
#     new_output = new_text_extractor.extract_text_from_single_file(
#         app_directory
#         + "/tests/test_data/goldilocks_tables_and_photo_and_messy_formatting.docx"
#     )

#     assert new_output == expected_output


# def test_single_complex_pdf_file(new_text_extractor, expected_output, app_directory):
#     new_output = new_text_extractor.extract_text_from_single_file(
#         app_directory
#         + "/tests/test_data/goldilocks_tables_and_photo_and_messy_formatting.pdf"
#     )

#     assert new_output == expected_output


# File Discovery
def test_directory_crawler_top_level(new_text_extractor, app_directory):
    output = new_text_extractor._crawl_directory(app_directory + "/tests/test_data", 1)
    print(output)
    print(os.getcwd() + "/tests/test_data")

    def _regex_search(pattern: str, output_list: list) -> bool:
        for path in output_list:
            if re.search(pattern, path):
                return True

        return False

    assert _regex_search(r"test_data/goldilocks.txt", output)
    assert not _regex_search(r"test_data/level2/level3/bar.txt", output)


def test_directory_crawler_bottom_level(new_text_extractor, app_directory):
    output = new_text_extractor._crawl_directory(
        (app_directory + "/tests/test_data"), 3
    )

    def _regex_search(pattern: str, output_list: list) -> bool:
        for path in output_list:
            if re.search(pattern, path):
                return True

        return False

    assert _regex_search(r"test_data/goldilocks.txt", output)
    assert _regex_search(r"test_data/level2/foo.txt", output)
    assert _regex_search(r"test_data/level2/level3/bar.txt", output)


def test_invalid_parent_directory(new_text_extractor):
    with pytest.raises(FileNotFoundError):
        new_text_extractor.extract_text_from_all_files_in_directory("/foo/bar", 1)


def test_invalid_depth(new_text_extractor):
    with pytest.raises(ValueError):
        new_text_extractor.extract_text_from_all_files_in_directory("test_data", 0)


# Text Formatting
def test_contraction_expansion(new_text_extractor):
    expected_output = "I cannot wait for the day that coffee is not a stigma. I will not go a day without it."
    test_input = "I can't wait for the day that coffee isn't a stigma. I won't go a day without it."

    generated_output = new_text_extractor._expand_contractions(test_input)

    assert expected_output == generated_output


# Hashing
def test_output_hashing(new_text_extractor):
    # https://stackoverflow.com/questions/48613002/sha-256-hashing-in-python

    string_to_hash = "This is a beautiful new string ready for hashing"
    test_hash = sha256(string_to_hash.encode("utf-8")).hexdigest()

    generated_hash = new_text_extractor._generate_hash(string_to_hash)

    assert test_hash == generated_hash
