import configparser
import os


class TestEnvironmentSetup:
    def __init__(self, config_file="../config.txt"):
        # Use '..' to go up one level from the current working directory
        config_path = os.path.join(os.path.dirname(__file__), config_file)
        self.config = self.load_config(config_path)
        self.test_dir = self.config.get(
            "config", "test_dir", fallback="test_temp_directory"
        )

    def load_config(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        return config

    def setup_test_directory(self):
        os.makedirs(self.test_dir)

    def teardown_test_directory(self):
        os.rmdir(self.test_dir)


if __name__ == "__main__":
    unittest.main()
