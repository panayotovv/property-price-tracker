from scraper.fetcher import fetch_page
from scraper.parser import parse_data
from database.repository import save_to_db


def run_scraper():
    for page in range(1, 110):
        print("Processing page:", page)
        url = f'https://www.property.bg/bulgaria/region-sofia/sofia-properties/page/{page}/'

        html = fetch_page(url)
        static_data, dynamic_data = parse_data(html)

        if static_data and dynamic_data:
            save_to_db(static_data, dynamic_data)