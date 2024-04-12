# Html-Parcer

This Python application is designed to scrape and extract product information from a list of URLs. Leveraging powerful libraries such as requests for handling HTTP requests, BeautifulSoup from beautifulsoup4 for parsing HTML content, and pandas for managing and exporting the data, it automatizes the process of collecting crucial product details from e-commerce or any product-based websites listed in a text file.

## Main Features
**_URL Processing:_** Reads a list of URLs from a text file ```(Url.txt)``` and processes each URL sequentially to extract product information.

**_Data Extraction:_** Utilizes BeautifulSoup to parse HTML content of each webpage and extracts structured product information such as name, description, price, currency, and availability.

**_Error Handling:_** Gracefully handles HTTP, SSL, and Request errors by logging them along with the URL, thus ensuring the process continuity even if some URLs are problematic.

**_Data Transformation and Export:_** Converts extracted data to a CSV file ```(products_info.csv)``` with proper formatting for prices, offering a seamless way to handle the extracted data for further analysis or use.

## Technologies Used
Python: As the core programming language, facilitating various powerful libraries and providing a base for the application logic.
requests: For performing HTTP requests to retrieve web pages.
BeautifulSoup4: Used for HTML content parsing and extraction of needed information.
pandas: For organizing the extracted data into a structured format and exporting it to CSV.
How It Works
The list of URLs is loaded from 
Url.txt.
Each URL is visited, and its content is fetched using the requests library.
The HTML content of each page is parsed with BeautifulSoup, and specific product information is extracted based on predefined HTML structures.
Extracted information for all products is compiled into a list.
This list is converted to a DataFrame using pandas, formatted adequately (e.g., price formatting), and finally exported to a 
products_info.csv
 file for easy access and use.
Installation and Usage
Before using the application, ensure that Python and all necessary packages (requests, beautifulsoup4, pandas) are installed. These dependencies are detailed in the 
pyproject.toml
, and you can easily install them using Poetry.

To run the application:

Ensure all URLs are listed in 
Url.txt
.

Execute the script with Python:

Insert
python main.py
Upon completion, check the 
products_info.csv
 file for the extracted data.

This application is designed for developers, data analysts, or anyone interested in extracting structured information from web pages efficiently and automatically.
