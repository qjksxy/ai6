import requests
from bs4 import BeautifulSoup
import urllib.request



if __name__ == '__main__':
    url = "https://www.bing.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    image_div = soup.find("div", attrs={"id": "bgImgProgLoad"})
    if image_div is not None:
        image_url = image_div["data-ultra-definition-src"]
        image_name = image_url.split("/")[-1]
        urllib.request.urlretrieve(image_url, image_name)
    else:
        print("Error: Cannot find image div")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
