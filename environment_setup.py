import os
import sys
import configparser
from unittest.mock import patch


class EnvironmentSetup:
    """
    A class for setting up and tearing down an environment.

    Attributes:
        config_file (str): The path to the configuration file.
        config (configparser.ConfigParser): The configuration parser.
        base_dir (str): The base directory path.
    """

    def __init__(self, config_file: str = "config.txt", is_test: bool = True) -> None:
        """
        Initializes the EnvironmentSetup.

        Args:
            config_file (str): The path to the configuration file. Defaults to "config.txt".
            is_test (bool): True if it's a test environment, False for live environment. Defaults to True.
        """
        # Use '..' to go up one level from the current working directory
        config_path = os.path.join(os.path.dirname(__file__), config_file)
        self.config = self.load_config(config_path)

        # Assume 'General' is the section name in your config file
        self.base_dir_key = "test_dir" if is_test else "live_dir"
        self.base_dir = self.config.get(
            "General", self.base_dir_key, fallback="default_directory"
        )

    def load_config(self, config_file: str) -> configparser.ConfigParser:
        """
        Loads and returns the configuration parser.

        Args:
            config_file (str): The path to the configuration file.

        Returns:
            configparser.ConfigParser: The configuration parser.
        """
        config = configparser.ConfigParser()
        config.read(config_file)
        return config

    def setup_directory(self) -> None:
        """
        Sets up the directory.
        """
        with patch(self.base_dir):
            self.environment_setup.setup_directory()

    def teardown_directory(self) -> None:
        """
        Tears down the directory.
        """
        with patch(self.base_dir):
            self.environment_setup.teardown_directory()


if __name__ == "__main__":
    # Get the root input location and test mode from command line arguments
    root_location = sys.argv[1] if len(sys.argv) > 1 else "."
    test_mode = bool(int(sys.argv[2])) if len(sys.argv) > 2 else True

    # Instantiate EnvironmentSetup based on command line arguments
    env_setup = EnvironmentSetup(is_test=test_mode)
