import glob
import os
import platform


def top_n_levels_expression(
    parent_directory: str, desired_depth: int, file_type: str
) -> str:
    """Should be 1 indexed. For example, top two levels would be 2, top level would be 1"""
    if desired_depth == 0:
        raise ValueError("Desired Depths should be 1 indexed")

    # Cleanup
    if file_type[0] != ".":
        file_type = "." + file_type

    while parent_directory[-1] in ("/", "\\"):
        parent_directory = parent_directory[:-1]

    if parent_directory[1] in [":"]:
        pass
    elif parent_directory[0] not in ("/", "\\"):
        parent_directory = "/" + parent_directory

    return f'{parent_directory}{"/*" * desired_depth}{file_type}'


def grab_all_filenames(pattern: str) -> list:
    return glob.glob(pattern)


def extract_text_from_document(filename: str) -> str:
    with open(filename, encoding="utf8") as ifile:
        return ifile.read().replace("\n", " ")


def extract_all_data_from_a_directory(
    parent_directory: str, desired_depth: int
) -> dict:
    expression = top_n_levels_expression(parent_directory, desired_depth, ".txt")
    # print(f'[INFO] Expression: {expression}')
    all_files = glob.glob(expression)
    # print(f'[INFO] File List: {all_files}')

    extracted_data = {}

    for each_file in all_files:
        text = extract_text_from_document(each_file)
        print(f"[INFO] Text Extracted: {text[0:150]}")

        if platform.system() == "Windows":
            name = each_file.split("\\")[-1].replace(".txt", "")
        else:
            name = each_file.split("/")[-1].replace(".txt", "")

        # print(f'[INFO] Name Generated: {name}')

        extracted_data[name] = {"text": text}

    # print(f'[INFO] Final Dictionary: {extracted_data}')

    return extracted_data


# print(extract_all_data_from_a_directory(os.getcwd() + "/speeches/", 1))
