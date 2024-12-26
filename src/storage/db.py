from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from typing import List, Dict

from .base import StorageStrategy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from models.product import Product
from models.base import Base

import configparser

class DBStorageStrategy(StorageStrategy):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.properties')
        database_url = config.get('DEFAULT', 'database_url')

        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        self.init_db()

    def init_db(self):
        Base.metadata.create_all(bind=self.engine)

    def save(self, events: List[Dict[str, str]]):
        db: Session = self.SessionLocal()
        try:
            for event in events:
                product = Product(
                    name=event['name'],
                    price=event['price'],
                    image_url=event['image_url']
                )
                db.add(product)
            db.commit()
            print("Data saved to database")
        except Exception as e:
            db.rollback()
            print(f"Error saving events to database: {e}")
        finally:
            db.close()
