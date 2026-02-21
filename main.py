from scraper.runner import run_scraper
from database.models import Base
from database.config import engine
from database.repository import get_expensive_properties


def init_db():
    Base.metadata.create_all(bind=engine)


def show_expensive_apartments():
    properties = get_expensive_properties()
    average_price_per_m = calculate_average_price_per_m2(properties)

    for prop in properties:
        print(f"{prop.title} -> {prop.price:,.0f}€ in {prop.location} - {prop.area:,.0f}m²")

    print(f"Average price per m²: {average_price_per_m}€")
    print(f"Total of {len(properties)} Large apartments")


def calculate_average_price_per_m2(properties):
    if not properties:
        return "0.00"

    total_price = sum(p.price for p in properties)
    total_area = sum(p.area for p in properties)

    if total_area == 0:
        return "0.00"

    price_per_m2 = total_price / total_area
    return f"{price_per_m2:,.2f}"

if __name__ == "__main__":
    init_db()
    run_scraper()


