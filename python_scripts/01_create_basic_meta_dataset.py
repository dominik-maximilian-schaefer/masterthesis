from pathlib import Path
import pandas as pd
from collections import Counter
import random


# Used for Demo Values
def clean_value_strip(value):
    return str(value).strip()


# Used for Column-Headers
def clean_value_strip_lowercase(value):
    return str(value).strip().lower()


# Import all CSV files from given directory, exctract the header, count their occurence, sort descending and save .csv file
def count_headers(directory_path: str, output_file: str):
    header_counter = Counter()
    csv_files = Path(directory_path).glob('*.csv')

    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file, delimiter=';')
            headers = [clean_value_strip_lowercase(header) for header in df.columns.tolist()]
            header_counter.update(headers)
        except pd.errors.ParserError as e:
            print(f"Error! Reading {csv_file.name}: {e}")

    header_df = pd.DataFrame(header_counter.items(), columns=['original_column', 'nr_of_occurrences'])
    header_df = header_df.sort_values(by='nr_of_occurrences', ascending=False)
    header_df.to_csv(output_file, sep=';', index=False)


# Adds Demo Values found in each csv to final data frame
def add_demo_values(output_file: str, search_directory: str):
    df = pd.read_csv(output_file, delimiter=';')

    if 'demo_values' not in df.columns:
        df['demo_values'] = None

    for index, row in df.iterrows():
        header_value = row['original_column']

        csv_files = Path(search_directory).glob('*.csv')

        demo_values = []

        for csv_file in csv_files:
            try:
                search_df = pd.read_csv(csv_file, delimiter=';')
                search_df.columns = [clean_value_strip_lowercase(col) for col in search_df.columns]

                if header_value in search_df.columns:
                    valid_values = list(set(search_df[header_value].dropna().apply(clean_value_strip).tolist()))
                    if len(valid_values) > 3:
                        selected_values = random.sample(valid_values, 3)
                    elif len(valid_values) <= 3 and len(valid_values) > 0:
                        selected_values = valid_values
                    else:
                        selected_values = [None]
                    demo_values.extend(selected_values)
            except pd.errors.ParserError as e:
                print(f"Error reading {csv_file.name}: {e}")

        if demo_values:
            df.at[index, 'demo_values'] = ','.join(map(str, demo_values))

    df.to_csv(output_file, sep=';', index=False)


# Removes all "none" or similar demo values
def clean_demo_values(csv_file_path):
    df = pd.read_csv(csv_file_path, delimiter=';')

    df['demo_values'] = df['demo_values'].astype(str)

    def clean_and_check(demo_values):
        if pd.isna(demo_values):
            return "EMPTY"

        values = demo_values.split(',')
        cleaned_values = [value.strip() for value in values if value.strip().lower() not in ["none", "nan", "0", "x"]]
        if not cleaned_values:
            return "EMPTY"
        else:
            return cleaned_values

    df['demo_values'] = df['demo_values'].apply(clean_and_check)

    df.to_csv(csv_file_path, index=False, sep=';')


# Depict exactly 3 demo values
def process_demo_values(csv_file_path):
    df = pd.read_csv(csv_file_path, delimiter=';')
    df['demo_values'] = df['demo_values'].astype(str)

    def clean_value(value):
        value = value.strip("[]")
        return value

    def select_three_unique(demo_values):
        if pd.isna(demo_values):
            return demo_values

        values = [clean_value(v) for v in demo_values.split(',')]
        unique_values = list(set(values))

        if len(unique_values) < 3:
            while len(unique_values) < 3:
                unique_values.append(random.choice(unique_values))

        selected_values = unique_values[:3]

        if 'EMPTY' in selected_values:
            selected_values = ["EMPTY"]

        return ','.join(selected_values)

    df['demo_values'] = df['demo_values'].apply(select_three_unique)
    df.to_csv(csv_file_path, index=False, sep=';')


if __name__ == "__main__":
    # Set directory and output_file
    directory = 'directory_containing_all_csv_files'
    output_file = 'meta-dataset'
    with open(output_file, 'w') as file:
        pass

    # Count headers and create first file
    count_headers(directory, output_file)

    # Add Demo Values
    add_demo_values(output_file, directory)

    # Clean Demo Values
    clean_demo_values(output_file)

    # Extract exactly three demo values
    process_demo_values(output_file)

    print("Script finished")
