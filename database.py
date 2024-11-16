# from sqlalchemy import create_engine, Column, Integer, String, DateTime
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker


# engine = create_engine('sqlite:///databse.sqlite')
# Base = declarative_base()


# class Nail(Base):
#     __tablename__ = 'nail'

#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer)
#     date = Column(DateTime)
#     time = Column(DateTime)
#     service = Column(String)


# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()
