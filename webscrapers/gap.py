import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import urllib

# Set the desired user agent string
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
# Configure Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument(f"user-agent={user_agent}")

# Set up the Chrome driver
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)


# This function will scrape images from the H&M fashion section
def scrapeGapFashion(url, folderName, maxImages):
    driver.get(url)
    print("Folder Name:", folderName)

    unique_images = set()  # Track unique image URLs
    i = 1
    while len(unique_images) < maxImages:
        try:
            # Find the images with class "item-image"
            images = driver.find_elements(By.CSS_SELECTOR, 'img.category-page-1fe0xra')

            if not images:
                break
            before = i
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

            if before == i:
              break
            # Scroll to load more images
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(10)  # Wait for the page to load new images

        except Exception as e:
            print("Error:", str(e))
            break


# Create a folder to store the images
if not os.path.exists("images/GapImages"):
    os.makedirs("images/GapImages")

maxImages = 100

url = "https://www.gap.com/browse/category.do?cid=5225&nav=meganav%3AMen%3ACategories%3AT-Shirts#pageId=0&department=75"
scrapeGapFashion(url, "images/GapImages", maxImages)

# Close the browser
driver.quit()
