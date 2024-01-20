# order_processing/order_validator.py
import csv
from datetime import datetime

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