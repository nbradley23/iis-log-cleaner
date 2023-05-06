import os
import time
import zipfile
from datetime import datetime

total_deleted = 0
total_zipped = 0

def zip_logs():

    global total_deleted
    total_deleted = 0
    global total_zipped
    total_zipped = 0

    while True:
        path = input('\nPLEASE ENTER FULL FILE PATH CONTAINING LOGS TO BE ZIPPED (EXAMPLE: F:\\logfiles or F:\\logfiles\\W3SVC8): ').lower()
        # if path[0:10] == 'f:\\logfile':
        if path:
            break

    while True:
        days_back_to_delete = int(input('\nDELETE FILES OLDER THAN HOW MANY DAYS? (90 DAYS FOR PCI, CANNOT GO LESS THAN 30 DAYS): ')) + 1
        if days_back_to_delete >= 30:
            break

    def get_old_files_recursively(path):
        old_file_list = []
        current_time = time.time()
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                #Converting date in filename to date usable to compare with current time 
                log_create_date = '20' + file[4:6] + '-' + file[6:8] + '-' + file[8:10]
                create_date_converted =  int(datetime.strptime(log_create_date, '%Y-%m-%d').timestamp())
                #Check if file is old enough to be deleted
                if current_time - create_date_converted > days_back_to_delete*24*60*60:
                    old_file_list.append(file_path)
        return old_file_list
    
    def delete_old_files (files_to_deleted):
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
                #Converting date in filename to date usable to compare with current time 
                log_create_date = '20' + file[4:6] + '-' + file[6:8] + '-' + file[8:10]
                create_date_converted =  int(datetime.strptime(log_create_date, '%Y-%m-%d').timestamp())
                #Check if file is older than 1 day and if so add to zip file list
                if current_time - create_date_converted > 24*60*60 and file_path.split('.')[-1] != 'zip':
                    zip_file_list.append(file_path)
        return zip_file_list

    def zip_files_remove_original(files_to_zip):
        for file_path in files_to_zip:
            # Create a zip file with the same name as the original file
            zip_file_path = file_path.replace('.log','.zip')
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

    print(f'\n========== TOTAL FILES DELETED: {total_deleted} ==========\n')
    print(f'========== TOTAL FILES ZIPPED: {total_zipped} ==========\n')

def run_again():
    while True:
        run_again = input('WOULD YOU LIKE TO RUN SCRIPT AGAIN ON ANOTHER PATH? (YES/NO): ').lower()
        if run_again == 'yes':
            zip_logs()
        else:
            break



print('\n==================================== IIS LOG CLEANER & ZIPPER ====================================\n')
print('***SCRIPT WILL PERMENATELY DELETE ANY LOGS THAT HAVE A CREATION DATE OLDER THAN THE NUMBER OF DAYS YOU SPECIFY***\n')
print('***SCRIPT WILL THEN ZIP ANY LOGS THAT WERE CREATED MORE THAN 1 DAY AGO***\n')
print('***SCRIPT WORKS RECURSIVELY SO YOU CAN USE THE TOP LEVEL LOGFILES FOLDER (EX. F:\logfiles) AND EACH SUBFOLDER WILL BE CLEANED*** \n\n***YOU CAN ALSO SPECIFY ONE SPECIFIC SITES FOLDER (EX. F:\logfiles\W3SVC8) AND IT WILL ONLY CLEAN THAT FOLDER***\n')
print('***PLEASE ENSURE THE DESIRED PATH IS CORRECT***\n')
print('***PRESS CTRL+C AT ANYTIME TO EXIT SCRIPT***\n')

while True:
    confirmation = input("I UNDERSTAND (YES/NO): ").lower()
    if confirmation == 'yes':
        zip_logs()
        run_again()
        break
    else:
        break



