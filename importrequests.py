import requests

# Make a request to https://scrapepark.org
# Store the result in 'res' variable
res = requests.get(
    'https://scrapepark.org')
txt = res.text
status = res.status_code

print(txt, status)
# print the result
