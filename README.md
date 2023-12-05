# Methods Analysis

## Description of the problem

This technical challenge involves the analysis of a dataset obtained from a survey of Python functions and libraries used for data analysis tasks.

This challenge engages participants in a tri-fold strategy. To begin with, you will categorise and parse Python methods. Building upon that, you will identify the methods and libraries that aren’t supported by Antigranular. For the final stretch of the challenge, you will create a user-friendly command-line interface (CLI) for generating insightful reports.

The analysis will be based on data from a SQLite database containing two tables with relevant information.

## Why is this an important problem?

Well, this is an unbeatable chance for us at Antigranular to really sink our teeth into how Python methods and libraries are used in data analysis, and figure out where we need to beef up our game. We want to understand patterns, grasp stumbling blocks, and better adapt to the needs of our data analysts and researchers. Consequently, this will allow for the better integration of libraries and improve the overall responsible data analysis landscape.

## Skills you will get by building a solution

By building this solution, you will not only develop a multiphase problem-solving approach but also earn a black belt in analysing Python methods and libraries. Oh, and does working with SQLite databases, designing CLIs with tools like Typer, and catering to user requirements sound interesting? Well, these are just appetizers! The main course is drawing data-driven conclusions and implementing features that evolve with the user community’s needs.

## More Details:

The challenge is divided into 3 distinct phases:

### Phase 1

Start by segregating the methods into different categories based on their functionality. This will provide a clearer understanding of the purpose and usage of each method. 

Here are some examples of categories:

1. Exploratory Analysis Helpers:
    - `matplotlib.pyplot`: This module is commonly used for creating visualisations and plots to explore and analyse data.
2. Data Analysis - Classification:
    - `sklearn.tree.DecisionTreeRegressor`: This module is used for implementing decision tree-based regression algorithms, which are commonly used for classification tasks.

By categorising the methods, we can better understand the specific functionalities they serve in the context of data analysis. This analysis will help us uncover patterns and trends in the usage of different modules and functions.

### Phase 2

In the second phase, we will crawl the [Antigranular Documentation](https://docs.antigranular.com/) to identify unsupported methods and libraries for data analysis tasks.

This analysis will provide insights into the limitations and areas where Antigranular's functionality can be improved. These findings will guide future development and integration efforts, ensuring that Antigranular meets the evolving needs of data analysts and researchers.

### Phase 3

This is where you let your creativity shine. 🌟

To streamline the analysis process and gain valuable insights, you will contribute to developing a robust command-line interface (CLI) for this project. While Typer is the preferred tool for this purpose, you can choose any suitable tool for implementation.

The CLI will offer extensive functionality, enabling us to generate a comprehensive report on the top 5 most frequently used libraries within each of the predetermined categories. These categories will provide a clear and organised framework for understanding the purpose and usage of each method in the context of data analysis.

Moreover, the CLI will filter out libraries that Antigranular already supports, ensuring that our analysis focuses on identifying additional libraries that can enhance our data analysis capabilities further. This will help us uncover new and emerging trends in the data analysis landscape and make informed decisions regarding the integration of new libraries.

Further enhancing its flexibility, the CLI will allow users to personally tailor their analysis by excluding specified libraries. This functionality ensures that our final report accurately reflects library usage preferences.

Another feature of the CLI is its ability to integrate additional data into the methods table. By considering user-provided information, we can enrich our analysis, thus enhancing the overall accuracy and comprehensiveness of our findings.

Lastly, the CLI will reveal the degree of coverage that Antigranular provides for various functions. This insight is crucial in evaluating how closely Antigranular aligns with the needs and requirements of data analysts. Consequently, we can strategise areas for improvement, ensuring Antigranular's place as a cutting-edge tool in the fast-evolving field of data science.

## Dataset

For this analysis, we have access to a SQLite database that contains two tables, which hold the relevant data for our research.

### Methods Table

The **methods** table in the dataset contains the following columns:

- **identifier**: This column contains the identifier of the person who gave the survey. The identifier has been masked to protect their identity.
- **methods**: This column contains the methods used for data analysis, in the format of `"library_name.module_name.function_name"`.

The data in this table provides information about the specific methods used by participants for data analysis tasks.

**Snippet of the data**:

| identifier | methods |
| --- | --- |
| n_2 | {'pandas,read_csv', 'pandas,head', 'pandas,DataFrame', 'pandas,Series', 'pandas,set_option'} |
| n_24 | {'pandas,read_csv', 'pandas,head', 'learntools.core,binder.bind', 'seaborn,distplot', 'seaborn,kdeplot'} |
| n_17 | set() |

<aside>
💡 `set()` means that the data given was irrelevant or wrong

</aside>

### Method Frequency Table

Now, participants were requested to create a Jupyter notebook utilising the functions they provided in the methods table. This table contains information about the usage of specific modules in their notebooks.

The **method_frequency** table contains the following columns:

- **module**: This column contains the name of the module used in the Jupyter notebooks.
- **frequency**: This column indicates the total number of times a particular module appears across all notebooks.
- **method**: This column records the number of notebooks in which a specific module is present.

| module | SUM of frequency | COUNTUNIQUE of method |
| --- | --- | --- |
| matplotlib.pyplot | 100,578 | 219 |
| pandas | 84,840 | 320 |
| numpy | 33,427 | 361 |
| seaborn | 21,676 | 125 |
| tensorflow.keras.models | 9,816 | 115 |
