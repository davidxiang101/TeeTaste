import time
import os
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import urllib

# Set the desired user agent string
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"

headers = {
    "User-Agent": user_agent,
    "Accept-Language": "en-US,en;q=0.9",
}

# Configure Chrome options
options = Options()
options.add_argument("--headless")  # Run Chrome in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(f"user-agent={user_agent}")
options.add_argument("Accept-Language: en-US,en;q=0.9")


# Set up the Chrome driver
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service, options=options)


# This function will scrape images from the Urban Outfitters fashion section
def scrapeUrbanOutfittersFashion(url, folderName, maxImages, timeout):
    driver.get(url)
    print("Folder Name:", folderName)

    unique_images = set()  # Track unique image URLs

    i = 1

    start_time = time.time()
    while len(unique_images) < maxImages:
        try:
            # Find the images with class "o-pwa-image__img o-pwa-product-tile__media"
            images = driver.find_elements(
                By.CSS_SELECTOR, ".o-pwa-image__img.o-pwa-product-tile__media"
            )

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

                # Download and save the image
                image_path = os.path.join(folderName, filename)
                urllib.request.urlretrieve(image_url, image_path)

                i += 1

                if time.time() - start_time > timeout:
                    print("Timeout reached. Exiting the loop.")
                    break

                # Emulate user interaction by scrolling and waiting random intervals
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(1, 3))

            if time.time() - start_time > timeout:
                print("Timeout reached. Exiting the loop.")
                break

            # Randomly vary the number of requests by waiting before scrolling
            time.sleep(random.uniform(2, 4))

        except Exception as e:
            print("Error:", str(e))
            break


# Create a folder to store the images
if not os.path.exists("images/UrbanOutfittersImages"):
    os.makedirs("images/UrbanOutfittersImages")

maxImages = 100
timeout = 60  # Timeout in seconds

url = "https://www.urbanoutfitters.com/graphic-tees-for-men"
scrapeUrbanOutfittersFashion(url, "images/UrbanOutfittersImages", maxImages, timeout)

# Close the browser
driver.quit()
