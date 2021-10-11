from app.TextExtraction import TextExtractor
import re
import pytest

# File Extraction
def test_valid_txt_file_path(new_text_extractor, expected_output):
    new_output = new_text_extractor.extract_text_from_single_file(
        "./test_data/goldilocks.txt"
    )

    assert new_output == expected_output


def test_invalid_txt_file_path(new_text_extractor):
    with pytest.raises(FileNotFoundError):
        new_text_extractor.extract_text_from_single_file("/foo/bar")


def test_single_simple_docx_file(new_text_extractor, expected_output):
    new_output = new_text_extractor.extract_text_from_single_file(
        "./test_data/goldilocks_only.docx"
    )

    assert new_output == expected_output


def test_single_simple_doc_file(new_text_extractor, expected_output):
    new_output = new_text_extractor.extract_text_from_single_file(
        "./test_data/goldilocks_only.doc"
    )

    assert new_output == expected_output


def test_single_complex_docx_file(new_text_extractor, expected_output):
    new_output = new_text_extractor.extract_text_from_single_file(
        "./test_data/goldilocks_tables_and_photo_and_messy_formatting.docx"
    )

    assert new_output == expected_output


def test_single_complex_pdf_file(new_text_extractor, expected_output):
    new_output = new_text_extractor.extract_text_from_single_file(
        "./test_data/goldilocks_tables_and_photo_and_messy_formatting.pdf"
    )

    assert new_output == expected_output


# File Discovery
def test_directory_crawler_top_level(new_text_extractor):
    output = new_text_extractor._crawl_directory("test_data", 1)
    top_level = re.findall(r"\S*test_data\/goldilocks\.txt", output)
    bottom_level = re.findall(r"\S*test_data\/level2\/foo\.txt", output)

    assert len(top_level) == 1
    assert len(bottom_level) == 0


def test_directory_crawler_bottom_level(new_text_extractor):
    output = new_text_extractor._crawl_directory("test_data", 3)

    top_level = re.findall(r"\S*test_data\/goldilocks\.txt", output)
    mid_level = re.findall(r"\S*test_data\/level2\/foo\.txt", output)
    bottom_level = re.findall(r"S*test_data\/level2\/level3\/bar\.txt")

    assert len(top_level) == 1
    assert len(mid_level) == 1
    assert len(bottom_level) == 1


def test_invalid_parent_directory(new_text_extractor):
    with pytest.raises(FileNotFoundError):
        new_text_extractor._crawl_directory("/foo/bar", 1)


def test_invalid_depth(new_text_extractor):
    with pytest.raises(ValueError):
        new_text_extractor._crawl_directory("test_data", 0)


# Text Formatting
def test_contraction_expansion(new_text_extractor):
    expected_output = "I cannot wait for the day that coffee is not a stigma. I will not go a day without it."
    test_input = "I can't wait for the day that coffee isn't a stigma. I won't go a day without it."

    generated_output = new_text_extractor._expand_contractions(test_input)

    assert expected_output == generated_output
