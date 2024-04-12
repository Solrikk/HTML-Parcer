from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, HTMLResponse
import uvicorn
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import quote
import asyncio

app = FastAPI()

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

async def process_url(url):
    try:
        encoded_url = quote(url, safe=':/')
        response = requests.get(encoded_url)

        response.raise_for_status()
        product_info = extract_product_info(response.content.decode('utf-8'))
        return product_info
    except requests.exceptions.HTTPError as err:
        return {
            "URL": url,
            "Error": "HTTPError",
            "ErrorMessage": str(err)
        }
    except requests.exceptions.SSLError as ssl_err:
        return {
            "URL": url,
            "Error": "SSLError",
            "ErrorMessage": str(ssl_err)
        }
    except requests.exceptions.RequestException as e:
        return {
            "URL": url,
            "Error": "RequestException",
            "ErrorMessage": str(e)
        }

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Upload URLs File</title>
        </head>
        <body>
            <h2>Upload File</h2>
            <form action="/upload-file/" enctype="multipart/form-data" method="post">
            <input name="file" type="file" accept=".txt">
            <input type="submit">
            </form>
        </body>
    </html>
    """

@app.post("/upload-file/")
async def create_upload_file(file: UploadFile = File(...)):
    content = await file.read()
    urls = content.decode('utf-8').splitlines()

    tasks = [process_url(url) for url in urls]
    products_info = await asyncio.gather(*tasks)

    if products_info:
        df = pd.DataFrame(products_info)
    else:
        df = pd.DataFrame({"Message": ["No data extracted"]})

    file_path = 'products_info.csv'
    df.to_csv(file_path, index=False, encoding='utf-8-sig', sep=';')

    return FileResponse(path=file_path, filename=file_path, media_type='text/csv')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)