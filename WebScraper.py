import requests
from bs4 import BeautifulSoup
import pandas as pd

# List of VC websites
url = 'https://www.balderton.com/companies/'
#Balderton is using cloudflare - which blocks scraper requests. We need to pretend to be a device.
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

def scrape_vc_portfolio(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    portfolio_data = []
    for investment in soup.find_all('div', class_='col-md-6 col-lg-4 js-shuffle-item'):
        # Extract name
        name_tag = investment.find('h3')
        name = name_tag.text.strip() if name_tag else None

        # Extract description
        description_tag = investment.find('p')
        description = description_tag.text.strip() if description_tag else None

        stage_date_tag = investment.find('span', class_='label-m fw-medium')
        if stage_date_tag:
            stage_date = stage_date_tag.text.strip()
            if ', ' in stage_date:
                stage, date_of_investment = stage_date.split(', ')
            elif ' in ' in stage_date:
                stage, date_of_investment = stage_date.split(' in ')
            else:
                stage, date_of_investment = stage_date, None
        else:
            stage, date_of_investment = None, None

        # Extract location
        location_tag = investment.find('span', class_='label-M d-block mb-auto')
        location = location_tag.text.strip() if location_tag else None

        portfolio_data.append({
            'Name': name,
            'Description': description,
            'Stage': stage,
            'Date of Investment': date_of_investment,
            'Location': location,
        })

    return portfolio_data


portfolio_data = scrape_vc_portfolio(url)

# Convert to DataFrame and export to CSV
df = pd.DataFrame(portfolio_data)
df.to_csv('vc_portfolio.csv', index=False)

print("Scraping completed and data saved to vc_portfolio.csv")
