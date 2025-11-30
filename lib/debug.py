#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    companies = session.query(Company).all()
    devs = session.query(Dev).all()
    freebies = session.query(Freebie).all()

    print("\n" + "=" * 60)
    print("TESTING FREEBIE TRACKER")
    print("=" * 60)

    # Test Company methods
    print("\n COMPANY TESTS")
    print("-" * 60)
    company = companies[0]
    print(f"Company: {company.name}")
    print(f"  Freebies given: {len(company.freebies)}")
    print(f"  Devs reached: {len(company.devs)}")
    
    new_freebie = company.give_freebie(devs[0], "Hoodie", 35)
    session.add(new_freebie)
    session.commit()
    print(f"  ✓ Gave new freebie: {new_freebie.item_name} to {devs[0].name}")
    
    oldest = Company.oldest_company()
    print(f"  Oldest company: {oldest.name} (founded {oldest.founding_year})")

    # Test Dev methods
    print("\n DEV TESTS")
    print("-" * 60)
    dev = devs[0]
    print(f"Dev: {dev.name}")
    print(f"  Freebies collected: {len(dev.freebies)}")
    print(f"  Companies visited: {len(dev.companies)}")
   
    if len(dev.freebies) > 0:
        actual_item = dev.freebies[0].item_name
        print(f"  Has '{actual_item}'? {dev.received_one(actual_item)}")
    print(f"  Has 'Unicorn'? {dev.received_one('Unicorn')}")
    
    if len(dev.freebies) > 0:
        freebie_to_give = dev.freebies[0]
        dev.give_away(devs[1], freebie_to_give)
        session.commit()
        print(f"  ✓ Gave away {freebie_to_give.item_name} to {devs[1].name}")

    # Test Freebie methods
    print("\n FREEBIE TESTS")
    print("-" * 60)
    freebie = freebies[0]
    print(f"Freebie: {freebie.item_name}")
    print(f"  Dev: {freebie.dev.name}")
    print(f"  Company: {freebie.company.name}")
    print(f"  Details: {freebie.print_details()}")

    print("\n" + "=" * 60)
    print("✓ ALL TESTS COMPLETED")
    print("=" * 60 + "\n")


    import ipdb; ipdb.set_trace()
