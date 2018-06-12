from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DBmodel import (Base, Customer , Owner , Location )


engine = create_engine('sqlite:///transportation.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine)
session = DBsession()

# Customer Data
cumstomer1 = Customer(first_name="Hossam",
                      last_name="Khaled",
                      email="hossam@gmail.com",
                      password="hossam123",
                      identity="12345678912365",
                      rate=0.0,
                      phone="12345698742",
                      )
session.add(cumstomer1)
session.commit()

cumstomer2 = Customer(first_name="Omar",
                      last_name="Ramzi",
                      email="omar@gmail.com",
                      password="omar123",
                      identity="12345678912365",
                      rate=0.0,
                      phone="12345698742",
                      )
session.add(cumstomer2)
session.commit()

cumstomer3 = Customer(first_name="Sayed",
                      last_name="Ashref",
                      email="sayed@gmail.com",
                      password="sayed123",
                      identity="12345678912365",
                      rate=0.0,
                      phone="12345698742",
                      )
session.add(cumstomer3)
session.commit()

cumstomer4 = Customer(first_name="Khaled",
                      last_name="Ibrahim",
                      email="khaled@gmail.com",
                      password="khaled123",
                      identity="12345678912365",
                      rate=0.0,
                      phone="12345698742",
                      )
session.add(cumstomer4)
session.commit()

owner = Owner(first_name="owner",
                      last_name="owner",
                      email="khed@gmail.com",
                      password="khaled123",
                      identity="12345678912365",
                      rate=0.0,
                      phone="12345698742",
                    )
session.add(owner)
session.commit()

location = Location(lat=11.23,
                    lang=12.556)
session.add(location)
session.commit()

location1 = Location(lat=18.23,lang=177.556)
session.add(location1)
session.commit()



print "dummy data successfully added"
