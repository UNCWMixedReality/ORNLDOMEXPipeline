# import os
# import unittest

# from DocumentIngestion import extract_text_from_document, top_n_levels_expression


# class Test_top_n_levels_expression(unittest.TestCase):

#     # Ideal Cases
#     def test_ideal_case(self):
#         expectation = "/home/sra6535/documents/*/*.txt"
#         result = top_n_levels_expression("/home/sra6535/documents", 2, ".txt")
#         self.assertEqual(result, expectation)

#     def test_top_level_ideal_case(self):
#         expectation = "/home/sra6535/documents/*.txt"
#         result = top_n_levels_expression("/home/sra6535/documents/", 1, ".txt")
#         self.assertEqual(result, expectation)

#     # Argument Mistakes
#     def test_zero_indexed_depth(self):
#         with self.assertRaises(ValueError):
#             top_n_levels_expression("/home/sra6535/documents", 0, ".txt")

#     # Formatting Assurance
#     def test_no_leading_slash(self):
#         expectation = "/home/sra6535/documents/*/*.txt"
#         result = top_n_levels_expression("home/sra6535/documents", 2, ".txt")
#         self.assertEqual(result, expectation)

#     def test_unwanted_trailing_slash(self):
#         expectation = "/home/sra6535/documents/*/*.txt"
#         result = top_n_levels_expression("/home/sra6535/documents/", 2, ".txt")
#         self.assertEqual(result, expectation)

#     def test_multiple_unwanted_trailing_slashes(self):
#         expectation = "/home/sra6535/documents/*/*.txt"
#         result = top_n_levels_expression("/home/sra6535/documents////////", 2, ".txt")
#         self.assertEqual(result, expectation)

#     def test_missing_file_type_period(self):
#         expectation = "/home/sra6535/documents/*/*.txt"
#         result = top_n_levels_expression("/home/sra6535/documents/", 2, "txt")
#         self.assertEqual(result, expectation)


# class Test_extract_text_from_document(unittest.TestCase):

#     # Ideal Case
#     def test_ideal_case(self):
#         filename = os.getcwd() + "/tests/test.txt"
#         expectation = "This is a really cool document for my program to test against!"
#         result = extract_text_from_document(filename)
#         self.assertEqual(expectation, result)

#     # Argument Mistakes
#     def test_invalid_filename(self):
#         filename = "lol/this/isnt/valid/test.txt"

#         with self.assertRaises(FileNotFoundError):
#             extract_text_from_document(filename)


# if __name__ == "__main__":
#     unittest.main()
