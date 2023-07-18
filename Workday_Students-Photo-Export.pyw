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
PATH_TO_LOCAL_STORAGE_FOLDER_FOR_IMAGE_FILES = f"C:\PATH\TO\PROFILE\PHOTOS\STUDENT" #Absolute path to the local folder where the Student profile images should be stored.
URL_TO_CR_Students_Profile_Photos = "" # URL to Worday RaaS report "CR_Students_Profile_Photos" (JSON format).

# You ***MUST REPLACE*** the "?Student%21WID=" URL parameter with "?Student%21Student_ID={}" for the batch process to work.
URL_TO_CR_Students_Profile_Photos_with_Base64_Image_Data = "" # URL to Workday RaaS report "CR_Students_Profile_Photos_with_Base64_Image_Data" (JSON format)

batch_size = 20 # The number of IDs to process at a time. Since Base64 Image Data is often VERY large for each record, a number no more than 20 is recommended.
    
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
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING) 
    # Creating an object
    logger.warning("Photo Export started")

    url_sudents = URL_TO_CR_Students_Profile_Photos
    # Cedentials to access the report with
    username = env_vars['WORKDAY_RaaS_User_Username']
    password = env_vars['WORKDAY_RaaS_User_Password']
    
    stuIDs = []
    
    # Function to process the URL with the list of IDs appended
    def process_url(stu_ids):
        url_template = URL_TO_CR_Students_Profile_Photos_with_Base64_Image_Data
        url = url_template.format("!".join(stu_ids))
        print(url)
        try:
            response_student_photos = requests.get(url, auth=(username, password))
            data_stu_photos = response_student_photos.json()
            if response_student_photos.status_code != 200:
                alertMessage = "IntSys: Student Photos - Failed to connect to webservice report for Base64 Photo data."
                logger.error(alertMessage)
        except BaseException as e:
            alertMessage = "ERROR: Student Photos - GET photo data failed - %s"%(e)
            logger.error(alertMessage)

        # Extracting relevant data            
        for student in data_stu_photos['Report_Entry']:
            student_id = student.get("Student_ID","")
            attachment_content = str(student.get("attachmentContent",""))
            # Decoding Base64 and saving as PNG file
            image_data = base64.b64decode(attachment_content)
            image = Image.open(BytesIO(image_data))
            image.save(f"{PATH_TO_LOCAL_STORAGE_FOLDER_FOR_IMAGE_FILES}{student_id}.png")
    
    
    try:
        response_students = requests.get(url_sudents, auth=(username, password))
        data_students = response_students.json()
        if response_students.status_code != 200:
            alertMessage = "IntSys: Students List - Failed to connect to webservice report."
            logger.error(alertMessage)
    except BaseException as e:
        alertMessage = "ERROR: Students List - GET report data failed - %s"%(e)
        logger.error(alertMessage)
        
    for student in data_students['Report_Entry']:
        stuIDs.append(student["Student_ID"])

        if len(stuIDs) == batch_size:
            process_url(stuIDs)
            stuIDs = []

    # Process any remaining IDs that didn't form a full batch
    if stuIDs:
        process_url(stuIDs)
        

if __name__ == "__main__":
    setup_logger()
    main()
