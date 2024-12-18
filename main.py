import requests
from bs4 import BeautifulSoup
import os
import argparse

def download_images(url, folder='images'):
    # Create folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all image tags
    img_tags = soup.find_all('img')

    # Download each image
    for img in img_tags:
        img_url = img.get('src')
        if not img_url:
            continue

        # Handle relative URLs
        if img_url.startswith('//'):
            img_url = 'http:' + img_url
        elif img_url.startswith('/'):
            img_url = url + img_url

        # Get the image filename
        img_name = os.path.join(folder, os.path.basename(img_url))

        # Download and save the image
        img_response = requests.get(img_url)
        img_response.raise_for_status()
        with open(img_name, 'wb') as f:
            f.write(img_response.content)

        print(f'Downloaded {img_name}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download images from a URL.')
    parser.add_argument('url', help='The URL to download images from')
    args = parser.parse_args()

    download_images(args.url)