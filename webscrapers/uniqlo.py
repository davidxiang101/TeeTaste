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


# This function will scrape images from the Uniqlo fashion section
def scrapeUniqloFashion(url, folderName, maxImages):
    driver.get(url)
    print("Folder Name:", folderName)

    i = 1

    while i <= maxImages:
        try:
            # Find the images with class "fr-ec-image__img"
            images = driver.find_elements(By.CSS_SELECTOR, ".fr-ec-image__img")

            if not images:
                break

            for image in images:
                if i > maxImages:
                    break

                # Get the image source URL
                image_url = image.get_attribute("src")
                print("Image number", i, ":\n", image_url, "\n")

                img_extension = os.path.splitext(image_url)[1].rsplit("?")[0]
                filename = f"image_{i}{img_extension}"

                # Create the folder if it doesn't exist
                if not os.path.exists(folderName):
                    os.makedirs(folderName)

                # Download and save the image
                image_path = os.path.join(folderName, filename)
                urllib.request.urlretrieve(image_url, image_path)

                i += 1

            # Scroll to load more images
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except Exception as e:
            print("Error:", str(e))
            break


# Create a folder to store the images
if not os.path.exists("images/UniqloImages"):
    os.makedirs("images/UniqloImages")

maxImages = 100

url = "https://www.uniqlo.com/us/en/men/tops/t-shirts"
scrapeUniqloFashion(url, "images/UniqloImages", maxImages)

# Close the browser
driver.quit()
