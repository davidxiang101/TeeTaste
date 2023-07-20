import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
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


# This function will scrape images from the Ralph Lauren fashion section
def scrapeRalphLaurenFashion(url, folderName, maxImages, timeout):
    driver.get(url)
    print("Folder Name:", folderName)

    unique_images = set()  # Track unique image URLs
    i = 1

    start_time = time.time()
    while len(unique_images) < maxImages:
        try:
            # Find the images with class "product-image"
            images = driver.find_elements(By.CSS_SELECTOR, ".product-image img")

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

            # Scroll to load more images
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)  # Wait for the page to load new images

            # Check if the "Load more" button exists
            load_more_button = driver.find_element(By.CSS_SELECTOR, "a.more-button")
            if load_more_button.is_displayed():
                # Click the "Load more" button
                driver.execute_script("arguments[0].click();", load_more_button)
                time.sleep(5)  # Wait for the page to load new products
            else:
                break

        except Exception as e:
            print("Error:", str(e))
            break


# Create a folder to store the images
if not os.path.exists("images/RalphLaurenImages"):
    os.makedirs("images/RalphLaurenImages")

maxImages = 100
timeout = 60  # Timeout in seconds

url = "https://www.ralphlauren.com/men-clothing-t-shirts"
scrapeRalphLaurenFashion(url, "images/RalphLaurenImages", maxImages, timeout)

# Close the browser
driver.quit()
