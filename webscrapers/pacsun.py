import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
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
    "User-Agent": user_agents[5],
    "Accept-Language": "en-US,en;q=0.9",
}


def scroll_to_height(driver):
    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight - 2400);")


def download_images(url, download_path):
    # Create the download directory if it doesn't exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Set up the Chrome WebDriver
    driver = webdriver.Chrome()

    try:
        # Navigate to the URL
        driver.get(url)

        # Wait for the page to load (adjust the wait time as needed)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "w-100")))

        # Scroll down to load additional images
        # scroll_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
        # while True:
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #     time.sleep(10)  # Adjust the wait time as needed
        #     new_scroll_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
        #     if new_scroll_height == scroll_height:
        #         # No more additional images to load, break the loop
        #         break
        #     else:
        #         scroll_height = new_scroll_height

        for i in range(20):  # Perform 20 partial scrolls
            scroll_to_height(driver)
            time.sleep(
                2
            )  # Add a short delay to allow the content to load before scrolling further

        # Now, scrape and download the images
        soup = BeautifulSoup(driver.page_source, "html.parser")
        images = soup.find_all("img", class_="w-100")

        i = 0
        for image in images:
            img_url = image["src"]
            print(img_url)

            # Download and save the image
            filename = f"image_{i}.jpg"
            image_path = os.path.join(download_path, filename)
            img_response = requests.get(img_url, headers=headers)
            if img_response.status_code == 200:
                with open(image_path, "wb") as f:
                    f.write(img_response.content)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download image from URL: {img_url}")
            i += 1

    finally:
        # Close the browser
        driver.quit()


if __name__ == "__main__":
    ssense_url = "https://www.pacsun.com/mens/graphic-tees/"
    download_path = (
        "images/PacSunImages"  # The directory will be created if it doesn't exist
    )

    download_images(ssense_url, download_path)
