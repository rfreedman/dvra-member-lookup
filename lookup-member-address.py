#!/usr/bin/env python3

import os
import sys
import pandas as pd
import pyperclip
from pathlib import Path

file_name ='spreadsheet.xlsx'
file_path = Path(file_name)

def ensure_spreadsheet_exists():
    if file_path.is_file() == False or os.access(file_path, os.R_OK) == False:
        print(f"Error: file '{file_name}' does not exist or is not readable")  
        sys.exit(1)  

def get_search_term():
    if len(sys.argv) < 2:
        print("Error: Missing search term.")
        print("Usage: python lookup-member-address.py <search_term>")
        sys.exit(1)
    return sys.argv[1]

def load_excel_file(file_name):
    return pd.read_excel(io=file_name, nrows=250)

def format_result(name_and_call, address):
        [name, call] = name_and_call.split('|')
        [last, first] = name.split(',')
        return f"{first.strip().title()} {last.strip().title()}\n{address}\n"

def search(search_term):
    # Load the Excel file into a pandas dataframe - limit the number of rows read
    ensure_spreadsheet_exists()
    df = load_excel_file('spreadsheet.xlsx')

    # Set search parameters
    column_number = 0  # 0 is the first data column (Column A)

    # Perform partial match lookup
    # case=False makes the search case-insensitive; na=False ignores empty cells
    condition = df.iloc[:, column_number].astype(str).str.contains(search_term, case=False, na=False)
    return df[condition]

def output_result(result_df, search_term):
    if not result_df.empty:
        name_column_name = result_df.columns[0]
        address_column_name = "Address"
        selected_columns = [name_column_name, address_column_name]

        unique_count = result_df[address_column_name].nunique()

        print()

        if unique_count == 1:
            name_and_call = result_df[name_column_name].iloc[0]
            address = result_df[address_column_name].iloc[0]

            result = format_result(name_and_call, address)
            pyperclip.copy(result)
            print(result)

        else:
            print("multiple non-unique matches:\n")
            for row in result_df[[name_column_name, address_column_name]].itertuples(index=False):
                result = format_result(row[0], row[1])
                print(result)
        print()
    else:
        print(f"No partial match found for '{search_term}'")


def main():
    search_term = get_search_term()
    df_result = search(search_term)
    output_result(df_result, search_term)

if __name__ == "__main__":
    main()