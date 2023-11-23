import configparser
import os
import sys
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

sys.path.append(r"C:\Users\simon.munns\OneDrive - Health Education England\Documents\sm BI\Natinal Bi\sprint 132\FandF\environment_setup.py")  # type: ignore
from ..environment_setup import EnvironmentSetup

sys.path.append(r"C:\Users\simon.munns\OneDrive - Health Education England\Documents\sm BI\Natinal Bi\sprint 132\FandF\set_up_achieve.py")  # type: ignore
from ..set_up_achieve import seupAchieve


class TestToEmptyFolder(unittest.TestCase):
    """
    Unit tests for the to_empty_folder function.
    """

    @classmethod
    def setUp(cls):
        cls.test_environment_setup = EnvironmentSetup(is_test=test_mode)

    def test_create_folders_if_not_exist(self):
        """
        Test create_folders_if_not_exist function.
        """
        with patch("your_module.os.path.exists", return_value=False), patch(
            "your_module.os.makedirs"
        ) as mock_makedirs:
            seupAchieve.create_folders_if_not_exist(
                self.test_environment_setup.test_dir  # type: ignore
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
            seupAchieve.to_empty_folder(self.root_folder)
            mock_rmtree.assert_called_once_with(self.root_folder)
