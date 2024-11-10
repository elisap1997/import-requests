import pkg_resources
import sys

# Check urllib3 version and install compatible version if needed
try:
    urllib3_version = pkg_resources.get_distribution('urllib3').version
    if urllib3_version.startswith('2.'):
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'urllib3==1.26.15'])
        print("Installed compatible urllib3 version")
except Exception as e:
    print(f"Error handling urllib3 version: {e}")

import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin

def scrape_products():
    # Make a request
    base_url = "https://scrapepark.org"
    page = requests.get(f"{base_url}/#products")
    soup = BeautifulSoup(page.content, 'html.parser')

    # Create products list
    products = []

    # Find all product containers
    product_items = soup.find_all('div', class_='product-item')  # Adjust class name based on actual HTML

    for item in product_items:
        try:
            # Extract product name
            name = item.find('h3', class_='product-name').text.strip()  # Adjust class name
            
            # Extract price (remove currency symbol and convert to float)
            price = item.find('span', class_='price').text.strip()  # Adjust class name
            price = price.replace('$', '').strip()
            
            # Extract image URL and make it absolute
            img_tag = item.find('img')
            img_url = img_tag.get('src') if img_tag else ''
            img_url = urljoin(base_url, img_url) if img_url else ''

            products.append({
                "Product Name": name,
                "Price": price,
                "Product Image": img_url
            })
        except AttributeError as e:
            print(f"Error processing product: {e}")
            continue

    return products

def save_to_csv(products, filename='products.csv'):
    # Define the field names for CSV
    fields = ["Product Name", "Price", "Product Image"]

    # Write to CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=fields)
        dict_writer.writeheader()
        dict_writer.writerows(products)

def main():
    try:
        # Scrape products
        products = scrape_products()
        
        # Save to CSV
        save_to_csv(products)
        
        print(f"Successfully scraped {len(products)} products and saved to products.csv")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

