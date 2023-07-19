import os
import requests
from bs4 import BeautifulSoup

# Set the desired user agent string
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"

# Set the headers with the modified user agent
headers = {
    "User-Agent": user_agent,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


# This function will create a soup and return the parsed HTML format for extracting HTML tags from the webpage
def makeSoup(url):
    # Load the webpage for the given URL using requests
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


# This function will scrape images from the Uniqlo fashion section
def scrapeUniqloFashion(url, folderName, maxImages):
    soup = makeSoup(url)
    print("Folder Name:", folderName)

    i = 1
    for image in soup.findAll("img", {"class": "fr-ec-image__img"}):
        if i <= maxImages:  # Check the number of images to be downloaded
            image_url = image.get("src")
            print("Image number", i, ":\n", image_url, "\n")

            img_extension = os.path.splitext(image_url)[1]
            filename = f"image_{i}{img_extension}"

            imageFile = open(os.path.join(folderName, filename), "wb")
            imageFile.write(requests.get(image_url).content)
            imageFile.close()

            i += 1
        else:
            break


# Create a folder to store the images
if not os.path.exists("images/UniqloImages"):
    os.makedirs("images/UniqloImages")

maxImages = 100

url = "https://www.uniqlo.com/us/en/men/tops/t-shirts"
scrapeUniqloFashion(url, "images/UniqloImages", maxImages)
