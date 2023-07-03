#Author: @signalSurfer
#7.3.23
#v0.1
#Pushbullet API dox: https://pypi.org/project/pushbullet.py/0.9.1/

import os
import csv
import shutil
import filecmp
from pushbullet import Pushbullet 

shared_folder_path = "path_to_share"
local_folder_path = "path_to_local_working_dir"
csv_filename = "csv_File_Name.csv"
pb = Pushbullet("o.APIKEY")

# Check if the CSV file exists in the shared folder
csv_file_path = os.path.join(shared_folder_path, csv_filename)
if not os.path.isfile(csv_file_path):
    print(f"CSV file '{csv_filename}' not found in the shared folder.")
    exit(1)
print("shared file found.")
# Check if the local folder exists, create it if it doesn't
if not os.path.exists(local_folder_path):
    os.makedirs(local_folder_path)

# Check if the file in the shared folder is different from the one in the local folder
local_csv_file_path = os.path.join(local_folder_path, csv_filename)
if os.path.isfile(local_csv_file_path) and filecmp.cmp(csv_file_path, local_csv_file_path):
    print("No changes in the CSV file.")
    exit()
print("file change detected:")
# Read the CSV file and compare with the previous version
previous_csv_data = []
if os.path.isfile(local_csv_file_path):
    with open(local_csv_file_path, 'r') as file:
        reader = csv.reader(file)
        previous_csv_data = list(reader)

new_csv_data = []
with open(csv_file_path, 'r') as file:
    reader = csv.reader(file)
    new_csv_data = list(reader)

# Find the affected rows and print columns 5 and 6
affected_rows = []
for i in range(len(new_csv_data)):
    if i >= len(previous_csv_data) or new_csv_data[i] != previous_csv_data[i]:
        affected_rows.append(i)
        if len(new_csv_data[i]) >= 6:
            Title = f"{new_csv_data[i][5]} {new_csv_data[i][4]}"
            Body = f"{new_csv_data[i][3]}"
            push = pb.push_note(str(Title), str(Body))
            
# Copy the CSV file from the shared folder to the local folder
shutil.copy2(csv_file_path, local_csv_file_path)
