# Exercises.py by Julie C. Mitchell
# Copyright 2025, MIT open source license
#
# To run this program, you need two input files:
#
#       Exercises.csv is a CSV file containing information about your exercises
#
#       Exercises.json is a JSON file that specifies how many of each type of
#       exercise you want and what equipment you have available.
#
# Use this command:
#       python3 script.py Exercises.csv Exercises.json
#
# You may need to execute the following code first, to install dependencies:
#       pip3 -install pandas
#


import pandas as pd
import sys
import json
import random

# Read CSV file for exercises
def read_csv_with_headers(file_path):
    df = pd.read_csv(file_path)  # Set first column as row index
    return df
 
# Read JSON file for job parameters
def read_json_file(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    return data

# Filter CSV file based on equipment
def filter_csv_by_equipment(df, json_data):
    equipment = json_data.get("Equipment", {})
    for eq in ["Bench", "Rack"]:
        has_eq = equipment.get(eq, 0)
        if has_eq == "No":
            df = df[df["Bench"] != eq]

    for eq in ["Kettlebell", "Dumbbell"]:
        has_eq = equipment.get(eq, 0)
        if has_eq == "No":
            df = df[df["XBell"] != eq]

    for eq in ["Circular", "Linear", "Strap"]:
        has_eq = equipment.get(eq, 0)
        if has_eq == "No":
            df = df[df["Band"] != eq]

    return df
    
# Determine the number of requested exercises in each categogy
def get_zone_exercise_count(json_data, zone):
    exercises = json_data.get("Routine", {})
    exercises_count = int(exercises.get(zone, 0))
    return exercises_count

# Select random exercises in each category
def select_random_zone_entries(df, json_data, zone):

    zone_df = df[df['Zone'] == zone]
    num_entries = get_zone_exercise_count(json_data, zone)
    if len(zone_df) > 0:
        random_selection = zone_df.sample(n=min(num_entries, len(zone_df)))
        if num_entries > 0:
            col_widths = {'Exercise':30, 'Zone': 10, 'Bench': 10, 'Band':10, 'XBell': 10, 'Weight':10, 'RepsPerSet':10}
            print()
            print("Exercises for " + zone)
            print_fixed_width(random_selection, col_widths)
        return random_selection


# Print exercise list as a fixed width table
def print_fixed_width(df, col_widths):
    for col in df.columns:
        print(f"{col:<{col_widths[col]}}", end="  ")
    print()
    for _, row in df.iterrows():
        for col in df.columns:
            print(f"{str(row[col]):<{col_widths[col]}}", end="  ")
        print()

# main
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <csv_file_path> <json_file_path>")
        sys.exit(1)
    
    csv_file_path = sys.argv[1]
    json_file_path = sys.argv[2]
    
    json_data = read_json_file(json_file_path)
    df = read_csv_with_headers(csv_file_path)
    dff = filter_csv_by_equipment(df, json_data)
    
    for zone in ["Arms", "Back", "Chest", "Glutes", "Core" "Cardio"]:
        select_random_zone_entries(dff, json_data, zone)
