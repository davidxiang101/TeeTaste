from bs4 import BeautifulSoup
import requests
import os


def save_image_from_url(image_url, destination_folder, image_name):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    response = requests.get(image_url, stream=True)
    response.raise_for_status()

    filename = os.path.join(destination_folder, image_name + ".jpg")

    with open(filename, "wb") as out_file:
        out_file.write(response.content)
    print(f"Saved image {filename}")


def scrape_stockx_images(page_url, destination_folder):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    }
    response = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    img_tags = soup.find_all("img", class_="chakra-image")

    downloaded_images = set()
    counter = 1
    for img in img_tags:
        image_url = img.get("src")
        if image_url not in downloaded_images:
            image_name = "sneaker" + str(counter)
            save_image_from_url(image_url, destination_folder, image_name)
            downloaded_images.add(image_url)
            counter += 1


scrape_stockx_images("https://stockx.com/sneakers", "sneaker_images")
