import requests
from bs4 import BeautifulSoup

# Make a request to https://scrapepark.org
page = requests.get(
    "https://scrapepark.org")
soup = BeautifulSoup(page.content, 'html.parser')

# Extract title of page
page_title = soup.title.text

# print the result
print(page_title)
