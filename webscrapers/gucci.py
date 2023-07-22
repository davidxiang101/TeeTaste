import os
import requests
from bs4 import BeautifulSoup
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    driver = webdriver.Chrome()

    try:
        page_number = 1
        uniqueImages = 0
        maxImages = 77

        while uniqueImages < maxImages:
            # Navigate to the URL of the current page
            page_url = f"{url}?page={page_number}"
            driver.get(page_url)

            # Wait for the images to load
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-tiles-grid-item-image")))

            # Get the updated HTML content after scrolling to capture all images
            updated_html = driver.page_source
            soup = BeautifulSoup(updated_html, 'html.parser')
            image_divs = soup.find_all('div', class_='product-tiles-grid-item-image')
            if not image_divs:
                # No more images on the current page, break the loop
                break

            i = 0
            for div in image_divs:
                # Find the picture tag inside the div
                picture_tag = div.find('picture')
                if picture_tag:
                    # Find all the source tags inside the picture tag
                    source_tags = picture_tag.find_all('source', srcset=True, attrs={'data-image-size': 'standard'})
                    for source_tag in source_tags:
                        # Extract the srcset attribute from the source tag
                        srcset = source_tag['srcset']
                        # Download and save the first image (highest resolution) in the list
                        img_url = "https:" + srcset
                        print(img_url)
                        uniqueImages = uniqueImages + 1

                        filename = f"image_{i}.jpg"
                        image_path = os.path.join(download_path, filename)
                        img_response = requests.get(img_url, headers=headers)
                        if img_response.status_code == 200:
                            with open(image_path, 'wb') as f:
                                f.write(img_response.content)
                            print(f"Downloaded: {filename}")
                        else:
                            print(f"Failed to download image from URL: {img_url}")
                        i = i + 1
                else:
                    print("Picture tag not found in the div.")

            page_number += 1

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    gucci_url = "https://www.gucci.com/us/en/ca/men/ready-to-wear-for-men/t-shirts-polo-shirts-for-men-c-men-readytowear-tshirts-and-polos"
    download_path = "images/GucciImages"  # The directory will be created if it doesn't exist

    download_images(gucci_url, download_path)
