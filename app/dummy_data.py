from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DBmodel import (Base, Customer , Owner , Location , Store )


engine = create_engine('sqlite:///transportation.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine)
session = DBsession()

# Customer Data
cumstomer1 = Customer(first_name="Hossam",
                      last_name="Khaled",
                      email="hossam@gmail.com",
                      identity="12345678912395",
                      rate=0.0,
                      phone="12345690872",
                      )
cumstomer1.hash_password("hossam123")
session.add(cumstomer1)
session.commit()

cumstomer2 = Customer(first_name="Omar",
                      last_name="Ramzi",
                      email="omar@gmail.com",
                      identity="02345678912365",
                      rate=0.0,
                      phone="12345698742",
                      )
cumstomer2.hash_password("omar123")
session.add(cumstomer2)
session.commit()

cumstomer3 = Customer(first_name="Sayed",
                      last_name="Ashref",
                      email="sayed@gmail.com",
                      identity="12333678912365",
                      rate=0.0,
                      phone="456987qeq42",
                      )
cumstomer3.hash_password("sayed123")
session.add(cumstomer3)
session.commit()

cumstomer4 = Customer(first_name="Khaled",
                      last_name="Ibrahim",
                      email="khaled@gmail.com",
                      identity="00045678912",
                      rate=0.0,
                      phone="12345698742aa",
                      )
cumstomer1.hash_password("khaled123")
session.add(cumstomer4)
session.commit()


# Owner Data
owner = Owner(first_name="Adel",
              last_name="Ramzy",
              email="ownmer1@gmail.com",
              identity="a12344478912365",
              rate=0.0,
              phone="a1200098742")
owner.hash_password("khaled123")
session.add(owner)
session.commit()

owner1 = Owner(first_name="Mohamed",
               last_name="Ramzy",
               email="owner2@gmail.com",
               identity="aa12345678912365",
               rate=0.0,
               phone="aa123456a98742")
owner.hash_password("khaled123")
session.add(owner1)
session.commit()

owner3 = Owner(first_name="Omar",
               last_name="Ramzy",
               email="owner3@gmail.com",
               identity="aaa12345678912365",
               rate=0.0,
               phone="aaa123456ssa98742")
owner.hash_password("khaled123")
session.add(owner3)
session.commit()

location = Location(lat=11.23, lang=12.556)
session.add(location)
session.commit()

location1 = Location(lat=18.23, lang=177.556)
session.add(location1)
session.commit()

location2 = Location(lat=177.23, lang=1757.556)
session.add(location2)
session.commit()


# stores data
store = Store(name="Omar Ramzy Store",
              location_id=1,
              owner_id=7,
              type='car')

session.add(store)
session.commit()

store2 = Store(name="Mohamed Ramzy Store",
               location_id=2,
               owner_id=6,
               type='bike')

session.add(store2)
session.commit()

store3 = Store(name="Adel Ramzy Store",
               location_id=3,
               owner_id=5,
               type='car')

session.add(store3)
session.commit()

print "dummy data successfully added"
