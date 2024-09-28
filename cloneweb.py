import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Function to download a file from a URL
def download_file(url, folder):
    local_filename = os.path.join(folder, os.path.basename(urlparse(url).path))
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return None

# Function to download all static assets from a webpage
def download_assets(soup, base_url, folder):
    assets = []
    # Download CSS files
    for link in soup.find_all('link', rel="stylesheet"):
        asset_url = urljoin(base_url, link['href'])
        assets.append(download_file(asset_url, folder))

    # Download JS files
    for script in soup.find_all('script', src=True):
        asset_url = urljoin(base_url, script['src'])
        assets.append(download_file(asset_url, folder))

    # Download images
    for img in soup.find_all('img', src=True):
        img_url = urljoin(base_url, img['src'])
        assets.append(download_file(img_url, folder))
    
    return assets

# Main function to clone a website
def clone_website(url, folder="cloned_website"):
    # Make the output folder
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Fetch the main page HTML
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to access {url}: {e}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Save the HTML file
    with open(os.path.join(folder, "index.html"), "w", encoding='utf-8') as f:
        f.write(str(soup))

    # Download all the assets (CSS, JS, images)
    download_assets(soup, url, folder)

    print(f"Website cloned in '{folder}' folder.")

# Example usage
if __name__ == "__main__":
    website_url = input("Enter the website URL to clone: ").strip()
    folder_name = input("Enter the folder name to save the clone (or press Enter for default 'cloned_website'): ").strip()
    if not folder_name:
        folder_name = "cloned_website"
    
    clone_website(website_url, folder_name)
