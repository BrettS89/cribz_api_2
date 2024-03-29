from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def json(self):
        return {
            'id': self.id,
            'email': self.email
        }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self, user_id):
        db.session.delete(self)
        db.session.commit()
