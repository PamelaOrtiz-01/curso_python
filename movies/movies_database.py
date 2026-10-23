""" Database operations for the movies app. """
import os
import csv

def load_csv_data(file_path):
    """Load data from a CSV file and return it as a list of dictionaries."""
    data = []
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data