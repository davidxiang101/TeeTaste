import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_images(url, download_path):
    # Create the download directory if it doesn't exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Set up the Chrome WebDriver
    # chromedriver_path = '/path/to/chromedriver'  # Replace with the actual path to chromedriver
    # chrome_service = ChromeService(executable_path=chromedriver_path)
    driver = webdriver.Chrome() #service=chrome_service)

    try:
        # Navigate to the URL
        driver.get(url)

        # Wait for the page to load (adjust the wait time as needed)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ProductCardAsset_media__yMYE9")))

        # Get the page source
        page_source = driver.page_source

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the div elements containing the images
        image_divs = soup.find_all('div', class_='ProductCardAsset_media__yMYE9')

        for i, div in enumerate(image_divs):
            # Find the image tag inside the div
            img_tag = div.find('img')
            if img_tag:
                img_url = img_tag['src']
                # Download and save the image
                filename = f"image_{i}.jpg"
                image_path = os.path.join(download_path, filename)
                img_response = requests.get(img_url)
                if img_response.status_code == 200:
                    with open(image_path, 'wb') as f:
                        f.write(img_response.content)
                    print(f"Downloaded: {filename}")
                else:
                    print(f"Failed to download image from URL: {img_url}")
            else:
                print("Image not found in the div.")

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    dior_url = "https://www.dior.com/en_us/fashion/mens-fashion/whats-new-for-men?category_filter=T-shirts"
    download_path = "images/DiorImages"  # The directory will be created if it doesn't exist

    scrape_images(dior_url, download_path)