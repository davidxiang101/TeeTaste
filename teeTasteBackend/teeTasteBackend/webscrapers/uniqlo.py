import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import urllib

# Set the desired user agent string
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument(f"user-agent={user_agent}")

# Set up the Chrome driver
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)


# This function will scrape images from the Uniqlo fashion section
def scrapeUniqloFashion(url, folderName, maxImages, timeout_per_image):
    driver.get(url)
    print("Folder Name:", folderName)

    i = 1
    unique_images = set()  # Track unique image URLs

    scroll_without_new_images = 0  # Counter for scrolling without finding new images

    while i <= maxImages:
        try:
            # Find the images with class "fr-ec-image__img"
            images = driver.find_elements(By.CSS_SELECTOR, ".fr-ec-image__img")

            if not images:
                # Increment the counter if no new images are found
                scroll_without_new_images += 1
                if scroll_without_new_images > 5:
                    # Break the loop if there are no new images after scrolling multiple times
                    print(
                        "No new images found after multiple scrolls. Exiting the loop."
                    )
                    break
            else:
                # Reset the counter if new images are found
                scroll_without_new_images = 0

            for image in images:
                if i > maxImages:
                    break

                # Get the image source URL
                image_url = image.get_attribute("src")
                print("Image number", i, ":\n", image_url, "\n")

                if image_url in unique_images:
                    print("Duplicate image. Skipping.")
                    continue

                img_extension = os.path.splitext(image_url)[1].rsplit("?")[0]
                filename = f"image_{i}{img_extension}"

                # Create the folder if it doesn't exist
                if not os.path.exists(folderName):
                    os.makedirs(folderName)

                # Download and save the image with a timeout
                start_time = time.time()
                try:
                    urllib.request.urlretrieve(
                        image_url, os.path.join(folderName, filename)
                    )
                    unique_images.add(image_url)
                except Exception as e:
                    print(f"Error downloading image {i}: {str(e)}")
                finally:
                    elapsed_time = time.time() - start_time

                if elapsed_time > timeout_per_image:
                    print(
                        f"Image {i} took too long to download ({elapsed_time} seconds). Skipping."
                    )
                else:
                    i += 1

            # Scroll to load more images
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight - 200);"
            )
            time.sleep(2)  # Wait for the page to load new images
        except Exception as e:
            print("Error:", str(e))
            break


# Create a folder to store the images
if not os.path.exists("images/UniqloImages"):
    os.makedirs("images/UniqloImages")

maxImages = 500
timeout_per_image = 10  # Timeout in seconds per image

url = "https://www.uniqlo.com/us/en/men/tops"
scrapeUniqloFashion(url, "images/UniqloImages", maxImages, timeout_per_image)

# Close the browser
driver.quit()
