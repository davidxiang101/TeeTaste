import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

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
    "User-Agent": user_agents[2],
    "Accept-Language": "en-US,en;q=0.9",
}

def download_images(url, download_path):
    # Create the download directory if it doesn't exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Set up the Chrome WebDriver
    chromedriver_path = '/path/to/chromedriver'  # Replace with the actual path to chromedriver
    chrome_service = ChromeService(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=chrome_service)

    try:
        # Navigate to the URL
        driver.get(url)

        # Wait for the page to load and images to be visible (adjust the wait time as needed)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-card__picture")))

        # Find all the image elements with class name "product-card__picture"
        image_elements = driver.find_elements(By.CLASS_NAME, "product-card__picture")
        i = 0

        # Get the initial count of images
        initial_image_count = len(image_elements)

        # Scroll down to load additional images
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Adjust the wait time as needed
            image_elements = driver.find_elements(By.CLASS_NAME, "product-card__picture")
            if len(image_elements) == initial_image_count:
                # No more additional images to load, break the loop
                break
            else:
                initial_image_count = len(image_elements)

        # Now, scrape and download the images
        for img_element in image_elements:
            img_srcset = img_element.get_attribute('srcset')
            if img_srcset:
                # Extract the URL of the image from the srcset attribute
                img_urls = img_srcset.split(',')
                img_url = img_urls[-1].strip().split()[0]
            else:
                # If srcset attribute is not present, get the image URL from the src attribute
                img_url = img_element.get_attribute('src')

            print(img_url)

            # Download and save the image
            filename = f"image_{i}.jpg"
            image_path = os.path.join(download_path, filename)
            img_response = requests.get(img_url, headers=headers)
            if img_response.status_code == 200:
                with open(image_path, 'wb') as f:
                    f.write(img_response.content)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download image from URL: {img_url}")
            i += 1

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    prada_url = "https://www.prada.com/us/en/mens/ready-to-wear/shirts/c/10138US"
    download_path = "images/PradaImages"  # The directory will be created if it doesn't exist

    download_images(prada_url, download_path)