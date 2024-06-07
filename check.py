import json
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# Define the database model
Base = declarative_base()
class DataItem(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    family_kor_nm = Column(String)  # Korean name of the family
    family_nm = Column(String)      # Scientific name of the family
    genus_kor_nm = Column(String)   # Korean name of the genus
    genus_nm = Column(String)       # Scientific name of the genus
    img_url = Column(String)        # URL of the image
    plant_nm = Column(String)  # Not recommended general name
    desc = Column(Text)  # Not recommended general name

# Create an SQLite3 engine and bind the session
engine = create_engine('sqlite:////Users/johnnykoo/repos/codespaces-flask/data.db')
Base.metadata.create_all(engine)  # Ensure all tables are created
Session = sessionmaker(bind=engine)
session = Session()

# Check if the data is inserted correctly
query_result = session.query(DataItem).all()
print('how many data we have?', len(query_result))

# Check the last 5 data from my query_result
# last_five_items = query_result[-5:]  # Get the last 5 items
for item in reversed(query_result):
    print("====================")
    print(item.family_kor_nm)
    print(item.family_nm)
    print(item.genus_kor_nm)
    print(item.genus_nm)
    print(item.img_url)
    print(item.plant_nm)
    print(item.desc)
    print("====================")

session.close()