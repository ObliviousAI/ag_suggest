import requests
from bs4 import BeautifulSoup


# Fetch the page

url="https://docs.antigranular.com"

packageLink= '/category/packages-1'
response = requests.get(f'{url}{packageLink}')

print(f"{url}{packageLink}")

# Parse HTML content
soup = BeautifulSoup(response.text, 'html.parser')


packages_section = soup.find('section', class_='row list_eTzJ')  # Update with the actual class/id
packages = packages_section.find_all('article') if packages_section else []

# Extract href links from each package
package_links = []
for package in packages:
    link = package.find('a')['href'] if package.find('a') else None
    if link:
        package_links.append(link)

all_methods=[]

for link in package_links:

    package_name = link.rsplit('/', 1)[-1]

    package_page = requests.get(f'{url}{link}')  # Assuming the links are relative
    package_soup = BeautifulSoup(package_page.text, 'html.parser')

    if(package_name=="pandas"):
        api_reference_section = package_soup.find('h2',class_="anchor anchorWithStickyNavbar_LWe7",id="api-reference")  # Assuming 'api-reference' is the ID of the API Reference section
        library_links=[]
        if api_reference_section:
            # Find all <a> tags within the <ul> tag under API Reference
            api_reference_list = api_reference_section.find_next('ul')
            if api_reference_list:
                api_links = api_reference_list.find_all('a')
                
                # Extract and print the href attribute from each <a> tag
                for link in api_links:
                    href = link.get('href')
                    code_text = link.find('code').text.strip()  # Extract text within <code> tag

                    method_page = requests.get(f'{url}{href}')  # Visit the linked page
                    method_soup = BeautifulSoup(method_page.text, 'html.parser')

                    # Extract all_ or whatever content you're interested in from the linked page
                    methods = method_soup.find_all('h3')  # Find all <h3> tags

                    # Extract text from <h3> tags excluding text from any <a> tags inside them
                    extracted_methods = []
                    for method in methods:
                        # Exclude text from any child <a> tags within the <h3> tag
                        method_text = ''.join(method.find_all(text=True, recursive=False)).strip()
                        extracted_methods.append(method_text)
                    
                    concatenated_methods = [f"{code_text}.{method}" for method in extracted_methods]

        all_methods+=concatenated_methods

    elif(package_name=="diffprivlib"):

        extracted_methods=[]
        api_reference_section = package_soup.find('h2',class_="anchor anchorWithStickyNavbar_LWe7",id="api-reference")  # Assuming 'api-reference' is the ID of the API Reference section
        library_links=[]
        if api_reference_section:
            # Find all <a> tags within the <ul> tag under API Reference
            api_reference_list = api_reference_section.find_next('ul')
            if api_reference_list:
                api_links = api_reference_list.find_all('a')
                
                # Extract and print the href attribute from each <a> tag
                for link in api_links:
                    href = link.get('href')
                    code_text = link.find('code').text.strip()  # Extract text within <code> tag

                    method_page = requests.get(href)  # Visit the linked page
                    method_soup = BeautifulSoup(method_page.text, 'html.parser')

                    if(code_text=="op_diffprivlib.tools"):
                        # Find all dt elements with the specified class
                        dt_elements = method_soup.find_all('dt', class_='sig sig-object py')
                        # Initialize an empty list to store the extracted texts
                        # Loop through each dt element and extract the desired text
                        for dt_element in dt_elements:
                            prename= dt_element.find('span', class_='sig-prename descclassname')
                            prename_text=prename.text.strip()
                            name_text = dt_element.find('span', class_='sig-name descname').text.strip()
                            # Join the extracted texts and append to the list
                            joined_text = f"{prename_text}{name_text}"
                            extracted_methods.append(joined_text)
                    else:
                        class_elements = method_soup.find_all('dl', class_='py class')
                        for class_element in class_elements:
                            classname=class_element.find('span', class_='sig-prename descclassname').text.strip()
                            classname+=class_element.find('span',class_="sig-name descname").text.strip()
                            class_methods=class_element.find_all('span',class_="sig-name descname")
                            class_methods = class_methods[1:]
                            for class_method in class_methods:
                                class_methods_text=class_method.text.strip()
                                joined_text=f"{classname}.{class_methods_text}"
                                extracted_methods.append(joined_text)

        all_methods+=extracted_methods

    elif(package_name=="smartnoise-sql"):
        extracted_methods=[]
        api_reference_section = package_soup.find('h2',class_="anchor anchorWithStickyNavbar_LWe7",id="api-reference")  # Assuming 'api-reference' is the ID of the API Reference section
        if api_reference_section:
            # Find all <a> tags within the <ul> tag under API Reference
            api_reference_list = api_reference_section.find_next('ul')
            if api_reference_list:
                api_links = api_reference_list.find_all('a')
                # Extract and print the href attribute from each <a> tag
                for link in api_links:
                    href = link.get('href')
                    code_text = link.find('code').text.strip()  # Extract text within <code> tag
                    print()
                    if(code_text=="op_snsql.Privacy"):
                        extracted_methods.append(code_text)
                    else:
                        extracted_methods.append(f"{code_text}.get_privacy_cost")
                        extracted_methods.append(f"{code_text}.execute")
        all_methods+=extracted_methods

    elif(package_name=="smartnoise-synth"):
        extracted_methods=[]
        method_page = requests.get("https://docs.smartnoise.org/synth/synthesizers/index.html")  # Visit the linked page
        method_soup = BeautifulSoup(method_page.text, 'html.parser')

        classname="op_"
        classname+= method_soup.find('span', class_='sig-prename descclassname').text.strip()
        classname+=method_soup.find('span',class_="sig-name descname").text.strip()

        class_elements = method_soup.find_all('dl', class_='py method')

        for class_element in class_elements:
            class_method=class_element.find('span',class_="sig-name descname").text.strip()
            extracted_methods.append(f"{classname}.{class_method}")
        

        all_methods+=extracted_methods

    elif(package_name=="opendp"):
        extracted_methods=[]

        page_link="https://docs.opendp.org/en/stable/user/"

        open_dp_modules=[]
        open_dp_modules.append("transformations.html")
        open_dp_modules.append("measurements.html")
        open_dp_modules.append("combinators.html")

        for module in open_dp_modules:
            method_page = requests.get(f"{page_link}{module}")  # Visit the linked page
            method_soup = BeautifulSoup(method_page.text, 'html.parser')

            methods=method_soup.find_all("code",class_="xref py py-func docutils literal notranslate")
            methods = list(set(methods))

            for method in methods:
                extracted_methods.append(method.text.strip())
        
        all_methods+=extracted_methods
                
print(all_methods)



import sqlite3

# Function to retrieve table schema from SQLite database
def get_table_schema(table_name):
    conn = sqlite3.connect('codepeak_ag.db')  # Connect to the SQLite database
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info({table_name});")  # Fetch table schema
    schema = cursor.fetchall()

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

def preprocess(method):
    if method.startswith('op_pandas'):
        return 'pandas' + method[10:]
    elif method.startswith('diffprivlib'):
        return 'sklearn' + method[11:]
    return method

# Preprocess all_methods to match the prefixes in flattened_methods
processed_all_methods = [preprocess(method) for method in all_methods]

# Find unsupported methods in flattened_methods
unsupported_methods = [method for method in flattened_methods if preprocess(method) not in processed_all_methods]

# Display unsupported methods
print("Unsupported Methods:")
print(unsupported_methods)

import json

with open('unsupported_methods.json', 'w') as file:
    json.dump(unsupported_methods, file)

with open('supported_methods.json', 'w') as file:
    json.dump(processed_all_methods, file)