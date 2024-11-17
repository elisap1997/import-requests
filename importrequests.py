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

def safe_extract_text(element, selector, class_name=None):
    """Safely extract text from an element"""
    try:
        if class_name:
            found = element.find(selector, class_=class_name)
        else:
            found = element.find(selector)
        return found.text.strip() if found else ''
    except (AttributeError, TypeError):
        return ''

def scrape_products():
    # Make a request
    base_url = "https://scrapepark.org"
    
    try:
        # Instead of making an HTTP request, use the local HTML content
        with open('products.html', 'r', encoding='utf-8') as file:
            content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
    except FileNotFoundError:
        print("Warning: products.html not found, attempting HTTP request...")
        page = requests.get(f"{base_url}/#products")
        soup = BeautifulSoup(page.content, 'html.parser')

    # Create products list
    products = []

    # Find all product boxes
    product_items = soup.find_all('div', class_='box')

    for item in product_items:
        try:
            # Find the detail box
            detail_box = item.find('div', class_='detail-box')
            if not detail_box:
                continue

            # Extract product name
            h5_element = detail_box.find('h5')
            if h5_element:
                span_element = h5_element.find('span')
                span_text = span_element.text.strip() if span_element else ''
                # Get the number part (last text node)
                number_text = h5_element.contents[-1].strip() if h5_element.contents else ''
                full_name = f"{span_text} {number_text}".strip()
            else:
                full_name = ''

            # Extract price
            h6_element = detail_box.find('h6')
            price = h6_element.text.strip().replace('$', '') if h6_element else ''

            # Extract image URL
            img_box = item.find('div', class_='img-box')
            img_tag = img_box.find('img') if img_box else None
            img_url = img_tag.get('src', '') if img_tag else ''
            img_url = urljoin(base_url, img_url) if img_url else ''

            # Only add product if we have at least a name or price
            if full_name or price:
                products.append({
                    "Product Name": full_name,
                    "Price": price,
                    "Product Image": img_url
                })

        except Exception as e:
            print(f"Error processing product: {str(e)}")
            continue

    return products

def clean_skateboard_data(products):
    """Clean the product data to remove non-skateboard entries"""
    clean_products = [
        product for product in products
        if (product['Product Name'].lower().find('skateboard') != -1 and
            product['Price'] and  # Must have a price
            product['Product Image'])  # Must have an image
    ]
    
    removed_count = len(products) - len(clean_products)
    if removed_count > 0:
        print(f"Removed {removed_count} non-skateboard entries during cleaning")
    
    return clean_products

def save_to_csv(products, filename='skateboards.csv'):
    # Define the field names for CSV
    fields = ["Product Name", "Price", "Product Image"]

    # Write to CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=fields)
        dict_writer.writeheader()
        dict_writer.writerows(products)
        print(f"Data saved to {filename}")

def main():
    try:
        # Scrape products
        products = scrape_products()
        
        if products:
            # Clean the data
            clean_products = clean_skateboard_data(products)
            
            # Save to CSV
            save_to_csv(clean_products)
            print(f"Successfully scraped and cleaned {len(clean_products)} skateboards")
            
            # Print first few entries as sample
            print("\nSample of scraped data:")
            for product in clean_products[:3]:
                print(product)
        else:
            print("No products were found to scrape")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()

