import configparser
import os
import pdb
import shutil
import sys
import unittest


# sys.path.append(
#     r"C:\Users\simon.munns\OneDrive - Health Education England\Documents\sm BI\Natinal Bi\sprint 132\FandF\tests\test_setup.py"
# )

from io import StringIO
from unittest.mock import mock_open, patch, MagicMock

##


# from setup import TestEnvironmentSetup it will not take the extruanl souce
sys.path.append(r"C:\Users\simon.munns\OneDrive - Health Education England\Documents\sm BI\Natinal Bi\sprint 132\FandF\main_setup.py")  # type: ignore
from main_setup import (
    extract_month_and_year,
    main,
    move_file_to_year_and_month_folders,
    print_folder_tree,
)

sys.path.append(r"C:\Users\simon.munns\OneDrive - Health Education England\Documents\sm BI\Natinal Bi\sprint 132\FandF\seupachieve.py")  # type: ignore
from seupachieve import seupAchieve


class TestYourScript(unittest.TestCase):
    """Test cases for YourScript."""

    @classmethod
    def setUpClass(cls):
        """Set up a temporary directory for testing."""

        class TestEnvironmentSetup:
            # Todo I need to check the file location is free befor it tests ot make a new one sadly. I can also cehck teh root is ok

            def __init__(self, config_file="config.txt"):
                # Use '..' to go up one level from the current working directory
                config_path = os.path.join(os.path.dirname(__file__), config_file)
                self.config = self.load_config(config_path)

                # Assume 'General' is the section name in your config file
                self.test_dir = self.config.get(
                    "General", r"test_dir", fallback="test_temp_directory"
                )

            def load_config(self, config_file):
                config = configparser.ConfigParser()
                config.read(config_file)
                return config

            def setup_test_directory(self):
                with patch(self.test_dir):
                    cls.test_environment_setup.setup_test_directory()

            def teardown_test_directory(self):
                with patch(self.test_dir):
                    cls.test_environment_setup.teardown_test_directory()

        cls.test_environment_setup = TestEnvironmentSetup()
        # cls.test_environment_setup.setup_test_directory()

    @classmethod
    def tearDownClass(cls):
        """Remove the temporary directory after testing."""

        os.rmdir(cls.test_environment_setup.test_dir)
        cls.test_environment_setup.teardown_test_directory()

    def test_extract_month_and_year_valid_format(self):
        file_name = "2023-11_file.txt"
        result = extract_month_and_year(file_name)
        self.assertEqual(result, (2023, 11))

    def test_extract_month_and_year_month_string_april(self):
        file_name = "2023-April_file.txt"
        result = extract_month_and_year(file_name)
        self.assertEqual(result, (2023, 4))

    def test_extract_month_and_year_month_string_short_apr(self):
        file_name = "2023-Apr_file.txt"
        result = extract_month_and_year(file_name)
        self.assertEqual(result, (2023, 4))

    def test_extract_month_and_year_invalid_format(self):
        file_name = "invalid_file_name.csv"
        result = extract_month_and_year(file_name)
        self.assertNotEqual(
            result, (0, 0)
        )  # You might want to choose a specific default value

    # to
    def test_move_file_to_year_and_month_folders(self):
        """
        Test the movement of a file to year and month folders.

        The function creates a temporary file, moves it to year and month folders
        using 'move_file_to_year_and_month_folders', and then checks if the
        folders and the moved file exist.

        """
        # Create a temporary file for testing
        test_file = os.path.join(self.test_environment_setup.test_dir, "test_file.csv")
        with open(
            test_file,
            "w",
        ) as f:
            f.write("Test content")
            f.close()

        # Mock os.makedirs to avoid actual directory creation
        with patch("os.makedirs"):
            # Mock os.path.exists to simulate directory existence
            with patch("os.path.exists", side_effect=[False, False, False, True]):
                # Move the file to year and month folders
                move_file_to_year_and_month_folders(test_file)

        # Check if the folders have been created
        year_folder = os.path.join(self.test_environment_setup.test_dir, "y2022")
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
        with patch.object(sys, "argv", ["script.py", "input_folder_address"]):  # type: ignore
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
        with patch.object(sys, "argv", self.test_environment_setup.test_dir):
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
        print_folder_tree(self.test_environment_setup.test_dir)

        # Get the printed output
        printed_output = sys.stdout.getvalue()

        # Reset standard output
        sys.stdout = original_stdout

        # Check if the expected output is in the printed output
        expected_output = "Folder Tree Structure:"
        self.assertIn(expected_output, printed_output)

    def test_create_folders_if_not_exist(self):
        """
        Test create_folders_if_not_exist function.
        """

        with patch("your_module.os.path.exists", return_value=False), patch(
            "your_module.os.makedirs"
        ) as mock_makedirs:
            seupAchieve.create_folders_if_not_exist(
                self.test_environment_setup.test_dir
            )
            mock_makedirs.assert_any_call(self.test_data_path)
            mock_makedirs.assert_any_call(self.test_archive_path)

    def test_move_folders(self):
        """
        Test move_folders function.
        """
        os.makedirs(self.test_data_path)
        folder_to_move: str = os.path.join(self.test_data_path, "folder_to_move")
        os.makedirs(folder_to_move)

        with patch("your_module.shutil.move") as mock_move:
            seupAchieve.move_folders(self.test_data_path, self.test_archive_path)
            mock_move.assert_called_once_with(
                folder_to_move, os.path.join(self.test_archive_path, "folder_to_move")
            )

    def test_add_timestamp_to_new_files(self):
        """
        Test add_timestamp_to_new_files function.
        """
        os.makedirs(self.active_folder_path)
        file_to_modify: str = os.path.join(self.active_folder_path, "file.txt")
        with open(file_to_modify, "w") as file:
            file.write("content")

        with patch("your_module.datetime") as mock_datetime:
            mock_datetime.now.return_value = MagicMock(
                spec=datetime, strftime=MagicMock(return_value="20220101120000")
            )
            seupAchieve.add_timestamp_to_new_files(self.active_folder_path)
            new_file_path: str = os.path.join(
                self.active_folder_path, "file_20220101120000.txt"
            )
            self.assertTrue(os.path.exists(new_file_path))

    def test_to_empty_folder(self):
        """
        Test to_empty_folder function.
        """
        with patch("your_module.shutil.rmtree") as mock_rmtree:
            to_empty_folder(self.test_environment_setup.test_dir)
            mock_rmtree.assert_called_once_with(self.test_environment_setup.test_dir)
