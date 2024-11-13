# Skateboard Product Scraper

A Python script that scrapes skateboard product information from scrapepark.org and saves it to a CSV file. The script can work with both local HTML files and live web requests.

## Features

- Scrapes skateboard product details including:
  - Product names
  - Prices
  - Product image URLs
- Supports both local HTML parsing and live web scraping
- Handles urllib3 version compatibility automatically
- Saves data in CSV format for easy analysis
- Includes error handling and safe text extraction

## Prerequisites

- Python 3.x
- pip (Python package installer)

## Required Libraries

```
requests
beautifulsoup4
urllib3
```

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd skateboard-scraper
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

The script will automatically handle urllib3 version compatibility issues if they arise.

## Usage

### Basic Usage

Run the script directly:

```bash
python importrequests.py
```

This will:
1. Attempt to read from a local `products.html` file
2. If the local file isn't found, scrape data from scrapepark.org
3. Save the results to `skateboards.csv`
4. Display a sample of the scraped data

### Output

The script generates a CSV file (`skateboards.csv`) with the following columns:
- Product Name
- Price
- Product Image

## Functions

### `safe_extract_text(element, selector, class_name=None)`
Safely extracts text from HTML elements with error handling.

### `scrape_products()`
Main scraping function that processes the HTML and extracts product information.

### `save_to_csv(products, filename='skateboards.csv')`
Saves the scraped data to a CSV file.

## Error Handling

The script includes comprehensive error handling for:
- urllib3 version compatibility issues
- File not found errors
- HTML parsing errors
- Network request errors
- Individual product processing errors

## Contributing

Feel free to open issues or submit pull requests with improvements.

## License

MIT License

## Disclaimer

This scraper is intended for educational purposes. Make sure to review and comply with scrapepark.org's terms of service and robots.txt file before deploying the scraper.