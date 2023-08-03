from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import os
import time
import random

folderName = "images/StockXShoesImages"
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

user_agent = random.choice(user_agents)
headers = {
    "User-Agent": user_agent,
    "Accept-Language": "en-US,en;q=0.9",
}


def scrape_stockx_shoe_images(url_base, num_pages):
    options = Options()
    options.add_argument("--disable-gpu")  # Disable GPU acceleration for headless mode.

    driver = webdriver.Chrome(options=options)

    # Track unique image URLs
    unique_images = set()
    image_urls = []

    # Loop over the number of pages you want to scrape
    for i in range(num_pages):
        url = url_base.format(i + 1)
        driver.get(url)

        # Wait for the page to load and render the dynamic content (adjust the wait time as needed).
        driver.implicitly_wait(10)

        img_elements = driver.find_elements(
            By.CSS_SELECTOR, "img.chakra-image.css-kpfxlo"
        )

        for img_element in img_elements:
            image_url = img_element.get_attribute("src")
            if image_url and image_url not in unique_images:
                image_urls.append(image_url)
                unique_images.add(image_url)

    driver.quit()
    return image_urls


if __name__ == "__main__":
    stockx_url_base = "https://stockx.com/shoes?page={}"
    num_pages = 10
    image_urls = scrape_stockx_shoe_images(stockx_url_base, num_pages)

    for idx, image_url in enumerate(image_urls, start=1):
        time.sleep(random.uniform(2.0, 5.5))  # Add a random delay between each download
        idx = idx
        try:
            print(f"Image {idx}: {image_url}")
            if not os.path.exists(folderName):
                os.makedirs(folderName)
            filename = "image_{}.jpg".format(idx)
            # Download and save the image
            image_path = os.path.join(folderName, filename)
            img_response = requests.get(image_url, headers=headers)
            if img_response.status_code == 200:
                with open(image_path, "wb") as f:
                    f.write(img_response.content)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download image from URL: {image_url}")
        except:
            print("Failed to download image.")
