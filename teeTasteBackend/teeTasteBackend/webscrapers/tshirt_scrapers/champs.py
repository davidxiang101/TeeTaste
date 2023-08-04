import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib

# Set the desired user agent string
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument(f"user-agent={user_agent}")

# Set up the Chrome driver
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)


# This function will scrape images from the H&M fashion section
def scrapeChampsFashion(url, folderName, maxImages):
    driver.get(url)
    print("Folder Name:", folderName)

    unique_images = set()  # Track unique image URLs
    i = 1

    while len(unique_images) < maxImages:
        try:
            # Find the images with class "item-image"
            images = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "img"))
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

                # Scroll to load more images
                # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)  # Wait for the page to load new images

            # # Check if the "next" button exists
            # load_more_button = driver.find_element(
            #     By.CSS_SELECTOR, "col.Pagination-option.Pagination-option--next.col-shrink"
            # )
            # if load_more_button.is_displayed():
            #     # Click the "Load more products" button
            #     driver.execute_script("arguments[0].click();", load_more_button)
            #     time.sleep(2)  # Wait for the page to load new products
            else:
                break

        except Exception as e:
            print("Error:", str(e))
            break


# Create a folder to store the images
if not os.path.exists("images/ChampsImages"):
    os.makedirs("images/ChampsImages")

# Scrape images for each category
for category in categories:
  
    url = f"https://www.amazon.com/s?rh=n%3A7141123011&page=1&keywords={category}"
    folderName = category.replace("-", "_")

    scrapeChampsFashion(url, folderName, maxImagesPerCategory)
