
from collections import defaultdict
import json
import sqlite3
import typer
import joblib

# Connect to SQLite database
conn = sqlite3.connect('codepeak_ag.db')
cursor = conn.cursor()

table_name="method_frequency"

# Fetch methods from the database table
cursor.execute(f"SELECT * FROM {table_name}")
frequency_table = cursor.fetchall()

# Remove header row
header = frequency_table[0]
data = frequency_table[1:]

# Create list of dictionaries
method_frequency = []
for row in data:
    module_name = row[0]
    if(module_name=="Grand Total"):
        continue 
    frequency = int(row[1].replace(',', ''))  # Remove commas and convert to int
    method_frequency.append({'module': module_name, 'SUM of frequency': frequency})



#loading files..
with open('methods_by_category.json', 'r') as file:
        methods_by_category = json.load(file)
with open('unsupported_methods.json', 'r') as file:
        unsupported_methods = json.load(file)
with open('supported_methods.json', 'r') as file:
        suppported_methods = json.load(file)


# Define the custom_tokenizer function
def custom_tokenizer(x):
    return x.split('.')

def load_model():
    # Load the model
    return joblib.load('classification_trained_model.joblib')


def top_libraries_per_category(method_frequency, categories):
    # Create a dictionary to store libraries per category
    libraries_per_category = defaultdict(list)

    # Group modules by category
    for category, category_methods in categories.items():
        # Use a set to store unique modules for this category
        unique_modules = set()

        # Filter modules by category (allowing partial matches)
        for entry in method_frequency:
            for method in category_methods:
                if entry['module'] in method:
                    unique_modules.add(entry['module'])

        # Sort unique modules by frequency
        sorted_modules = sorted(
            unique_modules,
            key=lambda module: next((x['SUM of frequency'] for x in method_frequency if x['module'] == module), 0),
            reverse=True
        )[:5]

        # Add top 5 unique modules to the category list
        libraries_per_category[category] = sorted_modules

    return libraries_per_category


app = typer.Typer()
import numpy as np
@app.command()
# Function to generate report for top 5 libraries in a category
def generate_report():
    # Implement logic to generate the report based on category, additional data, and exclusion list
    result = top_libraries_per_category(method_frequency, methods_by_category)
    typer.echo(f"Generating report...")
    for category in result:
        print(f"{category}:")
        for method in result[category]:
            print(method)
        print()
    

@app.command()
def filter_unsupported_libraries():
    # Logic to filter out libraries already supported by Antigranular
    typer.echo("Filtering unsupported libraries..")
    print(unsupported_methods)


@app.command()
def exclude_methods(excluded_methods: str):
    # Split the excluded_methods string into a list
    excluded_methods_list = excluded_methods.split(',')

    # Remove specified methods from the methods_by_category
    for category, methods in methods_by_category.items():
        methods_by_category[category] = [method for method in methods if method not in excluded_methods_list]

    # Remove excluded methods from the unsupported methods 
    unsupported_methods[:] = [method for method in unsupported_methods if method not in excluded_methods_list]

    # Remove excluded methods from the frequency table
    method_frequency[:] = [entry for entry in method_frequency if entry['module'] not in excluded_methods_list]

    typer.echo(f"Excluded methods: {excluded_methods_list}")

@app.command()
def include_methods(included_methods: str):
    # Split the excluded_methods string into a list
    included_methods_list = included_methods.split(',')

    model=load_model()
    predicted_categories= model.predict(included_methods_list)


    for method, category in zip(included_methods_list, predicted_categories):
        methods_by_category[category].append(method)

    for method in included_methods_list:
        if method not in suppported_methods:
            unsupported_methods.append(method)
    
    typer.echo(f"Included methods: {included_methods_list}")

    



# CLI commands for different functionalities
app.command()(generate_report)
app.command()(filter_unsupported_libraries)
app.command()(exclude_methods)
app.command()(include_methods)


if __name__ == "__main__":
    app()
