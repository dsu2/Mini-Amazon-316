from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, address, city, state, value, image):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.city = city
        self.state = state
        self.image = image
        self.value = value

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname, address, city, state, value, image
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname, address, city, state, image = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, password, firstname, lastname, address, city, state, value, image)
VALUES(:email, :password, :firstname, :lastname, :address, :city, :state, :value, :image)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname, lastname=lastname, address = address, city = city, state = state, value = 0, image = image)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname, address, city, state, value, image
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None

    def editUserName(id, firstname, lastname):
        try:
            rows = app.db.execute("""
UPDATE Users
SET firstname = :firstname, lastname = :lastname
WHERE id = :id
""",
                                  id=id, firstname=firstname, lastname=lastname)

        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return e

    def editUserEmail(id, email):
        try:
            rows = app.db.execute("""
UPDATE Users
SET email = :email  
WHERE id = :id
""",
                                  id=id, email=email)

        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return e  

    def editUserPassword(id, password):
        try:
            rows = app.db.execute("""
UPDATE Users
SET password = :password  
WHERE id = :id
""",
                                  id=id, password=password)

        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return e  
    def editUserAddress(id, address, city, state):
        try:
            rows = app.db.execute("""
UPDATE Users
SET address = :address, city = :city, state = :state  
WHERE id = :id
""",
                                  id=id, address = address, city = city, state = state)

        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return e  


    def editAddBalance(id, amount):
        try:
            rows = app.db.execute("""
UPDATE Users
SET value = value + :amount
WHERE id = :id
""",
                                  id=id, amount = amount)

        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return e  
    def editUserImage(id, image):
        try:
            rows = app.db.execute("""
UPDATE Users
SET image = :image  
WHERE id = :id
""",
                                  id=id, image = image)

        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return e  

    @staticmethod
    def getSid(id):
        rows = app.db.execute("""
SELECT id, uid
FROM Sellers
WHERE uid = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None

    @staticmethod
    def getvalue(id):
        rows = app.db.execute("""
SELECT value
FROM Users
WHERE id = :id
""",
                              id=id)
        return rows[0][0] if rows else None