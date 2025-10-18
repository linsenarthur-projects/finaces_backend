import pandas as pd

from sqlalchemy import create_engine
from datetime import date

from app.src.controller import process_csv_and_save_to_db, process_csv_and_save_to_dbx

print("Starting CSV processing...")
file_path = "data/00_zichtrekening.csv"
# process_csv_and_save_to_db(file_path)
process_csv_and_save_to_dbx(file_path)