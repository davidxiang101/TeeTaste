import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import urllib

# Set the desired user agent string
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4900.88 Safari/537.36"
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
def scrapeRalphLaurenFashion(url, folderName, maxImages):
    driver.get(url)
    print("Folder Name:", folderName)

    unique_images = set()  # Track unique image URLs
    i = 1

    while len(unique_images) < maxImages:
        try:
            # Find the images with class "item-image"
            images = driver.find_elements(By.CSS_SELECTOR, 'img.default-img')

            if not images:
                break

            for image in images:
                if i > maxImages:
                    break
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
            total_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")

            # Calculate one-eighth of the page height
            one_eighth_height = total_height // 8

            driver.execute_script("window.scrollTo(0, {});".format(one_eighth_height))
            time.sleep(1)  # Wait for the page to load new images

            # Check if the "Load more products" button exists
            load_more_button = driver.find_element(
                By.CSS_SELECTOR, 'a.view-all'
            )
            if load_more_button.is_displayed():
                # Click the "Load more products" button
                driver.execute_script("arguments[0].click();", load_more_button)
                time.sleep(15)  # Wait for the page to load new products
                driver.execute_script("window.scrollTo(0, {});".format(one_eighth_height))
            else:
                break

        except Exception as e:
            print("Error:", str(e))
            break


# Create a folder to store the images
if not os.path.exists("images/RalphLaurenImages1"):
    os.makedirs("images/RalphLaurenImages1")

maxImages = 100

url = "https://www.ralphlauren.com/men-clothing-t-shirts"
scrapeRalphLaurenFashion(url, "images/RalphLaurenImages1", maxImages)

# Close the browser
driver.quit()
