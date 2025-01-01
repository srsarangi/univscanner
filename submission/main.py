import os
import re
import subprocess
import csv

# import csv

# Define the output CSV file
# combined_csv = "combined.csv"

# # Create the CSV file with headers
# with open(combined_csv, mode="w", newline="") as file:
#     writer = csv.writer(file)
#     # Write headers
#     writer.writerow(["University Name", "Country", "Professor Name", "Email", "Link"])
#     print(f"{combined_csv} created with the required headers.")

# Define the directory where the files are located
directory = "./"

# Output CSV file for errors
error_csv = "error.csv"

# Function to extract the number from the filename
def extract_number(filename):
    match = re.match(r"(\d+)_.*\.py$", filename)
    return int(match.group(1)) if match else None

# List all files in the directory
files = os.listdir(directory)

# Filter and sort files based on the number
filtered_files = sorted(
    (f for f in files if f.endswith(".py") and (num := extract_number(f)) is not None and num >= 500),
    key=lambda f: extract_number(f)
)

# Prepare error CSV
with open(error_csv, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["File Name"])  # Write header

    # Execute each Python file with error handling
    for py_file in filtered_files:
        filepath = os.path.join(directory, py_file)
        try:
            print(f"Running {py_file}...")
            subprocess.run(["python3", filepath], check=True)
        except Exception as e:
            print(f"Error encountered with {py_file}. Logging to error.csv.")
            writer.writerow([py_file])  # Log file name to CSV