import csv
import os

def write_to_csv(response_dict, csv_file, fieldnames):
    """
    Appends a dictionary as a row to the specified CSV file.

    Args:
        response_dict (dict): The dictionary containing data to write.
        csv_file (str): Path to the CSV file.
        fieldnames (list): List of column names for the CSV file.
    """
    try:
        # Check if the file exists to decide whether to write the header
        file_exists = os.path.isfile(csv_file)

        # Open the file in append mode
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()  # Write the header only if the file doesn't exist
            writer.writerow(response_dict)  # Append the data row

        print(f"Data appended to {csv_file}")
    except Exception as e:
        print(f"Error writing to CSV: {e}")