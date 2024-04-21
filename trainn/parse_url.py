from urllib.parse import urlparse, parse_qs
import re
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from urllib.parse import urlparse, unquote
import pandas as pd


def parse_url(url):
    parsed_url = urlparse(url)

    scheme = parsed_url.scheme
    domain = parsed_url.netloc
    path = parsed_url.path
    query_params = parse_qs(parsed_url.query)

    return {
        'scheme': scheme,
        'domain': domain,
        'path': path,
        'query_params': query_params
    }


def extract_product_name(url):
    parsed_url = urlparse(url)
    path = parsed_url.path

    # Split the path by '/'
    path_segments = path.split('/')

    # Extract the last segment (which represents the product name)
    product_name = path_segments[-1]

    # Remove extensions after "."
    product_name = product_name.split('.')[0]

    # Check if product_name contains only numbers
    if product_name.isdigit():
        # Extract the second-to-last element from the path if the last element from path is only a serial number
        product_name = path_segments[-2]



    # Optionally, you can further clean or process the product name
    # For example, removing dashes and converting to title case
    product_name = product_name.replace('-', ' ').title()

    # Check if "Info" is in the product name
    if "Info" == product_name:
        return "None"

    if "Id" == product_name:
        return "None"

    if "About" == product_name or "About Us" == product_name:
        return "None"

    if "Tag" == product_name:
        return "None"

    if "All" == product_name or "All Products" == product_name:
        return "None"

    if "Index" == product_name or "Terms Of Service" == product_name:
        return "None"

    if "Detail" == product_name:
        return "None"

    # DA SUNT FOARTE MULTE FISIERE DE TIPUL Products.html sau .php
    if "Products" == product_name or "Productos" == product_name or "Product" == product_name:
        return "None"

    if "Women" == product_name:
        return "None"

    if "Links" == product_name:
        return "None"

    if "Contact" == product_name or "Contact Us" == product_name:
        return "None"

    if "Show" == product_name:
        return "None"

    if "Works" == product_name:
        return "None"

    if "Vendors" == product_name:
        return "None"

    if "Help_Answer" == product_name:
        return "None"

    if "Login" == product_name or "User Login" == product_name:
        return "None"

    if "En" == product_name or "En Us" == product_name:
        return "None"

    if "Quality" == product_name or "Quality Control" == product_name:
        return "None"

    if "Accessories" == product_name or "Accessori" == product_name or "Accesorios" == product_name:
        return "None"

    if re.match(r'Tr\d+', product_name):
        return "None"

    if re.match(r'Lc \d+', product_name):
        return "None"



    # Optionally, you can decode URL encoded characters
    product_name = unquote(product_name)

    # Check if the product name contains URL encoded characters
    #if '%' in product_name:
    #    return None

    return product_name


# Function to read URLs from CSV file and extract product names
def extract_product_names_from_csv(csv_file_path):
    urls = []  # List to store URLs

    # Read URLs from CSV file
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            # Assuming the URLs are in the first column of each row
            url = row[0]
            urls.append(url)

    # List to store extracted product names
    product_names = []

    # Extract product names from each URL
    for url in urls:
        product_name = extract_product_name(url)
        if product_name.strip():  # Check if product_name is not an empty string
            product_names.append(product_name)
        else:
            product_names.append("None")  # Convert empty strings to None
    return product_names

def create_pdf_from_list(data_list, output_file):
    c = canvas.Canvas(output_file, pagesize=letter)
    y = 750  # Initial y-coordinate for drawing text

    for item in data_list:
        c.drawString(100, y, str(item))
        y -= 20  # Move to the next line

    c.save()

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_pdf_from_list(data_list, output_file, items_per_page=50):
    c = canvas.Canvas(output_file, pagesize=letter)
    y = 750  # Initial y-coordinate for drawing text
    page_number = 1

    for i, item in enumerate(data_list, start=1):
        if i % items_per_page == 0:
            c.drawString(500, 30, f"Page {page_number}")
            c.showPage()
            page_number += 1
            y = 750  # Reset y-coordinate for new page

        c.drawString(100, y, str(item))
        y -= 20  # Move to the next line

    # Add the last page if there are remaining items
    if len(data_list) % items_per_page != 0:
        c.drawString(500, 30, f"Page {page_number}")
        c.showPage()

    c.save()


# Example URL
# url = "https://example.com/products/electronics/smartphones/iphone-12-pro-max?color=blue"

# url2 = "https://capecodcandy.co/products/peach-gummies"

# url3 = "https://www.doublepickups.com/xo-magnetic-condenser-mic-systems?itemId=vuw4620lsxphgoffc2rmn5opvdxn18-rbf3g"

# parsed_data = parse_url(url)
# print(parsed_data)

# product_name = extract_product_name(url)
# print(product_name)

# parsed_data = parse_url(url2)
# print(parsed_data)

# product_name = extract_product_name(url2)
# print(product_name)

# parsed_data = parse_url(url3)
# print(parsed_data)

# product_name = extract_product_name(url3)
# print(product_name)


# Path to your CSV file
csv_file_path = 'input.csv'

# Extract product names from CSV file
product_names = extract_product_names_from_csv(csv_file_path)
df = pd.DataFrame({'product_name': product_names[1:]})
df.to_csv('prod.csv', sep=',', index=False, encoding='utf-8')
print(df)


#df_links = pd.read_csv(csv_file_path)
#df_links = df_links['url']

#df = df.reset_index(drop=False, inplace=False)
#df_links = df_links.reset_index(drop=False, inplace=False)

#result = pd.merge(df, df_links, on='index')

#result.to_csv('prod.csv', sep=',', index=False, encoding='utf-8')


# Output PDF file path
#output_pdf_file = "output.pdf"

# Create the PDF from the list
#create_pdf_from_list(product_names, output_pdf_file)

