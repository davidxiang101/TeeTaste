import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import urllib

# Set the desired user agent string
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/95.0.1020.30 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/95.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.1.2 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Edge/95.0.1020.30 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/95.0",
]

headers = {
    "User-Agent": user_agents[5],
    "Accept-Language": "en-US,en;q=0.9",
}

# Configure Chrome options
options = Options()
options.add_argument("--headless")  # Run Chrome in headless mode (no GUI).
options.add_argument("--disable-gpu")  # Disable GPU acceleration for headless mode.


driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)


# This function will scrape images from the StockX website
def scrapeStockXShoes(driver, url, folderName, maxImages, timeout):
    # Set up the Chrome driver
    driver.get(url)
    print("Folder Name:", folderName)

    unique_images = set()  # Track unique image URLs
    i = 1

    start_time = time.time()
    while len(unique_images) < maxImages:
        try:
            # Find the images with CSS selector
            images = driver.find_elements(
                By.CSS_SELECTOR, "img.chakra-image.css-kpfxlo"
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

            if time.time() - start_time > timeout:
                print("Timeout reached. Exiting the loop.")
                break

            next_button = driver.find_element(By.XPATH, '//a[@aria-label="Next"]')
            next_button.click()
            driver.implicitly_wait(10)

        except Exception as e:
            print("Error:", str(e))
            break


# Create a folder to store the images
if not os.path.exists("images/StockXShoesImages"):
    os.makedirs("images/StockXShoesImages")

maxImages = 500
timeout = 60  # Timeout in seconds

url = "https://stockx.com/sneakers"  # Change the URL to the StockX sneakers section
scrapeStockXShoes(driver, url, "images/StockXShoesImages", maxImages, timeout)

# Close the browser
driver.quit()
