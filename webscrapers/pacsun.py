# import os
# import requests
# from bs4 import BeautifulSoup
# from selenium import webdriver
# import urllib.parse as urlparse
# import time

# # import random 
# from random import random

# def download_images(url, download_path, max_images=100):
#     # Create the download directory if it doesn't exist
#     if not os.path.exists(download_path):
#         os.makedirs(download_path)

#     # Create a browser instance using ChromeDriver
#     driver = webdriver.Chrome()

#     try:
#         # Set the user agent and headers
#         driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})
#         driver.set_network_conditions(
#             offline=False,
#             latency=0,  # Additional latency (ms)
#             download_throughput=1024 * 1024,  # Download speed (bytes/s)
#             upload_throughput=1024 * 1024,  # Upload speed (bytes/s)
#         )

#         # Navigate to the URL
#         driver.get(url)

#         image_count = 0
#         while True:
#             # Wait for a short period to let new images load
#             time.sleep(10 * random())
#             print(2)

#             # Parse the loaded HTML
#             soup = BeautifulSoup(driver.page_source, 'html.parser')
#             image_tags = soup.find_all('img', class_='w-100', srcset=True, src=False)
#             print(3)
#             for img_tag in image_tags:
#                 print(img_tag)
#                 img_url = img_tag['srcset']
#                 # Get the first image URL from the srcset (assuming the default resolution is listed first)
#                 img_url = img_url.split(',')[0].strip().split(' ')[0]

#                 # If the image URL is relative, convert it to an absolute URL
#                 if not img_url.startswith('http'):
#                     img_url = urlparse.urljoin(url, img_url)

#                 # Download and save the image
#                 filename = f"image_{image_count}.jpg"
#                 image_path = os.path.join(download_path, filename)
#                 img_response = requests.get(img_url)
#                 if img_response.status_code == 200:
#                     with open(image_path, 'wb') as f:
#                         f.write(img_response.content)
#                     print(f"Downloaded: {filename}")
#                     image_count += 1
#                     if image_count >= max_images:
#                         break  # Reached the max image count, exit the loop

#             if image_count >= max_images:
#                 break  # Exit the loop if the maximum image count is reached

#             # Scroll down to the bottom of the page
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#     finally:
#         # Close the browser
#         driver.quit()

# if __name__ == "__main__":
#     user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"

#     pacsun_url = "https://www.pacsun.com/mens/graphic-tees/"
#     download_path = "images/PacsunImages"  # The directory will be created if it doesn't exist
#     max_images = 100

#     download_images(pacsun_url, download_path, max_images)


import os
import requests
from bs4 import BeautifulSoup
import urllib.parse as urlparse

# Set the desired user agent string
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"

headers = {
    "User-Agent": user_agent,
    "Accept-Language": "en-US,en;q=0.9",
}

def scrape_images(url, download_path):
    # Create the download directory if it doesn't exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Send an HTTP GET request to the URL
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        image_tags = soup.find_all('img', class_='w-100', srcset=True, src=False)

        i = 0
        for img_tag in image_tags:
            img_url = img_tag['srcset']
            # Get the first image URL from the srcset (assuming the default resolution is listed first)
            img_url = img_url.split(',')[0].strip().split(' ')[0]
            print(img_url)

            # If the image URL is relative, convert it to an absolute URL
            if not img_url.startswith('http'):
                img_url = urlparse.urljoin(url, img_url)

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
            i += 1
    else:
        print(f"Failed to fetch the URL: {url}")

if __name__ == "__main__":
    pacsun_url = "https://www.pacsun.com/mens/graphic-tees/"
    download_path = "images/PacsunImages"  # The directory will be created if it doesn't exist

    scrape_images(pacsun_url, download_path)