from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

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
    time.sleep(20)   # when I increased the time, number of written products increased. Because of lazy-load
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# list of obtained products
data = []

# Define the CSS selector using the class name of the div containing the products.
products = browser.find_elements(By.CSS_SELECTOR, "div.p-card-wrppr")

for product in products:
    try:
        brand = product.find_element(By.CSS_SELECTOR, "span.prdct-desc-cntnr-ttl").text
    except:
        brand = "Yok"
    try:
        name = product.find_element(By.CSS_SELECTOR, "span.prdct-desc-cntnr-name").text
    except:
        name = "Yok"
    try:
        price = product.find_element(By.CSS_SELECTOR, "div.price-item.lowest-price-discounted").text
    except:
        price = "Yok"
    try:
        link = product.find_element(By.CSS_SELECTOR, "a.p-card-chldrn-cntnr").get_attribute("href")
    except:
        link = "Yok"

    data.append({
        "Marka": brand,
        "Ürün": name,
        "Fiyat": price,
        "Link": link
    })

# writing excel
df = pd.DataFrame(data)
df.to_excel("trendyol_urunler.xlsx", index=False)
print(f"{len(data)} ürün Excel dosyasına yazıldı: trendyol_urunler.xlsx")

browser.quit()
