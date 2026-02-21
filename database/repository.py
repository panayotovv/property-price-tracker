from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from database.models import Property, PropertyHistory
from database.config import SessionLocal


def save_to_db(static_data, dynamic_data):
    session = SessionLocal()

    try:
        with session.begin():

            stmt = insert(Property).values(static_data)
            stmt = stmt.on_conflict_do_nothing(index_elements=["link"])
            session.execute(stmt)

            links = [item["link"] for item in static_data]

            properties = session.execute(
                select(Property.id, Property.link)
                .where(Property.link.in_(links))
            ).all()

            link_to_id = {link: pid for pid, link in properties}

            history_objects = []

            for item in dynamic_data:
                property_id = link_to_id.get(item["link"])
                if property_id:
                    history_objects.append(
                        PropertyHistory(
                            property_id=property_id,
                            price=item["price"],
                            area=item["area"],
                            scraped_at=item["scraped_at"]
                        )
                    )

            session.add_all(history_objects)

        print(f"Inserted {len(history_objects)} history rows")

    except Exception as e:
        session.rollback()
        print("Database error:", e)

    finally:
        session.close()

def get_expensive_properties(title=None):
    session = SessionLocal()

    try:
        stmt = select(Property)

        if title is not None:
            stmt = stmt.where(Property.title == title)

        stmt = stmt.where(Property.price.is_not(None))

        stmt = (
            stmt
            .order_by(Property.price.desc())
            .limit(20)
        )

        properties = session.execute(stmt).scalars().all()
        return properties

    finally:
        session.close()




