from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os
import requests

# Selenium setup
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--start-maximized")

service = Service("C:\\Users\\sezen\\OneDrive\\Masaüstü\\Selenium\\chromedriver.exe")
browser = webdriver.Chrome(service=service, options=chrome_options)

# Trendyol URL, we should initialize the URL which we are scrapping
url = "https://www.trendyol.com/sr?wb=142700&wc=104025&tag=kirmizi_kampanya_urunu"
browser.get(url)
time.sleep(20)

# with scrolling, we can obtain more product
last_height = browser.execute_script("return document.body.scrollHeight")

while True:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    browser.execute_script("window.scrollBy(0, -1500);")
    time.sleep(2)
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# list of obtained products
data = []

# Define the CSS selector using the class name of the div containing the products.
os.makedirs("urun_fotolari", exist_ok=True)

products = browser.find_elements(By.CSS_SELECTOR, "div.p-card-wrppr")

for i, product in enumerate(products, start=1):
    try:
        brand = product.find_element(By.CSS_SELECTOR, "span.prdct-desc-cntnr-ttl").text
    except:
        brand = "Yok"
    try:
        name = product.find_element(By.CSS_SELECTOR, "span.prdct-desc-cntnr-name").text
    except:
        name = "Yok"
    try:
        sub_title = product.find_element(By.CSS_SELECTOR, "div.product-desc-sub-container").text
    except:
        sub_title = "Yok"
    try:
        price = product.find_element(By.CSS_SELECTOR, "div.price-item.discounted").text
    except:
        price = "Yok"
    try:
        link = product.find_element(By.CSS_SELECTOR, "a.p-card-chldrn-cntnr").get_attribute("href")
    except:
        link = "Yok"
    try:
        badges = product.find_elements(By.CSS_SELECTOR, "div.badges-wrapper div.product-badge")
        badge_names = [b.find_element(By.CSS_SELECTOR, "div.name").text for b in badges]
        badge_text = ", ".join(badge_names) if badge_names else "Yok"
    except:
        badge_text = "Yok"
    
    # Downloading images
    try:
        img_elem = product.find_element(By.CSS_SELECTOR, "div.image-container img.p-card-img")
        img_url = img_elem.get_attribute("src")
        img_data = requests.get(img_url).content
        img_file_name = f"urun_fotolari/urun_{i}.jpg"
        with open(img_file_name, "wb") as handler:
            handler.write(img_data)
    except:
        img_url = "Yok"
        img_file_name = "Yok"
    try:
        color_count = product.find_element(By.CSS_SELECTOR, "span.color-variant-count").text
    except:
        color_count = "1"  # If not, except '1'

    data.append({
        "Marka": brand,
        "Ürün": name,
        "Açıklama": sub_title,
        "Fiyat": price,
        "Link": link,
        "Rozetler": badge_text,
        "Fotoğraf_URL": img_url,
        "Fotoğraf_Dosya": img_file_name,
        "Renk_Seçenek_Sayısı": color_count
    })

# writing excel
df = pd.DataFrame(data)
df.to_excel("trendyol_urunler.xlsx", index=False)
print(f"{len(data)} ürün Excel dosyasına yazıldı ve fotoğraflar kaydedildi.")

browser.quit()
