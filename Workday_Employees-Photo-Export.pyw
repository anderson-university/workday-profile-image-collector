import os
import requests
import base64
from PIL import Image
from io import BytesIO
import logging
from dotenv import dotenv_values

####################################################################
# Modify the below variables for your local environment

PATH_TO_ENVIRONMENT_VARIABLES_FILE = f"C:\PATH\TO\.env" # Absolute path to the ".env" file where the various secured credentials are located.
PATH_TO_LOG_FILE = f"C:\PATH\TO\LOG\FILE\****.log" #Absolute path, including the .log file name, where you want the log file to be created or found.
PATH_TO_LOCAL_STORAGE_FOLDER_FOR_IMAGE_FILES = f"C:\PATH\TO\PROFILE\PHOTOS\EMPLOYEES" #Absolute path to the local folder where the Employee profile images should be stored.
URL_TO_CR_Employees_Profile_Photos = "" # URL to Worday RaaS report "CR_Employees_Profile_Photos" (JSON format).

# You ***MUST REPLACE*** the "?Worker%21WID=" URL parameter with "?Worker%21Employee_ID={}" for the batch process to work.
URL_TO_CR_Employees_Profile_Photos_with_Base64_Image_Data = "" # URL to Workday RaaS report "CR_Employees_Profile_Photos_with_Base64_Image_Data" (JSON format)

batch_size = 20 # The number of IDs to process at a time. Since Base64 Image Data is often VERY large for each record, a number no more than 20 is recommended.
IMAGE_FILE_FORMAT = ".png" # Example formats: .png, .jpg, .gif, etc.
    
####################################################################


# Access the values of environment variables
env_vars = dotenv_values(PATH_TO_ENVIRONMENT_VARIABLES_FILE)
 
# Create and configure logger
def setup_logger():
    log_file_path = PATH_TO_LOG_FILE
    logging.basicConfig(filename=log_file_path,
                        format='%(asctime)s %(message)s',
                        filemode='a',
                        encoding='utf-8',
                        level=logging.WARNING)
    # Create the log file if it does not exist
    open(log_file_path, 'a').close()

def main(): 
    # Start logging for instance.
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING) 
    # Creating an object
    logger.warning("Photo Export started")
    
    # Set the credentials with which to access the Workday reports
    username = env_vars['WORKDAY_RaaS_User_Username']
    password = env_vars['WORKDAY_RaaS_User_Password']

    # Set the URL to collect the list of Employees who have profile photos listed in their Worker BO record.
    url_employees = URL_TO_CR_Employees_Profile_Photos
    
    # Create an empty list for the Employee IDs
    empIDs = []
    
    # Function to process the URL with the list of IDs appended
    def process_url(emp_ids):
        # Define the variable containing the link to the report with the Base64 image data.
        url_template = URL_TO_CR_Employees_Profile_Photos_with_Base64_Image_Data
        # Reformat the empIDs list sent in the function's parameter to be separated by an exclamation mark 
        # as is expected by Workday.
        url = url_template.format("!".join(emp_ids))
        # Print the url with the list of employee ids used as the report prompt.
        print(url)
        
        # Access the RaaS URL and process the JSON-formatted data returned.
        try:
            response_employee_photos = requests.get(url, auth=(username, password))
            data_emp_photos = response_employee_photos.json()
            if response_employee_photos.status_code != 200:
                alertMessage = "IntSys: Employee Photos - Failed to connect to webservice report for Base64 Photo data."
                logger.error(alertMessage)
        except BaseException as e:
            alertMessage = "ERROR: Employee Photos - GET photo data failed - %s"%(e)
            logger.error(alertMessage)

        # Loop through each returned record and extract the relevant data.            
        for employee in data_emp_photos['Report_Entry']:
            employee_id = employee.get("Employee_ID","")
            attachment_content = str(employee.get("attachmentContent",""))
            # Decode the Base64 image data and save as an image file to the desired location (variables above).
            image_data = base64.b64decode(attachment_content)
            image = Image.open(BytesIO(image_data))
            image.save(f"{PATH_TO_LOCAL_STORAGE_FOLDER_FOR_IMAGE_FILES}\{employee_id}{IMAGE_FILE_FORMAT}")
    
    # Access the Workday report to obtain a list of IDs where a photo is present in the BO record. 
    try:
        response_employees = requests.get(url_employees, auth=(username, password))
        data_employees = response_employees.json()
        if response_employees.status_code != 200:
            alertMessage = "IntSys: Employees List - Failed to connect to webservice report."
            logger.error(alertMessage)
    except BaseException as e:
        alertMessage = "ERROR: Employees List - GET report data failed - %s"%(e)
        logger.error(alertMessage)
    
    # Loop through the returned JSON-formatted data from the first report and append the Employee IDs from that
    # report to the empIDs list used to populate the Employees%21Employee_ID={} (report prompt) in the report to get 
    # the Base64 image data.    
    for employee in data_employees['Report_Entry']:
        empIDs.append(employee["Employee_ID"])
        # Once the empIDs list count reachs the defined amount (default: 20), send the list to the process_url
        # function to get the image data and save it.
        if len(empIDs) == batch_size:
            process_url(empIDs)
            empIDs = []

    # Process any remaining IDs that didn't form a full batch
    if empIDs:
        process_url(empIDs)
        

if __name__ == "__main__":
    setup_logger()
    main()
