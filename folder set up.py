import os


def create_project_structure(project_name="your_project", root_location="."):
    project_path = os.path.join(root_location, project_name)

    # Create the main project directory if it doesn't exist
    os.makedirs(project_path, exist_ok=True)

    # Change into the project directory
    os.chdir(project_path)

    # Create the your_module directory if it doesn't exist
    your_module_path = os.path.join(project_path, "your_module")
    os.makedirs(your_module_path, exist_ok=True)
    with open(os.path.join(your_module_path, "__init__.py"), "w") as f:
        f.write("print('Hello from your_module!')")

    # Create the tests directory if it doesn't exist
    tests_path = os.path.join(project_path, "tests")
    os.makedirs(tests_path, exist_ok=True)
    with open(os.path.join(tests_path, "__init__.py"), "w") as f:
        f.write("from your_module.module_file import some_function")

    # Create the data directory if it doesn't exist
    data_path = os.path.join(project_path, "data")
    os.makedirs(data_path, exist_ok=True)

    # Create 'test_data' and 'live_data' folders within 'data'
    os.makedirs(os.path.join(data_path, "test_data"), exist_ok=True)
    os.makedirs(os.path.join(data_path, "live_data"), exist_ok=True)

    # Create an 'archive' folder within 'data'
    os.makedirs(os.path.join(data_path, "archive"), exist_ok=True)

    # Create the main script if it doesn't exist
    main_script_path = os.path.join(project_path, "main_script.py")
    with open(main_script_path, "w") as f:
        f.write("print('Hello from main_script!')")

    # Create README.md if it doesn't exist
    readme_path = os.path.join(project_path, "README.md")
    with open(readme_path, "w") as f:
        f.write("# Your Project\n\nThis is a description of your project.")

    # Create requirements.txt if it doesn't exist
    requirements_path = os.path.join(project_path, "requirements.txt")
    open(requirements_path, "w").close()


if __name__ == "__main__":
    create_project_structure(project_name="FandF", root_location=".")
