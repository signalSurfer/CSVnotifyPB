import os
import csv
import shutil
import filecmp
from pushbullet import Pushbullet #Pushbullet API doc: https://pypi.org/project/pushbullet.py/0.9.1/

shared_folder_path = "path_to_share"
local_folder_path = "path_to_local_folder"
csv_filename = "name_of_csv.csv"
pb = Pushbullet(api_key)

# Check if the CSV file exists in the shared folder
csv_file_path = os.path.join(shared_folder_path, csv_filename)
if not os.path.isfile(csv_file_path):
    print(f"CSV file '{csv_filename}' not found in the shared folder.")
    exit(1)

# Check if the local folder exists, create it if it doesn't
if not os.path.exists(local_folder_path):
    os.makedirs(local_folder_path)

# Check if the file in the shared folder is different from the one in the local folder
local_csv_file_path = os.path.join(local_folder_path, csv_filename)
if os.path.isfile(local_csv_file_path) and filecmp.cmp(csv_file_path, local_csv_file_path):
    print("No changes in the CSV file.")
    exit()

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
            print(f"Row {i+1}: Column 5: {new_csv_data[i][4]}, Column 6: {new_csv_data[i][5]}")

# Copy the CSV file from the shared folder to the local folder
shutil.copy2(csv_file_path, local_csv_file_path)
print("CSV file copied successfully.")

# Create a new CSV file with the affected rows only
affected_csv_file_path = os.path.join(local_folder_path, "affected_data.csv")
with open(affected_csv_file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    for row_index in affected_rows:
        writer.writerow(new_csv_data[row_index])
print("Affected rows copied to 'affected_data.csv'.")

print("Pushing Affected rows csv")
with open("affected_csv_file_path", "rb") as rows:
    file_data = pb.upload_file(rows, "affected_data.csv")

push = pb.push_file(**file_data)#need to test pushing
