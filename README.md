Trendyol Product Scraper

This Python script uses Playwright to scrape products from Trendyol. It saves product details to an Excel file and downloads product images locally.

Features: Scrapes brand, name, description, price, link, badges, color count, and image URL.

Downloads product images. Than saves data to trendyol_urunler_playwright.xlsx.

Requirements: Python 3.10+
Packages: playwright, pandas, requests, openpyxl

Run the script: python trendyol_scraper.py

Images are saved in urun_fotolari/.
Data is saved in trendyol_urunler_playwright.xlsx.

Recommendations: headless=False is recommended for successful scraping.

