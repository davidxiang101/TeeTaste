import os
import requests
from bs4 import BeautifulSoup

# URL of the website you want to scrape
url = 'https://www.example.com'

# Send a get request to the website
response = requests.get(url)

# Parse the website's content
soup = BeautifulSoup(response.text, 'html.parser')

# Find all image tags
img_tags = soup.find_all('img')

# Check if 'images' folder exists
if not os.path.exists('images'):
    os.makedirs('images')

# Loop over each image tag
for img_tag in img_tags:
    img_url = img_tag.get('src')

    # Complete the image URL if it's incomplete
    if 'http' not in img_url:
        img_url = url + img_url

    # Get the content of the image
    response = requests.get(img_url, stream=True)

    # Open a file and save the image
    with open('images/' + img_url.split('/')[-1], 'wb') as out_file:
        out_file.write(response.content)
