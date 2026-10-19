import urllib.request
import os

def download_logo():
    # Official Google Noto Emoji 512x512 high-resolution PNG for 1F4B8 (Money with Wings)
    url = "https://fonts.gstatic.com/s/e/notoemoji/latest/1f4b8/512.png"
    target_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
    
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)
    
    print(f"Downloading high-resolution emoji logo from {url}...")
    with urllib.request.urlopen(req, timeout=10) as response:
        image_data = response.read()
        
    with open(target_path, "wb") as f:
        f.write(image_data)
        
    print(f"Successfully saved {len(image_data)} bytes to {target_path}")

if __name__ == "__main__":
    download_logo()
