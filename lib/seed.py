#!/usr/bin/env python3
from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Company, Dev, Freebie

# Script goes here!

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # clear existing data
    session.query(Freebie).delete()
    session.query(Company).delete()
    session.query(Dev).delete()
    session.commit()

    fake = Faker()

    print("Seeding companies...")
    companies = [
        Company(
            name=fake.company(),
            founding_year=random.randint(1990, 2023)
        )
        for i in range(20)
    ]
    session.bulk_save_objects(companies)
    session.commit()

    print("Seeding devs...")
    devs = [
        Dev(
            name=fake.name()
        )
        for i in range(30)
    ]
    session.bulk_save_objects(devs)
    session.commit()

    # fetch companies and devs from database to get their IDs
    companies = session.query(Company).all()
    devs = session.query(Dev).all()

    print("Seeding freebies...")
    freebie_items = [
        "T-shirt", "Sticker", "Water Bottle", "Laptop Sleeve", 
        "Pen", "Notebook", "USB Drive", "Hat", "Keychain", 
        "Tote Bag", "Mug", "Mousepad", "Lanyard", "Backpack",
        "Hoodie", "Socks", "Phone Stand", "Cable Organizer"
    ]
    
    freebies = [
        Freebie(
            item_name=random.choice(freebie_items),
            value=random.randint(1, 50),
            dev_id=random.choice(devs).id,
            company_id=random.choice(companies).id
        )
        for i in range(100)
    ]
    session.bulk_save_objects(freebies)
    session.commit()

    print("Seeding complete!")