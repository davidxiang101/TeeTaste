import os
import urllib
import urllib.request
from bs4 import BeautifulSoup
import requests

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


# This function will scrape images from the Amazon fashion section
def scrapeAmazonFashion(url, folderName, maxImages):
    soup = makeSoup(url)
    print("Folder Name:", folderName)

    i = 1
    for image in soup.findAll("img", {"class": "s-image"}):
        if i <= maxImages:  # Check the number of images to be downloaded
            image_url = image.get("src")
            print("Image number", i, ":\n", image_url, "\n")

            nameOfFile = image.get("alt")
            nameOfFile = nameOfFile.replace("/", "-")
            img = image.get("src")
            tempCheck = img.split(".")
            check = str(tempCheck[len(tempCheck) - 1])
            ImageType = ".jpeg"  # Default image type

            if check == "jpg" or check == "jpeg":
                ImageType = ".jpeg"
            elif check == "png":
                ImageType = ".png"

            filename = nameOfFile
            folderIndividualName = (
                "AmazonImages/" + folderName + "/"
            )  # Path where the images will be stored

            # Create the folder according to the search name
            if not os.path.exists(folderIndividualName):
                os.makedirs(folderIndividualName)

            imageFile = open(folderIndividualName + filename + ImageType, "wb")
            imageFile.write(
                requests.get(img).content
            )  # Read and save the image file from the link
            imageFile.close()

            i += 1
        else:
            break


# Create a folder to store the images
if not os.path.exists("images/AmazonImages"):
    os.makedirs("images/AmazonImages")

maxImagesPerCategory = 10  # Maximum number of images to scrape per category

# List of fashion categories on Amazon
categories = [
    "mens-shirts",
    "mens-tshirts",
    "mens-polos",
    "womens-tops-tees",
    "womens-dresses",
    "womens-blouses-button-down-shirts",
]

# Scrape images for each category
for category in categories:
    url = f"https://www.amazon.com/s?rh=n%3A7141123011&page=1&keywords={category}"
    folderName = category.replace("-", "_")

    scrapeAmazonFashion(url, folderName, maxImagesPerCategory)
