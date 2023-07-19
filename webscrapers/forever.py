import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import urllib
from urllib.error import HTTPError

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"

# Set the headers with the modified User-Agent
headers = {
    "User-Agent": user_agent,
    "Accept-Language": "en-US,en;q=0.9",
}

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument(f"user-agent={user_agent}")

# Set up the Chrome driver
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)


# This function will scrape images from the Forever 21 fashion section
def scrapeForeverFashion(url, folderName, maxImages):
    driver.get(url)
    print("Folder Name:", folderName)

    unique_images = set()  # Track unique image URLs
    i = 1

    while len(unique_images) < maxImages:
        try:
            # Find the images with class "product-tile__image"
            images = driver.find_elements(By.CSS_SELECTOR, ".product-tile__image")

            if not images:
                break

            for image in images:
                if i > maxImages:
                    break

                # Get the image source URL
                image_url = image.get_attribute("src")
                if image_url and image_url not in unique_images:
                    unique_images.add(image_url)
                    print("Image number", i, ":\n", image_url, "\n")
                    filename = f"image_{i}.jpg"

                    # Create the folder if it doesn't exist
                    if not os.path.exists(folderName):
                        os.makedirs(folderName)

                    try:
                        # Download and save the image
                        image_path = os.path.join(folderName, filename)
                        urllib.request.urlretrieve(image_url, image_path)
                        i += 1
                    except HTTPError as http_err:
                        if http_err.code == 403:
                            print("HTTP Error 403: Forbidden. Skipping image.")
                        else:
                            print("Error downloading image:", str(http_err))

            # Scroll to load more images
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)  # Wait for the page to load new images

        except Exception as e:
            print("Error:", str(e))
            break


# Create a folder to store the images
if not os.path.exists("images/ForeverImages"):
    os.makedirs("images/ForeverImages")

maxImages = 10

url = "https://www.forever21.com/us/shop/catalog/category/21men/mens-new-arrivals-graphic-tees"
scrapeForeverFashion(url, "images/ForeverImages", maxImages)

# Close the browser
driver.quit()
