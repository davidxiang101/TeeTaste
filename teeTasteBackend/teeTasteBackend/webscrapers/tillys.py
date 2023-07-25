import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64

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
# Set up the Chrome WebDriver with custom user agent
chrome_options = ChromeOptions()
chrome_options.add_argument(f"user-agent={user_agents[6]}")

def save_image_from_base64(base64_data, image_path):
    img_data = base64.b64decode(base64_data)
    with open(image_path, 'wb') as f:
        f.write(img_data)
    print(f"Downloaded: {image_path}")

def scrape_images(url, download_path):
    # Create the download directory if it doesn't exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Set up the Chrome WebDriver
    # chromedriver_path = '/path/to/chromedriver'  # Replace with the actual path to chromedriver
    # chrome_service = ChromeService(executable_path=chromedriver_path)
    driver = webdriver.Chrome()#service=chrome_service)

    try:
        # Navigate to the URL
        driver.get(url)

        # Wait for the page to load (adjust the wait time as needed)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-tile-image")))

        # Find the image elements
        image_elements = driver.find_elements(By.CLASS_NAME, "product-tile-image")

        for i, img_element in enumerate(image_elements):
            # Get the Base64-encoded image data from the element
            img_url = img_element.get_attribute("src")

            # Check if the image URL starts with "data:image" (Base64 data URI)
            if img_url.startswith('data:image'):
                # Save the image as a file
                filename = f"image_{i}.jpg"
                image_path = os.path.join(download_path, filename)
                save_image_from_base64(img_url.split(",")[1], image_path)
            else:
                # Download and save the image from the regular URL
                filename = f"image_{i}.jpg"
                image_path = os.path.join(download_path, filename)
                img_response = requests.get(img_url)
                if img_response.status_code == 200:
                    with open(image_path, 'wb') as f:
                        f.write(img_response.content)
                    print(f"Downloaded: {image_path}")
                else:
                    print(f"Failed to download image from URL: {img_url}")

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    tillys_url = "https://www.tillys.com/men/clothing/t-shirts/"
    download_path = "images/TillysImages"  # The directory will be created if it doesn't exist

    scrape_images(tillys_url, download_path)