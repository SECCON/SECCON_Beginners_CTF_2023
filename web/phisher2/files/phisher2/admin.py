import os
import re
import pyocr
import requests
from PIL import Image
from selenium import webdriver

APP_URL = os.getenv("APP_URL", "http://localhost:16161/")
FLAG = os.getenv("FLAG", "ctf4b{dummy_flag}")

# read text from image
def ocr(image_path: str):
    tool = pyocr.get_available_tools()[0]
    return tool.image_to_string(Image.open(image_path), lang="eng")


def openWebPage(fileId: str):
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        url = f"file:///var/www/uploads/{fileId}.html"
        driver.get(url)

        image_path = f"./images/{fileId}.png"
        driver.save_screenshot(image_path)
        driver.quit()
        text = ocr(image_path)
        os.remove(image_path)
        return text
    except Exception:
        return None


def find_url_in_text(text: str):
    result = re.search(r"https?://[\w/:&\?\.=]+", text)
    if result is None:
        return ""
    else:
        return result.group()


def share2admin(input_text: str, fileId: str):
    # admin opens the HTML file in a browser...
    ocr_text = openWebPage(fileId)
    if ocr_text is None:
        return "admin: Sorry, internal server error."

    # If there's a URL in the text, I'd like to open it.
    ocr_url = find_url_in_text(ocr_text)
    input_url = find_url_in_text(input_text)

    # not to open dangerous url
    if not ocr_url.startswith(APP_URL):
        return "admin: It's not url or safe url.", ocr_url, input_text

    try:
        # It seems safe url, therefore let's open the web page.
        requests.get(f"{input_url}?flag={FLAG}")
    except Exception:
        return "admin: I could not open that inner link.", ocr_url, input_text
    return "admin: Very good web site. Thanks for sharing!", ocr_url, input_text
