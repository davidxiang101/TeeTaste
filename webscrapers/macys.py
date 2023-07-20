from selenium import webdriver
import os
import urllib
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
folderName = "images/MacysImages"
def scrape_macy_images(url):
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode (no GUI).
    options.add_argument("--disable-gpu")  # Disable GPU acceleration for headless mode.

    driver = webdriver.Chrome()
    driver.get(url)

    try:
        # Wait for the element with class 'pge-img-opt-expr' to be present on the page.
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'pge-img-opt-expr')))

        # Scroll to the bottom of the page to trigger dynamic loading (adjust the number of scrolls as needed).
        for _ in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(5)

        # Wait for the images to load after scrolling.
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'pge-img-opt-expr')))

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        image_urls = []

        div_tags = soup.find_all('div', class_='pge-img-opt-expr ll-search-browse-exp')
        for div_tag in div_tags:
            source_tag = div_tag.find('source')
            if source_tag and 'srcset' in source_tag.attrs:
                image_url = source_tag['srcset'].split(',')[0].split()[0]
                image_urls.append(image_url)

    finally:
        driver.quit()
    
    return image_urls

if __name__ == "__main__":
    macy_url = "https://www.macys.com/shop/mens-clothing/mens-shirts/Pageindex,Productsperpage/2,120?id=20626"
    image_urls = scrape_macy_images(macy_url)
    for idx, image_url in enumerate(image_urls, start=1):
      idx = idx + 126
      try:
        print(f"Image {idx}: {image_url}")
        if not os.path.exists(folderName):
          os.makedirs(folderName)
        filename = "image_{}.jpg".format(idx)
        # Download and save the image
        image_path = os.path.join(folderName, filename)
        urllib.request.urlretrieve(image_url, image_path)
      except:
        print("failed")
