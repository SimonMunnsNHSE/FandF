from typing import Tuple
import re
from datetime import datetime
import os
import shutil
import sys

from environment_setup import EnvironmentSetup
from seupachieve import seupAchieve


def extract_month_and_year(file_name: str) -> Tuple[int, int]:
    """
    Extracts the month and year from the given file name.

    Args:
        file_name (str): The name of the file.

    Returns:
        Tuple[int, int]: A tuple containing the year and month.

    >>> extract_month_and_year("2023-11_file.txt")
    (2023, 11)
    >>> extract_month_and_year("2023-April_file.txt")
    (2023, 4)
    >>> extract_month_and_year("2023-Apr_file.txt")
    (2023, 4)
    """
    # Regular expression pattern for matching yyyy.mm or mm.yyyy
    pattern = re.compile(r"(\d{4})[.-](\d{2})")

    match = pattern.search(file_name)
    if match:
        year, month = map(int, match.groups())
        return year, month
    else:
        # Try to find month strings in the file name and map them to numeric values
        month_strings = [
            "jan",
            "feb",
            "mar",
            "apr",
            "may",
            "jun",
            "jul",
            "aug",
            "sep",
            "oct",
            "nov",
            "dec",
        ]
        for index, month_str in enumerate(month_strings, start=1):
            if month_str in file_name.lower():
                current_date = datetime.now()
                return current_date.year, index

        # Default to current year and month if no pattern or relevant month string is found
        current_date = datetime.now()
        return current_date.year, current_date.month


def move_file_to_year_and_month_folders(file_path: str):
    """
    Moves the file directly into the year and month subfolders in the specified format.

    Args:
        file_path (str): The path to the file.

    >>> move_file_to_year_and_month_folders("C:\\path\\to\\file\\2023-11_file.txt")
    """
    # Extracting year and month from the file name
    year, month = extract_month_and_year(os.path.basename(file_path))

    # Creating year folder in the Google style guide format
    year_folder = f"y{year}"

    # Creating month subfolder in the Google style guide format
    month_subfolder = f"m{month}"

    # Creating the year folder if it doesn't exist
    year_folder_path = os.path.join(os.path.dirname(file_path), year_folder)
    if not os.path.exists(year_folder_path):
        os.makedirs(year_folder_path)

    # Creating the month subfolder inside the year folder if it doesn't exist
    month_folder_path = os.path.join(year_folder_path, month_subfolder)
    if not os.path.exists(month_folder_path):
        os.makedirs(month_folder_path)

    # Destination path for the file in the year and month subfolders
    destination_path = os.path.join(month_folder_path, os.path.basename(file_path))
    # Check if the file already exists in the destination folder
    if os.path.exists(destination_path):
        print(
            f"File '{os.path.basename(file_path)}' already exists in the destination folder. Skipping."
        )
        return

    # Moving the file into the year and month subfolders
    shutil.move(file_path, destination_path)


# def print_folder_tree(input_folder: str):

#     """
#     Prints the folder tree structure starting from the specified input folder.

#     Args:
#         input_folder (str): The path to the input folder.

#     Note: This function prints the folder tree structure and does not return a value.
#     Example usage (not a typical doctest due to printing)
#     >>> print_folder_tree("C:\\path\\to\\input\\folder")
#     """
#     pass


def main():
    # Check if the input folder address is provided in the command line
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_folder_address>")
        sys.exit(1)

    input_folder_address = sys.argv[1] if len(sys.argv) > 1 else "."
    test_mode = bool(int(sys.argv[2])) if len(sys.argv) > 2 else True

    # Instantiate EnvironmentSetup based on command line arguments
    env_setup = EnvironmentSetup(is_test=test_mode)
    env_setup.setup_directory()
    file_ops = seupAchieve(input_folder_address)
    file_ops.to_empty_folder()

    # Move files to year and month folders
    for root, _, files in os.walk(input_folder_address):
        if "CSV" in root:
            for file_name in files:
                file_path = os.path.join(root, file_name)
                move_file_to_year_and_month_folders(file_path)

    # Print updated folder tree structure
    # print_folder_tree(input_folder_address)


if __name__ == "__main__":
    main()
