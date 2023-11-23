# file_operations.py
import os
import shutil
from datetime import datetime


class FileOperations:
    """
    A class containing file operations to manage "test_data" and "test_archive" folders.

    Attributes:
        root_folder (str): The root folder path.
        test_data_path (str): The path to the "test_data" folder.
        test_archive_path (str): The path to the "test_archive" folder.
        active_folder_path (str): The path to the "active" folder inside "test_archive".
    """

    def __init__(self, root_folder):
        """
        Initialize the FileOperations instance.

        Args:
            root_folder (str): The root folder path.
        """
        self.root_folder = root_folder
        self.test_data_path = os.path.join(root_folder, "test_data")
        self.test_archive_path = os.path.join(root_folder, "test_archive")
        self.active_folder_path = os.path.join(self.test_archive_path, "active")

    def create_folders_if_not_exist(self):
        """
        Create "test_data" and "test_archive" folders if they don't exist.

        Returns:
            None

        Examples:
            >>> file_ops = FileOperations("/path/to/root")
            >>> file_ops.create_folders_if_not_exist()
            >>> os.path.exists("/path/to/root/test_data")
            True
            >>> os.path.exists("/path/to/root/test_archive")
            True
        """
        for folder_path in [self.test_data_path, self.test_archive_path]:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

    def move_folders(self, source_folder, destination_folder):
        """
        Move folders from source_folder to destination_folder.

        Args:
            source_folder (str): The source folder path.
            destination_folder (str): The destination folder path.

        Returns:
            None

        Examples:
            >>> file_ops = FileOperations("/path/to/root")
            >>> os.makedirs("/path/to/root/test_data/folder_to_move")
            >>> file_ops.move_folders("/path/to/root/test_data", "/path/to/root/test_archive")
            >>> os.path.exists("/path/to/root/test_archive/folder_to_move")
            True
        """
        for item in os.listdir(source_folder):
            item_path = os.path.join(source_folder, item)
            if os.path.isdir(item_path) and not item.startswith("_"):
                shutil.move(item_path, os.path.join(destination_folder, item))

    def add_timestamp_to_new_files(self, folder):
        """
        Add date-time stamp to new files in the folder.

        Args:
            folder (str): The folder path.

        Returns:
            None

        Examples:
            >>> file_ops = FileOperations("/path/to/root")
            >>> os.makedirs("/path/to/root/test_archive/active")
            >>> with open("/path/to/root/test_archive/active/file.txt", "w") as file:
            ...     file.write("content")
            >>> file_ops.add_timestamp_to_new_files("/path/to/root/test_archive/active")
            >>> os.path.exists("/path/to/root/test_archive/active/file_{}.txt".format(datetime.now().strftime('%Y%m%d%H%M%S')))
            True
        """
        for item in os.listdir(folder):
            item_path = os.path.join(folder, item)
            if os.path.isfile(item_path) and not item.startswith("_"):
                current_time = datetime.now().strftime("%Y%m%d%H%M%S")
                new_file_name = (
                    f"{item.split('.')[0]}_{current_time}.{item.split('.')[1]}"
                )
                os.rename(item_path, os.path.join(folder, new_file_name))

    def to_empty_folder(self):
        """
        Perform actions to make the specified folders empty and move files.

        Returns:
            None

        Examples:
            >>> file_ops = FileOperations("/path/to/root")
            >>> file_ops.to_empty_folder()
        """
        self.create_folders_if_not_exist()

        self.move_folders(self.test_data_path, self.test_archive_path)
        self.add_timestamp_to_new_files(self.active_folder_path)
        self.move_folders(self.test_data_path, self.test_archive_path)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
