import sqlite3


class UserModel:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def json(self):
        return {
            'id': self.id,
            'email': self.email
        }

    def find_by_email(self, email):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM users WHERE email=?'
        result = cursor.execute(query, (email,))
        row = result.fetchone()
        if row:
            self.id = row[0]
            self.email = row[1]
            self.password = row[2]

        connection.close()
        return self

    def find_by_id(self, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM users WHERE id=?'
        result = cursor.execute(query, (_id,))
        row = result.fetchone()
        if row:
            self.id = row[0]
            self.email = row[1]

        connection.close()

    def add_to_db(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'INSERT INTO users VALUES (NULL, ?, ?)'
        cursor.execute(query, (self.email, self.password))

        connection.commit()
        connection.close()


    @classmethod
    def delete_from_db(cls, user_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'DELETE FROM users WHERE id=?'
        cursor.execute(query, (user_id,))
        connection.commit()
        connection.close()
