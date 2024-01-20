import os
import csv
import smtplib
from datetime import datetime
import shutil

def get_today_date_folder(incoming_folder):
    today_date = datetime.today().strftime('%Y%m%d')
    today_folder_path = os.path.join(incoming_folder, today_date)

    if os.path.exists(today_folder_path):
        return today_folder_path
    else:
        print(f"No folder found for today's date: {today_date}")
        return None

def read_and_validate_orders(csv_filename, product_master_filename):
    product_master = load_product_master(product_master_filename)

    validation_results = {'valid': [], 'invalid': []}

    with open(csv_filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for order in reader:
            # Perform validations
            is_valid, reasons = validate_order(order, product_master)
            
            if is_valid:
                validation_results['valid'].append(order)
            else:
                validation_results['invalid'].append({'order': order, 'reasons': reasons})

    return validation_results

def load_product_master(product_master_filename):
    product_master = {}
    
    with open(product_master_filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for product in reader:
            product_master[product['product_id']] = {
                'product_name': product['product_name'],
                'price': float(product['price']),
                'category': product['category']
            }

    return product_master

def validate_order(order, product_master):
    reasons = []

    # Validation 1: Product ID Check
    product_id = order.get('product_id')
    if product_id not in product_master:
        reasons.append("Product ID not found in product master")
    else:
        # Validation 2: quantity Check
        quantity = order.get('quantity')
        if quantity is not None and quantity != '':
            try:
                expected_total = product_master[product_id]['price'] * int(quantity)
                sales_amount = float(order.get('sales', 0))
                if sales_amount != expected_total:
                    reasons.append("Total sales amount mismatch")
            except ValueError:
                reasons.append("Invalid quantity or sales value")
        else:
            reasons.append("Quantity is missing or invalid")

    # Validation 3: Order Date Check
    order_date_str = order.get('order_date')
    if order_date_str:
        order_date = datetime.strptime(order_date_str, '%Y-%m-%d')
        if order_date > datetime.today():
            reasons.append("Order date is in the future")
    else:
        reasons.append("Order date is missing or invalid")

    # Validation 4: Non-Empty Fields Check
    for field in order:
        if not order[field]:
            reasons.append(f"Empty field '{field}'")

    # Validation 5: Location Check
    city_value = order.get('city')
    if city_value:
        cleaned_city = city_value.strip()  # Strip leading and trailing spaces
        allowed_locations = ['Mumbai', 'Bangalore']
        if cleaned_city not in allowed_locations:
            reasons.append("Invalid location")
    else:
        reasons.append("City is missing or invalid")

    # All validations passed
    is_valid = len(reasons) == 0
    return is_valid, reasons

def send_validation_email(total_files, successful_files, rejected_files):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'kj.python.learning@gmail.com'
    smtp_password = 'yzjh nraf kfky ucdc'  

    business_email = 'kaushaljoshi100@gmail.com'

    subject = f"Validation Email {datetime.today().strftime('%Y-%m-%d')}"
    body = f"Total {total_files} incoming files, {successful_files} successful files, and {rejected_files} rejected files for today."

    # Create the email message
    message = f"Subject: {subject}\n\n{body}"

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)

        server.sendmail(smtp_username, business_email, message)

    print('Validation mail sent')

def process_files():
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
                    shutil.copy(csv_filepath, rejected_filepath)

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
                    shutil.copy(csv_filepath, success_filepath)

                    print(f"File '{filename}' copied to 'success_files'.")

        send_validation_email(total_files, successful_files, rejected_files)
    else:
        print("Exiting script.")

if __name__ == "__main__":
    process_files()
