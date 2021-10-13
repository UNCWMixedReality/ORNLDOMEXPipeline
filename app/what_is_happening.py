from TextExtraction import TextExtractor
import os
import re


test = TextExtractor()

print(test._generate_glob_patterns((os.getcwd() + "/tests/test_data"), 3))
print(test._crawl_directory((os.getcwd() + "/tests/test_data"), 3))


def _regex_search(pattern: str, output_list: list) -> bool:
    for path in output_list:
        if re.search(pattern, path):
            return True

    return False


output = test._crawl_directory((os.getcwd() + "/tests/test_data"), 3)

print(_regex_search(r"test_data/goldilocks.txt", output))
