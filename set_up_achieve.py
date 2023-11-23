# file_operations.py
import os
import shutil
from datetime import datetime


class seupAchieve:
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
        Initialize the seupAchive instance.

        Args:
            root_folder (str): The root folder path.
        """
        self.root_folder = root_folder

        if self.navigate_up_to_folder(root_folder, "test_data") != "":
            self.test_data_path = self.navigate_up_to_folder(root_folder, "test_data")
        else:
            self.test_data_path = os.path.join(root_folder, "test_data")
        if "test_archive" not in root_folder:
            self.test_archive_path = os.path.join(root_folder, "test_archive")

        if self.navigate_up_to_folder(root_folder, "test_archive") != "":
            self.test_archive_path = self.navigate_up_to_folder(
                root_folder, "test_archive"
            )
        else:
            self.test_data_path = os.path.join(root_folder, "test_archive")

        if self.navigate_up_to_folder(root_folder, "active") != "":
            self.test_archive_path = self.navigate_up_to_folder(root_folder, "active")
        else:
            self.test_data_path = os.path.join(root_folder, "active")

    def navigate_up_to_folder(self, start_path, target_folder):
        """
        Navigate up the directory structure from the given start path until finding the target folder.

        Args:
            start_path (str): The starting path from which to navigate.
            target_folder (str): The name of the target folder to find.

        Returns:
            str: The path to the target folder if found, or an empty string if not found.
        """
        current_path = os.path.abspath(start_path)

        while os.path.basename(current_path) != target_folder:
            # Move up one level in the directory structure
            current_path = os.path.dirname(current_path)

            # Break if we reach the root directory
            if current_path == os.path.dirname(current_path):
                return ""

        return current_path

    def create_folders_if_not_exist(self):
        """
        Create "test_data" and "test_archive" folders if they don't exist.

        Returns:
            None

        Examples:
            >>> file_ops = seupAchive("/path/to/root")
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
            >>> file_ops = seupAchive("/path/to/root")
            >>> os.makedirs("/path/to/root/test_data/folder_to_move")
            >>> file_ops.move_folders("/path/to/root/test_data", "/path/to/root/test_archive")
            >>> os.path.exists("/path/to/root/test_archive/folder_to_move")
            True
        """
        item_path_list = []
        for item in os.listdir(source_folder):
            item_path = os.path.join(source_folder, item)
            if os.path.isdir(item_path) and not item.startswith("_"):
                shutil.move(item_path, os.path.join(destination_folder, item))
                item_path_list.append(item_path)

        return item_path_list

    def add_timestamp_to_new_files(self, folder):
        """
        Add date-time stamp to new files in the folder.

        Args:
            folder (str): The folder path.

        Returns:
            None

        Examples:
            >>> file_ops = seupAchive("/path/to/root")
            >>> os.makedirs("/path/to/root/test_archive/active")
            >>> with open("/path/to/root/test_archive/active/file.txt", "w") as file:
            ...     file.write("content")
            >>> file_ops.add_timestamp_to_new_files("/path/to/root/test_archive/active")
            >>> os.path.exists("/path/to/root/test_archive/active/file_{}.txt".format(datetime.now().strftime('%Y%m%d%H%M%S')))
            True
        """
        import pdb

        pdb.set_trace()
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
            >>> file_ops = seupAchive("/path/to/root")
            >>> file_ops.to_empty_folder()
        """
        self.create_folders_if_not_exist()

        item_path_list = self.move_folders(self.test_data_path, self.test_archive_path)
        self.add_timestamp_to_new_files(item_path_list)
        self.move_folders(self.test_data_path, self.test_archive_path)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
