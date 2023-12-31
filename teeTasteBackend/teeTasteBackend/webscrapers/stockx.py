from selenium import webdriver
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import time
import random
from selenium.webdriver.common.action_chains import ActionChains

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


def slow_scroll_to_bottom(driver):
    # Get the initial and final heights of the page
    initial_height = 0
    final_height = driver.execute_script("return document.body.scrollHeight")

    while final_height != initial_height:
        # Calculate the scroll amount (randomize it a bit for a more natural scroll)
        scroll_amount = random.randint(300, 500)

        # Slow scroll to the bottom of the page
        driver.execute_script(f"window.scrollTo(0, {initial_height});")
        time.sleep(
            random.uniform(1.0, 2.5)
        )  # Add a random delay between each scroll action

        # Update the final_height in case the content dynamically loads and increases the page height
        final_height = driver.execute_script("return document.body.scrollHeight")

        # Update the initial_height with the current scroll position
        initial_height = driver.execute_script(
            f"return Math.min(window.pageYOffset + {scroll_amount}, document.body.scrollHeight);"
        )

        next_button = driver.find_element(By.XPATH, '//a[@aria-label="Next"]')
        if next_button.is_displayed():
            print("Next button is in the viewport.")
            actions = ActionChains(driver)
            # Introduce a random delay before clicking the "Next" button
            delay = random.uniform(2.0, 4.0)  # Random delay between 2 to 4 seconds
            time.sleep(delay)

            actions.move_to_element(next_button)
            delay = random.uniform(3.0, 5.0)
            actions.click().perform()
        else:
            print("Next button is not in the viewport.")

        # Check if we are already near the bottom of the page
        if initial_height >= final_height - 1000:
            break


def scrape_stockx_shoe_images(url):
    options = Options()
    options.add_argument("--disable-gpu")  # Disable GPU acceleration for headless mode.

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Wait for the page to load and render the dynamic content (adjust the wait time as needed).
    driver.implicitly_wait(10)

    unique_images = set()  # Track unique image URLs
    image_urls = []
    for _ in range(2):  # Use an underscore (_) for a variable that won't be used
        time.sleep(1)
        img_elements = driver.find_elements(
            By.CSS_SELECTOR, "img.chakra-image.css-kpfxlo"
        )
        for img_element in img_elements:
            image_url = img_element.get_attribute("src")
            if image_url and image_url not in unique_images:
                image_urls.append(image_url)
                unique_images.add(image_url)

        slow_scroll_to_bottom(driver)

    driver.quit()
    return image_urls


if __name__ == "__main__":
    stockx_url = "https://stockx.com/sneakers"
    image_urls = scrape_stockx_shoe_images(stockx_url)

    for idx, image_url in enumerate(image_urls, start=1):
        idx = idx
        try:
            print(f"Image {idx}: {image_url}")
            if not os.path.exists(folderName):
                os.makedirs(folderName)
            filename = "image_{}.jpg".format(idx)
            # Download and save the image
            image_path = os.path.join(folderName, filename)
            # urllib.request.urlretrieve(image_url, image_path)
            img_response = requests.get(image_url, headers=headers)
            if img_response.status_code == 200:
                with open(image_path, "wb") as f:
                    f.write(img_response.content)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download image from URL: {image_url}")
        except:
            print("failed")
