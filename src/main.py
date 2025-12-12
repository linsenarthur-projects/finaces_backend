import pandas as pd

from datetime import date

from controller import process_csv_and_save_to_db

print("Starting CSV processing...")
file_path = "data/00_zichtrekening.csv"
# process_csv_and_save_to_db(file_path)