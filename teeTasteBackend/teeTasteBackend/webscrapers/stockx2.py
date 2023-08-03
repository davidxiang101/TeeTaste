import requests
import json


def search():
    url = "https://stockx.com/sneakers"

    headers = {
        "accept": "application/json",
        "accept-encoding": "utf-8",
        "accept-language": "en-GB,en;q=0.9",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "x-requested-with": "XMLHttpRequest",
        "app-platform": "Iron",
        "app-version": "2022.05.08.04",
        "referer": "https://stockx.com/",
    }

    response = requests.get(url=url, headers=headers)
    if response.status_code != 200:
        print(f"Request to {url} returned status code {response.status_code}")
        return str(response.status_code)
    try:
        output = json.loads(response.text)
    except json.JSONDecodeError:
        print(f"Couldn't decode response as JSON: {response.text}")
        return "couldn't decode as JSON"
    if "Products" in output and len(output["Products"]) > 0:
        return output["Products"][0]
    else:
        print("No products in response")
        return "No products in response"


item = search()
print(item)
if item is not None:
    url = item["media"]["imageUrl"]
    print(url)
