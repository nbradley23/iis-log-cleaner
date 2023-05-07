import os
import time
import zipfile
import re
from datetime import datetime

total_deleted = 0
total_zipped = 0
total_skipped = 0


def zip_logs():

    global total_deleted
    total_deleted = 0

    global total_zipped
    total_zipped = 0

    global total_skipped
    total_skipped = 0

    skipped_file_list = []

    while True:
        path = input(
            '\nPLEASE ENTER FULL FILE PATH CONTAINING LOGS TO BE ZIPPED (EXAMPLE: F:\\logfiles or F:\\logfiles\\W3SVC8): ').lower()
        # if path[0:10] == 'f:\\logfile':
        if path:
            break

    while True:
        days_back_to_delete = int(input(
            '\nDELETE FILES OLDER THAN HOW MANY DAYS? (90 DAYS FOR PCI, CANNOT GO LESS THAN 30 DAYS): ')) + 1
        if days_back_to_delete >= 30:
            break

    print('\n')

    def get_old_files_recursively(path):
        old_file_list = []
        current_time = time.time()
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                # Use regex to check if file is IIS log
                if re.search('u_ex[0-9]+\.log', file_path.split('\\')[-1]):
                    # Converting date in filename to date usable to compare with current time
                    log_create_date = '20' + \
                        file[4:6] + '-' + file[6:8] + '-' + file[8:10]
                    create_date_converted = int(datetime.strptime(
                        log_create_date, '%Y-%m-%d').timestamp())
                    # Check if file is old enough to be deleted
                    if current_time - create_date_converted > days_back_to_delete*24*60*60:
                        old_file_list.append(file_path)
                else:
                    if file_path.split('.')[-1] != 'zip':
                        skipped_file_list.append(file_path)
                        global total_skipped
                        total_skipped += 1
        return old_file_list

    def delete_old_files(files_to_deleted):
        for file in files_to_deleted:
            os.remove(file)
            global total_deleted
            total_deleted += 1
            print(f'DELETED: {file}')

    def get_files_to_zip_recursively(path):
        zip_file_list = []
        current_time = time.time()
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                # Use regex to check if file is IIS log
                if re.search('u_ex[0-9]+\.log', file_path.split('\\')[-1]):
                    # Converting date in filename to date usable to compare with current time
                    log_create_date = '20' + \
                        file[4:6] + '-' + file[6:8] + '-' + file[8:10]
                    create_date_converted = int(datetime.strptime(
                        log_create_date, '%Y-%m-%d').timestamp())
                    # Check if file is older than 1 day and if so add to zip file list
                    if current_time - create_date_converted > 24*60*60 and file_path.split('.')[-1] != 'zip':
                        zip_file_list.append(file_path)
                # else:
                #     print(
                #         f'ZIP OPERATION SKIPPED, NOT AN IIS LOG: {file_path} ')
        return zip_file_list

    def zip_files_remove_original(files_to_zip):
        for file_path in files_to_zip:
            # Create a zip file with the same name as the original file
            zip_file_path = file_path.replace('.log', '.zip')
            with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Add the original file to the zip archive
                zip_file.write(file_path, os.path.basename(file_path))
            # Delete the original file
            os.remove(file_path)
            global total_zipped
            total_zipped += 1
            print(f'ZIPPED: {file_path}')

    old_file_list = get_old_files_recursively(path)
    delete_old_files(old_file_list)

    zip_file_list = get_files_to_zip_recursively(path)
    zip_files_remove_original(zip_file_list)

    for file_path in skipped_file_list:
        print(
            f'DELETE & ZIP OPERATIONS SKIPPED, FILE NOT AN IIS LOG FILE: {file_path}')

    print(f'''\n    ========== TOTAL FILES DELETED: {total_deleted} ==========
    ========== TOTAL FILES ZIPPED: {total_zipped} ==========
    ========== TOTAL FILES SKIPPED: {total_skipped} ==========\n''')


def run_again():
    while True:
        run_again = input(
            'WOULD YOU LIKE TO RUN SCRIPT AGAIN ON ANOTHER PATH? (YES/NO): ').lower()
        if run_again == 'yes':
            zip_logs()
        else:
            break


print("""
**************************************************************************************************
                                     IIS LOG CLEANER & ZIPPER 
                                         By: Nick Bradley       
**************************************************************************************************

**SCRIPT FUNCTIONALITY**
- Permanently deletes logs older than the user-specified number of days.
- Zips logs created more than 1 day ago.
- Skips any files that do not match the IIS log naming convention.
- Works recursively on subfolders if top level LogFiles folder is specified.
- Zip function will automatically skip already zipped log files.

**USAGE**
- To clean all site folders in one run, use the top-level logfiles folder (e.g., F:\logfiles) 
- To clean only one site folder at a time, specify the specific site folder (e.g., F:\logfiles\W3SVC8) 

**IMPORTANT**
- Will only work on Windows IIS logs
- Ensure the desired path is correct before running the script.
- Press Ctrl+C at any time to exit the script.
""")

while True:
    confirmation = input("I UNDERSTAND (YES/NO): ").lower()
    if confirmation == 'yes':
        zip_logs()
        run_again()
        break
    else:
        break
