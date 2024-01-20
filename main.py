# main.py
from packages.file_processor import process_files

if __name__ == "__main__":

    #Hardcoding the source folder and product_master file name but this can be made dynamic as well by accepting the input from user if ETL folder location changes in future
    incoming_folder = "incoming_files"
    product_master_filename = "product_master.csv"

    #invoking the process_files method that will invoke multiple functions to perform required ETL and send validation mail as well
    process_files(incoming_folder,product_master_filename)
