import requests
from bs4 import BeautifulSoup
import os

def download_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    if not os.path.exists('images'):
        os.makedirs('images')

    for img_tag in img_tags:
        img_url = img_tag['src']
        img_name = img_url.split('/')[-1]
        with open(f'images/{img_name}', 'wb') as f:
            img_response = requests.get(img_url)
            f.write(img_response.content)

url = input("Enter the website URL: ")
download_images(url)
