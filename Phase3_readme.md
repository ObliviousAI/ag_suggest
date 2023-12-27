# CodePeak Analysis CLI Tool

## Overview

The CodePeak Analysis CLI tool processes method frequency data stored in an SQLite database. It performs various operations such as generating reports, filtering unsupported libraries, and excluding or including specific methods from the analysis.

## Commands

- **generate_report**: Generates a report displaying the top 5 libraries in each category based on method frequency.

- **filter_unsupported_libraries**: Filters out libraries that are already supported by Antigranular.

- **exclude_methods**: Excludes specified methods from analysis and updates related data structures accordingly.

- **include_methods**: Includes specified methods, predicts their categories using a pre-trained model, and updates the analysis data.

## Functionality

### Loading Data

The tool loads method frequency data from an SQLite database and JSON files containing categorized methods and supported/unsupported methods.

### Data Processing

- Parses method frequency data.
- Groups modules by category and identifies the top libraries per category based on frequency.

### Operations

- Generates reports for top libraries in each category.
- Filters out unsupported libraries.
- Excludes or includes specified methods from analysis and updates the associated data structures.

## Usage

Execute the commands using the CLI tool:

- `python filename.py generate-report`: Generates a report for top libraries per category.
- `python filename.py filter-unsupported-libraries`: Filters unsupported libraries.
- `python filename.py exclude-methods --excluded_methods method1,method2`: Excludes specified methods.
- `python filename.py include-methods --included_methods method3,method4`: Includes specified methods.

## Dependencies

- Python 3.x
- Libraries: collections, json, sqlite3, typer, joblib, numpy

