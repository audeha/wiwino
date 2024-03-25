from sqlalchemy import create_engine, Column, Integer, Float, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

# Define the base class
Base = declarative_base()

# Define ORM classes
class Vintage(Base):
    __tablename__ = 'vintages'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    wine_id = Column(Integer, ForeignKey('wines.id'))
    ratings_average = Column(Float)
    ratings_count = Column(Integer)
    year = Column(Integer)
    price_euros = Column(Float)
    price_discounted_from = Column(Float)
    price_discount_percentage = Column(Float)
    bottle_volume_ml = Column(Integer)

class Wine(Base):
    __tablename__ = 'wines'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_natural = Column(Boolean)
    region_id = Column(Integer, ForeignKey('regions.id'))
    winery_id = Column(Integer, ForeignKey('wineries.id'))
    ratings_average = Column(Float)
    ratings_count = Column(Integer)
    url = Column(String)
    acidity = Column(Float)
    fizziness = Column(Float)
    intensity = Column(Float)
    sweetness = Column(Float)
    tannin = Column(Float)
    user_structure_count = Column(Integer)

class Country(Base):
    __tablename__ = 'countries'
    code = Column(String, primary_key=True)
    name = Column(String)
    regions_count = Column(Integer)
    users_count = Column(Integer)
    wines_count = Column(Integer)
    wineries_count = Column(Integer)
    # Relationships
    regions = relationship("Region", backref="country")
    top_lists = relationship("TopList", backref="country")
    most_used_grapes = relationship("MostUsedGrapes", backref="country")

class Region(Base):
    __tablename__ = 'regions'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    country_code = Column(String, ForeignKey('countries.code'))
    # Relationship
    wines = relationship("Wine", backref="region")

class Winery(Base):
    __tablename__ = 'wineries'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # Relationship
    wines = relationship("Wine", backref="winery")

class Grape(Base):
    __tablename__ = 'grapes'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    wines_count = Column(Integer)
    # Relationship
    most_used_grapes = relationship("MostUsedGrapes", backref="grape")

class TopList(Base):
    __tablename__ = 'toplists'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    country_code = Column(String, ForeignKey('countries.code'))

class VintageTopListRanking(Base):
    __tablename__ = 'vintage_toplists_rankings'
    id = Column(Integer, primary_key=True)
    top_list_id = Column(Integer, ForeignKey('toplists.id'))
    vintage_id = Column(Integer, ForeignKey('vintages.id'))
    rank = Column(Integer)
    previous_rank = Column(Integer)

class MostUsedGrapes(Base):
    __tablename__ = 'most_used_grapes_per_country'
    id = Column(Integer, primary_key=True)
    country_code = Column(String, ForeignKey('countries.code'))
    grape_id = Column(Integer, ForeignKey('grapes.id'))

class Keyword(Base):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # Relationship
    keywords_wine = relationship("KeywordsWine", backref="keyword")

class KeywordsWine(Base):
    __tablename__ = 'keywords_wine'
    id = Column(Integer, primary_key=True)
    keyword_type = Column(String)
    count = Column(Integer)
    keyword_id = Column(Integer, ForeignKey('keywords.id'))
    wine_id = Column(Integer, ForeignKey('wines.id'))
    group_name = Column(String)


# Create engine and bind session
engine = create_engine('sqlite:///vivino.db')


# Now, reflect the tables to make sure the definitions are correct and all relationships are established.
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Clean and preprocess the data
# For example, let's remove wines with a rating count less than 10
for vintage in session.query(Vintage).filter(Vintage.ratings_count < 10):
    session.delete(vintage)

# Commit changes
session.commit()

# Close the session
session.close()
