from playwright.sync_api import sync_playwright
import pandas as pd
import os
import requests
import time

# 1. Playwright 
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # while headless=True, could not scrap
    page = browser.new_page()
    
    # Trendyol URL, we should initialize the URL which we are scrapping
    url = "https://www.trendyol.com/sr?wb=142700&wc=104025&tag=kirmizi_kampanya_urunu"
    page.goto(url)
    
    # with scrolling, we can obtain more product
    last_height = page.evaluate("document.body.scrollHeight")
    
    while True:
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(3)
        page.evaluate("window.scrollBy(0, -1500)")
        time.sleep(2)
        new_height = page.evaluate("document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    products = page.query_selector_all("div.p-card-wrppr")
    
    os.makedirs("urun_fotolari", exist_ok=True)

    # list of obtained products
    data = []
    
    # Define the selector using the class name of the div containing the products.
    for i, product in enumerate(products, start=1):
        try:
            brand = product.query_selector("span.prdct-desc-cntnr-ttl").inner_text()
        except:
            brand = "Yok"
        try:
            name = product.query_selector("span.prdct-desc-cntnr-name").inner_text()
        except:
            name = "Yok"
        try:
            sub_title = product.query_selector("div.product-desc-sub-container").inner_text()
        except:
            sub_title = "Yok"
        try:
            price = product.query_selector("div.price-item.discounted").inner_text()
        except:
            try:
                price = product.query_selector("div.price-item").inner_text()
            except:
                price = "Yok"
        try:
            link_elem = product.query_selector("a.p-card-chldrn-cntnr")
            link = link_elem.get_attribute("href")
        except:
            link = "Yok"
        try:
            badges = product.query_selector_all("div.badges-wrapper div.product-badge div.name")
            badge_text = ", ".join([b.inner_text() for b in badges]) if badges else "Yok"
        except:
            badge_text = "Yok"
        try:
            img_elem = product.query_selector("div.image-container img.p-card-img")
            img_url = img_elem.get_attribute("src")
            img_data = requests.get(img_url).content
            img_file_name = f"urun_fotolari/urun_{i}.jpg"
            with open(img_file_name, "wb") as handler:
                handler.write(img_data)
        except:
            img_url = "Yok"
            img_file_name = "Yok"
        try:
            color_count = product.query_selector("span.color-variant-count").inner_text()
        except:
            color_count = "1"
        
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
    df.to_excel("trendyol_urunler_playwright.xlsx", index=False)
    print(f"{len(data)} ürün Excel dosyasına yazıldı ve fotoğraflar kaydedildi.")
    
    browser.close()
