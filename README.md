# Workday Profile Image Collector

The Workday Profile Image Collector is a Python script that accesses specific Workday reports set up as Report-as-a-Service (RaaS) and collects raw Base64 image data from them. It then converts the Base64 data to image files using the Python Imaging Library (PIL) and stores those image files to a local folder.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [License](#license)
- [Contributing](#contributing)
- [Support](#support)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)

## Installation

1. Clone the repository to your local machine:
```python
git clone https://github.com/anderson-university/workday-profile-image-collector.git
cd workday-image-collector
```
2. Set up a virtual environment (optional but recommended):
```python
python -m venv venv
source venv/bin/activate # On Windows, use "venv\Scripts\activate"
```
3. Install the required dependencies:
```python
pip install -r requirements.txt
```
## Usage

1. Before running the script, make sure you have set up the necessary authentication credentials in the .env file and the correct permissions to access the Workday RaaS reports with image data.

2. Modify the varaiables at the top of the python files to specify the Workday reports you want to access, the path to the log file you want to create and use or modify, and the local folder to store the image files.

3. Run the Python file(s)

    - Ensure you have Python installed: If you don't have Python installed, download and install the latest version of Python from the official website (https://www.python.org/downloads/).

    - UNIX/MacOS:
        - Rename the file: Rename the file to change its extension from .pyw to .py.
        - Run the .py file: Open a terminal or command prompt, navigate to the directory containing the converted .py file, and execute the following command:
            ```python
            python Workday_Students-Photo-Export.py # .pwy if running in Windows
            ```
            or
            ```python
            python Workday_Employees-Photo-Export.py # .pwy if running in Windows
            ```
        This command runs the .py file using the Python interpreter and executes its code.
    
    - Windows:
        - In Windows, these files can be run either by using the command line, by double-clicking the .pyw file with the mouse, or by setting a schedule via Task Scheduler simply by pointing directly to the .pyw file in the Actions tab.
        - Open the Command Prompt: Press Win + R, type cmd, and press Enter to open the Command Prompt.
        - Navigate to the directory: Use the cd command to navigate to the directory where the .pyw file is located. For example:
            ```python
            cd C:\path\to\directory
            ```
        - Run the .pyw file: Execute the .pyw file using the Python interpreter by typing its name without the extension:
            ```python
            pythonw Workday_Students-Photo-Export.pyw
            ```
            or
            ```python
            pythonw Workday_Employees-Photo-Export.pyw
            ```
        - Press Enter: Press Enter to run the .pyw file.

    The script will fetch image data from the specified Workday reports, convert the Base64 data to image files, and save them to the local folder.

## Configuration

Configuration will be done in the two python files near the top and in the one .env file.
- `reports` : Each report should have a unique URL endpoint to access the report data.

- `local_folder` : Each file points to an absolute path to the local folder where the image files will be saved.

- `environment_variables` : The credentials of the user account in Workday by which the Workday RaaS report will be run. This account must have appropriate security permissions in Workday to access the applicable Business Objects and fields.

## License

This project is licensed under the AGPL License - see the [LICENSE.txt](LICENSE.txt) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes you would like to propose.

## Support

If you encounter any issues or have questions about using the Workday Image Collector, please feel free to [open an issue](https://github.com/anderson-university/workday-profile-image-collector/issues).

## Acknowledgements

- Thanks to the Python community for providing excellent tools and libraries.
- This project was inspired by the need to efficiently collect and store profile photos from Workday reports.

## Contact

For additional information or inquiries, you can reach out to the project maintainer at jritchie@andersonuniversity.edu (mailto:jritchie@andersonuniversity.edu).
