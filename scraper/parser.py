from datetime import datetime

def parse_data(html):
    static_data = []
    dynamic_data = []

    for prop in html:
        title = prop.find("div", class_="ttl")
        title = title.get_text(strip=True) if title else None

        square = prop.find("div", class_="lst")
        if square:
            square = square.find("i")
            square = square.get_text(strip=True) if square else None
            square = float(square.split(' ')[0]) if square else None

        location = prop.find("div", class_="loc")
        location = location.get_text(separator=" ", strip=True) if location else None
        if location:
            location = location.replace('\xa0', ' ')

        price_div = prop.find("div", class_="prc")
        price = None

        if price_div:
            old_price = price_div.find("s")
            if old_price:
                old_price.extract()

            price = price_div.get_text(strip=True)

        if price:
            price = price.replace('\xa0', ' ')
            if "Rent" in price or "Price" in price:
                continue

            price = price.split('€')[0].replace(',', '').strip()
            price = int(price) if price.isdigit() else None

        link_tag = prop.find("a", class_="lnk")
        link = link_tag["href"] if link_tag else None

        if not link:
            continue

        static_data.append({
            "title": title,
            "location": location,
            "link": link
        })

        dynamic_data.append({
            "link": link,
            "price": price,
            "area": square,
            "scraped_at": datetime.utcnow()
        })

    return static_data, dynamic_data