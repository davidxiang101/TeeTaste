import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

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

def scrape_images(url, download_path):
    # Create the download directory if it doesn't exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Create a browser instance using ChromeDriver
    driver = webdriver.Chrome()

    try:
        # Navigate to the URL
        driver.get(url)

        # Wait for the page to load (adjust the wait time as needed)
        time.sleep(5)

        # Get the page source after the JavaScript has executed
        page_source = driver.page_source

        # Use BeautifulSoup to parse the loaded HTML
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the image tags containing the image URLs
        image_tags = soup.find_all('img', class_='img-responsive')

        for i, img_tag in enumerate(image_tags):
            img_url = img_tag['src']
            print(img_url)

            # If the image URL is relative, convert it to an absolute URL
            if not img_url.startswith('http'):
                img_url = "https:" + img_url

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

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    ae_url = "https://www.ae.com/us/en/c/men/tops/t-shirts/cat90012?pagetype=plp"
    download_path = "images/AEImages"  # The directory will be created if it doesn't exist

    scrape_images(ae_url, download_path)