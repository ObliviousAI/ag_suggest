import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd

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



fetched_methods = [method[0].replace("'", "").replace("{", "").replace("}", "").split(", ") for method in methods_data]

flattened_methods = [method for sublist in fetched_methods for method in sublist]



flattened_methods = list(set(flattened_methods))


for i in range(len(flattened_methods)):
    flattened_methods[i] = flattened_methods[i].replace(",", ".")



# print(flattened_methods)



# Close the database connection
conn.close()

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline

categories = {
    'Exploratory Analysis Helpers': [
        'matplotlib.pyplot', 'seaborn', 'pandas', 'numpy', 'scipy', 'plotly', 'bokeh', 'statsmodels', 
        'tensorflow', 'keras', 'scikit-learn', 'nltk', 'gensim', 'wordcloud', 'networkx'
    ],
    'Data Analysis - Classification': [
        'sklearn.tree.DecisionTreeRegressor', 'sklearn.tree.DecisionTreeClassifier',
        'sklearn.ensemble.RandomForestRegressor', 'sklearn.ensemble.RandomForestClassifier',
        'sklearn.svm.SVC', 'sklearn.svm.LinearSVC', 'sklearn.linear_model.LogisticRegression',
        'xgboost.XGBClassifier', 'catboost.CatBoostClassifier', 'lightgbm.LGBMClassifier'
    ],
    'Data Analysis - Clustering': [
        'sklearn.cluster.KMeans', 'sklearn.cluster.DBSCAN', 'sklearn.cluster.AgglomerativeClustering',
        'sklearn.cluster.MiniBatchKMeans', 'sklearn.cluster.Birch', 'sklearn.cluster.MeanShift'
    ],
    'Data Preprocessing': [
        'sklearn.preprocessing.StandardScaler', 'sklearn.preprocessing.MinMaxScaler',
        'sklearn.preprocessing.OneHotEncoder', 'sklearn.preprocessing.LabelEncoder',
        'sklearn.impute.SimpleImputer', 'sklearn.decomposition.PCA', 'sklearn.feature_selection.SelectKBest'
    ],
    'Natural Language Processing': [
        'nltk.tokenize.word_tokenize', 'nltk.sentiment.SentimentIntensityAnalyzer', 
        'gensim.models.Word2Vec', 'spacy.load', 'textblob.TextBlob', 'transformers.BertTokenizer'
    ],
    'Image Processing': [
        'opencv.imread', 'opencv.cvtColor', 'skimage.io.imread', 'PIL.Image.open', 'matplotlib.pyplot.imshow',
        'tensorflow.image.resize', 'scipy.ndimage.rotate', 'scipy.ndimage.zoom'
    ],
    'Model Evaluation Metrics': [
        'sklearn.metrics.accuracy_score', 'sklearn.metrics.precision_score', 'sklearn.metrics.recall_score',
        'sklearn.metrics.f1_score', 'sklearn.metrics.confusion_matrix', 'sklearn.metrics.roc_curve',
        'sklearn.metrics.mean_squared_error', 'sklearn.metrics.r2_score'
    ],
    'Model Training and Evaluation': [
        'sklearn.model_selection.train_test_split', 'sklearn.model_selection.cross_val_score',
        'tensorflow.keras.Model.fit', 'tensorflow.keras.Model.evaluate', 'tensorflow.keras.Model.predict',
        'sklearn.pipeline.Pipeline.fit', 'sklearn.pipeline.Pipeline.predict'
    ],
    'Other': [
        'os.listdir', 'os.walk', 'time.sleep', 'random.choice', 'json.load', 'pickle.load'
    ]
}


# Combine method names from all categories
all_methods = [method for methods in categories.values() for method in methods]


labels = []

# Create labeled data
for method in all_methods:
    for category, methods in categories.items():
        if method in methods:
            labels.append(category)

# Vectorizer with specific parameters

# print(all_methods)
# print()
# print(labels)
# print()




tfidf_vectorizer = TfidfVectorizer(tokenizer=lambda x: x.split('.'), token_pattern=None)

X_train, X_test, y_train, y_test = train_test_split(all_methods, labels, test_size=0.4, random_state=42)

# tfidf_vectorizer.fit(X_train)

# # Define classifiers
svm = SVC()
rf = RandomForestClassifier()
log_reg = LogisticRegression(max_iter=10000)

# # Construct a voting classifier
voting_classifier = VotingClassifier(estimators=[('svm', svm), ('rf', rf), ('log_reg', log_reg)], voting='hard')

# # Create a pipeline
pipeline = Pipeline([('tfidf', tfidf_vectorizer), ('clf', voting_classifier)])

# # Grid search for hyperparameter optimization
param_grid = {
    'tfidf__ngram_range': [(1, 1), (1, 2)],  # Adjust ngram range
    'clf__svm__C': [1, 10, 100, 1000],  # SVM regularization parameter
    'clf__rf__n_estimators': [100, 200, 500],  # Number of trees in RF
    'clf__log_reg__C': [0.1, 1, 10, 100],  # Regularization parameter for Logistic Regression
}
# 
grid_search = GridSearchCV(pipeline, param_grid, cv=5, verbose=2, n_jobs=-1)
grid_search.fit(X_train, y_train)

# # Evaluate the best model
best_classifier = grid_search.best_estimator_
predicted = best_classifier.predict(X_test)

accuracy = accuracy_score(y_test, predicted)
print(f"Best Model Accuracy: {accuracy}")

# Assuming 'predicted' contains the predicted categories for each method in 'flattened_methods'
predicted_categories = best_classifier.predict(flattened_methods)

# Initialize a dictionary to store methods for each predicted category
methods_by_category = {category: [] for category in set(predicted_categories)}

# Group methods by their predicted categories
for method, category in zip(flattened_methods, predicted_categories):
    methods_by_category[category].append(method)

# Print methods for each category
for category, methods in methods_by_category.items():
    print(f"Category: {category}")
    print(methods)
    print()



