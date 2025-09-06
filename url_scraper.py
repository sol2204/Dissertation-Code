"""
URL Scraper for People's Daily English Website
----------------------------------------------
This script uses Selenium + BeautifulSoup to scrape article URLs
containing the keyword '朝鲜' (North Korea) from People's Daily.
It saves the collected URLs into a CSV file.

Pipeline:
1. Open the listing page with Selenium.
2. User manually navigates to the first desired page.
3. Script extracts article URLs from each page.
4. User manually clicks "Next" between pages when prompted.
5. URLs are saved to 'article_urls.csv'.
"""

import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------
# Setup Selenium WebDriver
# ---------------------------------------------------------------------
options = Options()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/89.0.4389.82 Safari/537.36"
)

service = Service(
    executable_path="C:/Users/sol stappard/Desktop/chrome driver/chromedriver.exe"
)
driver = webdriver.Chrome(service=service, options=options)

# Track already scraped URLs to avoid duplicates
scraped_urls = set()


# ---------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------
def get_page_content_selenium():
    """Fetch page content with Selenium and return BeautifulSoup object."""
    time.sleep(5)  # Wait for page to load
    return BeautifulSoup(driver.page_source, "html.parser")


def extract_article_links(soup):
    """Extract article links containing '朝鲜' in title or snippet. THIS IS CURRENTLY SET UP TO LOOK AT NORTH KOREA - BUT IN MY DISSERTATION I LOOKED AT JAPAN"""
    article_links = []

    for article_tag in soup.select('a[href*="people.com.cn"]'):
        article_link = article_tag["href"]
        article_text = article_tag.get_text()
        snippet_tag = article_tag.find_next("div", class_="abs")

        if (
            article_link not in scraped_urls
            and (
                "朝鲜" in article_text
                or (snippet_tag and "朝鲜" in snippet_tag.get_text())
            )
        ):
            article_links.append(article_link)
            scraped_urls.add(article_link)

    return article_links


def save_urls_to_csv(urls, file_name="article_urls.csv"):
    """Save extracted URLs to a CSV file."""
    with open(file_name, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["url"])  # Write header once
        for url in urls:
            writer.writerow([url])
    print(f"URLs added to {file_name}")


def scrape_all_pages_selenium(start_url, max_pages=100):
    """Scrape multiple pages with manual user control."""
    page_number = 1
    driver.get(start_url)

    print("Opening the main article listing page...")
    input("Navigate to the first page you want to scrape, then press Enter...")

    while page_number <= max_pages:
        print(f"Scraping page {page_number}...")
        soup = get_page_content_selenium()
        article_links = extract_article_links(soup)

        save_urls_to_csv(article_links)
        print("Articles added to CSV")

        user_choice = input(
            "Continue to next page? Type 'yes' to continue or 'no' to stop: "
        ).strip().lower()
        if user_choice == "no":
            print("Stopping the scraping process...")
            break
        else:
            input("Manually click the 'Next' button, then press Enter...")

        page_number += 1


# ---------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------
if __name__ == "__main__":
    start_url = "http://en.people.cn/518256/index.html"
    max_pages = 100

    scrape_all_pages_selenium(start_url, max_pages)
    driver.quit()
