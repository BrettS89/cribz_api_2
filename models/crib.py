import sqlite3
from services.crib import scrape
import time


class CribModel:
    def __init__(self, _id, url, name, price, pictures, user, created_date):
        crib_details = CribModel.get_details(url)
        self.id = _id
        self.url = url
        self.name = crib_details['name']
        self.price = crib_details['price']
        self.pictures = crib_details['pictures']
        self.user = user
        self.created_date = created_date

    @classmethod
    def from_url(cls, url, user):
        c = CribModel.get_details(url)
        millis = int(round(time.time() * 1000))
        return CribModel(None, url, c['name'], c['price'], c['pictures'], user, millis)

    @classmethod
    def get_details(cls, url):
        return scrape(url)

    @classmethod
    def get_by_id(self, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM cribs WHERE id=?'
        results = cursor.execute(query, (_id,))
        row = results.fetchone()
        connection.close()

        return CribModel(
            row[0], row[1], row[2], row[3], row[4], row[5], row[6]
            )

    def json(self):
        return {
            'id': self.id,
            'url': self.url,
            'name': self.name,
            'price': self.price,
            'pictures': self.pictures.split('|'),
            'user': self.user,
            'created_date': self.created_date
        }

    def save_to_db(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'INSERT INTO cribs VALUES (NULL, ?, ?, ?, ?, ?, ?)'
        cursor.execute(
            query,
            (self.url,
             self.name,
             self.price,
             self.pictures,
             self.user,
             self.created_date))

        connection.commit()
        connection.close()
        self.get_by_url(self.url)

    def get_by_url(self, url):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM cribs WHERE url=?'
        results = cursor.execute(query, (url,))
        row = results.fetchone()

        self.id = row[0]
        self.url = row[1]
        self.name = row[2]
        self.price = row[3]
        self.pictures = row[4]
        self.user = row[5]
        self.created_date = row[6]

        connection.close()

    def delete_from_db(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'DELETE FROM cribs WHERE id=?'
        cursor.execute(query, (self.id,))
        connection.commit()
        connection.close()
