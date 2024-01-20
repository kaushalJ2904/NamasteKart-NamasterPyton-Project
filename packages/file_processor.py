# order_processing/file_processor.py
import os
import shutil
import csv
from datetime import datetime
from packages.order_validator import read_and_validate_orders, load_product_master
from packages.email_sender import send_validation_email

def get_today_date_folder(incoming_folder):
    today_date = datetime.today().strftime('%Y%m%d')
    today_folder_path = os.path.join(incoming_folder, today_date)

    if os.path.exists(today_folder_path):
        return today_folder_path
    else:
        print(f"No folder found for today's date: {today_date}")
        return None

def process_files(incoming_folder, product_master_filename):
    incoming_folder = "incoming_files"
    product_master_filename = "product_master.csv"

    today_folder = get_today_date_folder(incoming_folder)

    if today_folder:
        total_files = 0
        successful_files = 0
        rejected_files = 0

        for filename in os.listdir(today_folder):
            if filename.endswith(".csv"):
                total_files += 1
                csv_filepath = os.path.join(today_folder, filename)
                validation_results = read_and_validate_orders(csv_filepath, product_master_filename)

                if validation_results['invalid']:
                    rejected_files += 1
                    # Copy to rejected_files folder
                    rejected_folder = os.path.join("rejected_files", datetime.today().strftime('%Y%m%d'))
                    os.makedirs(rejected_folder, exist_ok=True)
                    rejected_filepath = os.path.join(rejected_folder, filename)

                    #copy the rejected file to rejected folder
                    shutil.copy(csv_filepath, rejected_filepath)

                    #move the rejected file to rejected folder
                    #shutil.move(csv_filepath, rejected_filepath)

                    # Create error file
                    error_filepath = os.path.join(rejected_folder, f"error_{filename}")
                    with open(error_filepath, 'w', newline='') as csvfile:
                        fieldnames = ['order_id', 'order_date', 'product_id', 'quantity', 'sales', 'city', 'reasons']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()

                        for invalid_order in validation_results['invalid']:
                            writer.writerow({
                                'order_id': invalid_order['order']['order_id'],
                                'order_date': invalid_order['order']['order_date'],
                                'product_id': invalid_order['order']['product_id'],
                                'quantity': invalid_order['order']['quantity'],
                                'sales': invalid_order['order']['sales'],
                                'city': invalid_order['order']['city'],
                                'reasons': '; '.join(invalid_order['reasons'])
                            })

                    print(f"File '{filename}' copied to 'rejected_files' with error file created.")
                else:
                    successful_files += 1
                    # Copy to success_files folder
                    success_folder = os.path.join("success_files", datetime.today().strftime('%Y%m%d'))
                    os.makedirs(success_folder, exist_ok=True)
                    success_filepath = os.path.join(success_folder, filename)

                    #Copy the success file to success folder
                    shutil.copy(csv_filepath, success_filepath)

                    #move the success file to success folder
                    #shutil.move(csv_filepath, success_filepath)


                    print(f"File '{filename}' copied to 'success_files'.")

        send_validation_email(total_files, successful_files, rejected_files)
    else:
        print("Exiting script.")
