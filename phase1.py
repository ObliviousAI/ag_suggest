import sqlite3

# Function to retrieve table schema from SQLite database
def get_table_schema(table_name):
    conn = sqlite3.connect('codepeak_ag.db')  # Connect to the SQLite database
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info({table_name});")  # Fetch table schema
    schema = cursor.fetchall()

    # Display column names and details
    if schema:
        print("Column names and details for table:", table_name)
        for column in schema:
            print(column)
    else:
        print(f"No schema found for table {table_name}")

    conn.close()  # Close the database connection

get_table_schema('Methods')  # Display table schema for 'Methods'

# Connect to SQLite database
conn = sqlite3.connect('codepeak_ag.db')
cursor = conn.cursor()

# Fetch methods from the database table
cursor.execute("SELECT methods FROM Methods")
methods_data = cursor.fetchall()

# Close the database connection
conn.close()

# Categorize method based on predefined categories
def categorize_method(method):
    categories = {
        'Data Manipulation': ['pandas.read_csv', 'pandas.DataFrame', 'numpy.array', 'pandas.concat'],
        'Data Visualization': ['matplotlib.pyplot', 'seaborn.distplot', 'matplotlib.scatter'],
        'Machine Learning': ['sklearn.tree.DecisionTreeRegressor', 'tensorflow.keras.models'],
        'Statistics': ['scipy.stats.norm', 'statsmodels.api'],
        'Data Cleaning': ['pandas.dropna', 'pandas.fillna', 'sklearn.impute.SimpleImputer'],
        'Natural Language Processing': ['nltk.tokenize.word_tokenize', 'gensim.models.Word2Vec'],
        'Time Series Analysis': ['pandas.to_datetime', 'statsmodels.tsa.seasonal.seasonal_decompose'],
    }
    
    for category, methods in categories.items():
        if method in methods:
            return category
    
    return 'Other'  # Default category if method doesn't match predefined categories

# Process the methods data
method_sets = [eval(method[0]) for method in methods_data]  # Evaluate method strings to lists

processed_methods = []
for method_set in method_sets:
    for method in method_set:
        processed_method = method.replace(',', '.')  # Replace ',' with '.'
        processed_methods.append(processed_method)

processed_methods = list(set(processed_methods))  # Remove duplicates

categorized_methods = {}

# Categorize processed methods
for method in processed_methods:
    category = categorize_method(method)
    if category not in categorized_methods:
        categorized_methods[category] = []
    categorized_methods[category].append(method)

# Print categorized methods
for category, methods in categorized_methods.items():
    print(category + ":")
    print(methods)
