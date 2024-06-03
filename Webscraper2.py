import requests
import time
from bs4 import BeautifulSoup

urls = ['https://www.ycombinator.com/companies',
        'https://www.balderton.com/companies/',
        'https://www.indexventures.com/companies/backed/all/',
        'https://octopusventures.com/portfolio/',
        'https://www.amadeuscapital.com/companies/',
        'https://www.bgf.co.uk/portfolio/']

output_file = 'scrapedtext.txt'
# Balderton is using cloudflare - which blocks scraper requests. We need to pretend to be a device.
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36'}


def scrape_pages(urls, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for url in urls:
            response = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(response.content, 'html.parser')
            file.write(soup.get_text(separator='\n', strip=True))
            file.write("\n\n")
            print(f"Data from {url} has been saved to {output_file}")


scrape_pages(urls, output_file)
