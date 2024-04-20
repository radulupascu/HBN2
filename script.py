import pandas as pd
import re
from urllib import urlparse, parse_qs

def extract_words_from_link(url):
    
    pattern = r'\b\w+\b'
    words = re.findall(pattern, url)
    return words

def parse(csv_file, n):
    df = pd.read_csv(csv_file)
    
    for link in df.iloc[0:n, 0]:
        print(extract_words_from_link(str(link)))

if __name__ == '__main__':
    csv_file = './url_product_extraction_input_dataset.csv'  # Replace with your CSV file path
    
    parse(csv_file, 10)
