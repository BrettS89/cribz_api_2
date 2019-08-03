from services.crib import scrape
import time
from db import db


class CribModel(db.Model):
    __tablename__ = 'cribs'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    name = db.Column(db.String)
    price = db.Column(db.Float(precision=2))
    pictures = db.Column(db.String)
    created_date = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')


    def __init__(self, _id, url, name, price, pictures, user, created_date):
        crib_details = CribModel.get_details(url)
        self.id = _id
        self.url = url
        self.name = crib_details['name']
        self.price = crib_details['price']
        self.pictures = crib_details['pictures']
        self.user_id = user
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
    def get_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def json(self):
        return {
            'id': self.id,
            'url': self.url,
            'name': self.name,
            'price': self.price,
            'pictures': self.pictures.split('|'),
            'user_id': self.user.id,
            'created_date': self.created_date
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_url(cls, url):
        return cls.query.filter_by(url=url).first()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
