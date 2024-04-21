from urllib.parse import urlparse, parse_qs, unquote
import re
import csv
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


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
    path_segments = path.split('/')
    product_name = path_segments[-1].split('.')[0]
    if product_name.isdigit():
        product_name = path_segments[-2]
    product_name = product_name.replace('-', ' ').title()
    if product_name.lower() in ["info", "id", "about", "about us", "tag", "all", "all products", "index", "terms of service",
                        "detail", "products", "productos", "product", "women", "links", "contact", "contact us",
                        "show", "works", "vendors", "help_answer", "login", "user login", "en", "en us", "quality",
                        "quality control", "accessories", "accessori", "accesorios"]:
        return "None"
    if re.match(r'Tr\d+', product_name) or re.match(r'Lc \d+', product_name):
        return "None"
    product_name = unquote(product_name)
    return product_name if '%' not in product_name else "None"

url_cross_ref = []

def extract_product_names_from_csv(csv_file_path):
    urls = []
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        urls = [row[0] for row in csv_reader]
    product_names = []
    for url in urls:
        product_name = extract_product_name(url)
        if product_name.strip():
            product_names.append(product_name)
        else:
            url_cross_ref.append(url)
    return product_names


def create_pdf_from_list(data_list, output_file, items_per_page=50):
    c = canvas.Canvas(output_file, pagesize=letter)
    y = 750
    page_number = 1
    for i, item in enumerate(data_list, start=1):
        if i % items_per_page == 0:
            c.drawString(500, 30, f"Page {page_number}")
            c.showPage()
            page_number += 1
            y = 750
        c.drawString(100, y, str(item))
        y -= 20
    if len(data_list) % items_per_page != 0:
        c.drawString(500, 30, f"Page {page_number}")
        c.showPage()
    c.save()

if __name__ == '__main__':
    csv_file_path = './input.csv'
    product_names = extract_product_names_from_csv(csv_file_path)

    df = pd.DataFrame({'product_name': product_names[1:]})
    df_links = pd.read_csv(csv_file_path)['url']
    df = df.reset_index(drop=False, inplace=False)
    df_links = df_links.reset_index(drop=False, inplace=False)

    result = pd.merge(df, df_links, on='index')
    result = result.drop(columns=['index'])
    result = result.drop(columns=['url'])
    # result.to_csv('prob.csv', sep=',', index=False, encoding='utf-8')

    #cross-reference with llama3 !!
    try:
        import get_product_names
        df = pd.DataFrame(columns=['product_name'])
        resp_list = []
        for url in url_cross_ref:
            prod_name = get_product_names.get_product_names(url)
            resp_list.append(prod_name)
            break
        df['product_name'] = resp_list

        df = df.reset_index(drop=False, inplace=False)

        df.index = range(result.index[-1] + 1, result.index[-1] + 1 + len(df))

        result_df = pd.concat([result, df], ignore_index=False)
        result_df = result_df.drop(columns=['index'])
        result_df = result.drop(columns=['index'])

        print(result_df.info())
        # df.to_csv('llama_generated.csv', sep=',', index=False, encoding='utf-8')

        result_df.to_csv('prod.csv', sep=',', index=False, encoding='utf-8')
    except Exception as e:
        result.to_csv('prod.csv', sep=',', index=False, encoding='utf-8')
        # print(e)



