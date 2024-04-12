import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import quote

with open('Url.txt', encoding='utf-8') as file:
    urls = file.read().splitlines()

def extract_product_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    product_info_list = soup.select('.product-page__product-info li')
    product_info = {}
    for item in product_info_list:
        name_span = item.find('span', class_='product-page__product-info_name')
        text_span = item.find('span', class_='product-page__product-info_text')
        if name_span and text_span:
            name = name_span.get_text().strip()
            text = text_span.get_text().strip()
            product_info[name] = text

    name_meta = soup.find('meta', itemprop='name')['content']
    description_meta = soup.find('meta', itemprop='description')['content']
    price_meta = soup.find('meta', itemprop='price')['content']
    currency_meta = soup.find('meta', itemprop='priceCurrency')['content']
    availability_link = soup.find('link', itemprop='availability')['href']

    product_info['Name'] = name_meta
    product_info['Description'] = description_meta
    product_info['Price'] = price_meta
    product_info['Currency'] = currency_meta
    product_info['Availability'] = availability_link.split('/')[-1]

    return product_info

all_products_info = []

for i, url in enumerate(urls):
    print(f"Processing URL {i+1}/{len(urls)}: {url}")
    try:
        encoded_url = quote(url, safe=':/')
        response = requests.get(encoded_url)

        response.raise_for_status()
        product_info = extract_product_info(response.content.decode('utf-8'))
        all_products_info.append(product_info)
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error for {url}: {err}")
        all_products_info.append({
            "URL": url,
            "Error": "HTTPError",
            "ErrorMessage": str(err)
        })
    except requests.exceptions.SSLError as ssl_err:
        print(f"SSL Error for {url}: {ssl_err}")
        all_products_info.append({
            "URL": url,
            "Error": "SSLError",
            "ErrorMessage": str(ssl_err)
        })
    except requests.exceptions.RequestException as e:
        print(f"Request Error for {url}: {e}")
        all_products_info.append({
            "URL": url,
            "Error": "RequestException",
            "ErrorMessage": str(e)
        })

if all_products_info:
    df = pd.DataFrame(all_products_info)
    for column in ['Price']:
        df[column] = df[column].astype(float).apply(lambda x: f"{x:.1f}" if x.is_integer() else f"{x:.2f}")
    df.to_csv('products_info.csv', index=False, encoding='utf-8-sig', sep=';')