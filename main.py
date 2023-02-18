import os
import pandas as pd
from datetime import datetime

# parse config file
with open("config.txt", "r") as f:
    config = dict(line.strip().split("=") for line in f)

search_directory = config["Search_Directory"]
output_directory = config["Output_Directory"]
search_keywords = [keyword.strip().lower() for keyword in config["Search_Keywords"].split(",")]
search_columns = [int(column) - 1 for column in config["Search_Columns"].split(",")]
output_file = config["OutputFile"]

# get list of CSV files in search directory
csv_files = [filename for filename in os.listdir(search_directory) if filename.endswith(".csv")]

# loop through CSV files
result_df = pd.DataFrame()
for csv_file in csv_files:
    # read CSV file into dataframe and convert column names to lowercase
    df = pd.read_csv(os.path.join(search_directory, csv_file))
    df.columns = [column.lower() for column in df.columns]

    # loop through rows in dataframe
    for index, row in df.iterrows():
        # search for match in search columns and with search keywords
        match_column = None
        match_keyword = None
        for column in search_columns:
            if match_column:
                break
            for keyword in search_keywords:
                if keyword in str(row.iloc[column]).lower():
                    match_column = df.columns[column]
                    match_keyword = keyword
                    break

        # if match found, add matched column and keyword to row and append to result dataframe
        if match_column:
            row = pd.concat([pd.Series([match_column, match_keyword]), row])
            result_df = result_df.append(row, ignore_index=True)

# write result dataframe to CSV file with timestamp
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
output_filename = output_file + "_" + timestamp + ".csv"
result_df.to_csv(os.path.join(output_directory, output_filename), index=False)