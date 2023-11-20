import os
import sys

sys.path.append("/tests/test_setup")
import unittest
from io import StringIO
from unittest.mock import patch

# Todo can not work out why this is not working
from test_setup import TestEnvironmentSetup

from main import (
    extract_month_and_year,
    main,
    move_file_to_year_and_month_folders,
    print_folder_tree,
)


class TestYourScript(unittest.TestCase):
    def setUp(self):
        # Set up a temporary directory for testing
        cls.test_environment_setup = TestEnvironmentSetup()
        cls.test_environment_setup.setup_test_directory()

    def tearDown(self):
        # Remove the temporary directory after testing
        os.rmdir(self.test_dir)

    def test_extract_month_and_year_valid_format(self):
        """
        Test the extraction of month and year from a valid file name format.

        The function uses the 'extract_month_and_year' function to extract the
        month and year from a valid file name format and asserts that the result
        matches the expected values.

        """
        file_name = "fft ae 2013.04 Apr.sites.csv"
        result = extract_month_and_year(file_name)
        self.assertEqual(result, (2013, 4))

    def test_extract_month_and_year_invalid_format(self):
        """
        Test the extraction of month and year from an invalid file name format.

        The function uses the 'extract_month_and_year' function to extract the
        month and year from an invalid file name format and asserts that the
        result does not match a specific default value.

        """
        file_name = "invalid_file_name.csv"
        result = extract_month_and_year(file_name)
        self.assertNotEqual(
            result, (0, 0)
        )  # You might want to choose a specific default value

    def test_move_file_to_year_and_month_folders(self):
        """
        Test the movement of a file to year and month folders.

        The function creates a temporary file, moves it to year and month folders
        using 'move_file_to_year_and_month_folders', and then checks if the
        folders and the moved file exist.

        """
        # Create a temporary file for testing
        test_file = os.path.join(self.test_dir, "test_file.csv")
        with open(test_file, "w") as f:
            f.write("Test content")

        # Move the file to year and month folders
        move_file_to_year_and_month_folders(test_file)

        # Check if the folders have been created
        year_folder = os.path.join(self.test_dir, "y2022")
        month_folder = os.path.join(year_folder, "m11")
        self.assertTrue(os.path.exists(year_folder))
        self.assertTrue(os.path.exists(month_folder))
        self.assertTrue(os.path.exists(os.path.join(month_folder, "test_file.csv")))

    def test_main_with_valid_input(self):
        """
        Test the 'main' function with valid input.

        The function uses the 'patch' method to simulate command line arguments
        and checks if 'main' is executed without errors.

        """
        with patch.object(sys, "argv", ["script.py", "input_folder_address"]):
            # Replace 'script.py' and 'input_folder_address' with actual script and folder address
            with patch("builtins.print") as mock_print:
                main()

        mock_print.assert_not_called()  # Ensure that print is not called for valid input

    def test_main_with_invalid_input(self):
        """
        Test the 'main' function with invalid input.

        The function uses the 'patch' method to simulate missing command line
        arguments and checks if 'sys.exit' is called with the correct status.

        """
        with patch.object(sys, "argv", ["script.py"]):
            with patch("sys.exit") as mock_exit:
                main()

        mock_exit.assert_called_with(
            1
        )  # Ensure sys.exit is called with status 1 for invalid input

    def test_print_folder_tree(self):
        """
        Test the printing of the folder tree structure.

        The function redirects standard output to capture the print output of
        'print_folder_tree'. It then checks if the expected output indicating the
        folder tree structure is present in the captured output.

        """

        # Redirect standard output to capture print output

        original_stdout = sys.stdout
        sys.stdout = StringIO()

        # Print the folder tree
        print_folder_tree(self.test_dir)

        # Get the printed output
        printed_output = sys.stdout.getvalue()

        # Reset standard output
        sys.stdout = original_stdout

        # Check if the expected output is in the printed output
        expected_output = "Folder Tree Structure:"
        self.assertIn(expected_output, printed_output)


if __name__ == "__main__":
    unittest.main()
