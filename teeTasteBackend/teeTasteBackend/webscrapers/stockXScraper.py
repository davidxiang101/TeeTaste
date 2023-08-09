import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
from PIL import Image

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
    "User-Agent": user_agents[7],
    "Accept-Language": "en-US,en;q=0.9",
}

def download_images(url, download_path, output_file):
    # Create the download directory if it doesn't exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Set up the Chrome WebDriver
    driver = webdriver.Chrome()

    try:
        # Navigate to the URL
        driver.get(url)

        # Wait for the page to load (adjust the wait time as needed)
        time.sleep(10)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "css-tkc8ar")))

        # Now, scrape and download the images
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        div_tags = soup.find_all('div', class_='css-tkc8ar')

        i = 960
        for div_tag in div_tags:
            img_url = div_tag.find('img').get('src')
            if img_url:
                print(img_url)
                # Split the URL at the "?" delimiter
                img_url, query_parameters = img_url.split("?", 1)

                # Download and save the image
                filename = f"image_{i}.png"
                image_path = os.path.join(download_path, filename)
                img_response = requests.get(img_url, headers=headers)
                if img_response.status_code == 200:
                    with open(image_path, 'wb') as f:
                        f.write(img_response.content)
                    print(f"Downloaded: {filename}")

                    with open(output_file, 'a') as file:
                        file.write(f"Image {i}: {img_url}\n")

                    # Open and verify the downloaded image using Pillow
                    try:
                        img = Image.open(image_path)
                        img.verify()  # Verify image integrity
                        print(f"Verified: {filename}")
                    except Exception as e:
                        print(f"Verification failed: {filename} - {e}")
                else:
                    print(f"Failed to download image from URL: {img_url}")
                i += 1
            else:
                print("Source tag not found in the picture tag.")

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    stockX = "https://stockx.com/sneakers?page=25"
    download_path = "images/sneakers"  # The directory will be created if it doesn't exist
    output_file = "sneakers.txt"
    download_images(stockX, download_path, output_file)
