import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set the desired user agent string
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"

headers = {
    "User-Agent": user_agent,
    "Accept-Language": "en-US,en;q=0.9",
}

def download_images(url, download_path):
    # Create the download directory if it doesn't exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Create a browser instance using ChromeDriver
    driver = webdriver.Chrome()

    try:
        # Set the user agent and headers
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})
        driver.set_network_conditions(
            offline=False,
            latency=0,  # Additional latency (ms)
            download_throughput=1024 * 1024,  # Download speed (bytes/s)
            upload_throughput=1024 * 1024,  # Upload speed (bytes/s)
        )

        # Navigate to the URL
        driver.get(url)

        # Wait for the image elements to be present on the page
        wait = WebDriverWait(driver, 10)
        image_divs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'productHeroContainer_dVvdX')))
        
        i = 0
        for div in image_divs:
            try:
                # Find the 'img' element within the 'div' element
                img_tag = div.find_element(By.TAG_NAME, 'img')
                if img_tag:
                    img_url = img_tag.get_attribute('src')
                    # img_url = "https:" + img_url
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
                else:
                    print("Image not found in the div.")
                i = i + 1
            except Exception as e:
                print(f"Error while processing image: {str(e)}")
                
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    asos_url = "https://www.asos.com/us/men/t-shirts-tank-tops/cat/?cid=7616"
    download_path = "images/AsosImages"  # The directory will be created if it doesn't exist

    download_images(asos_url, download_path)