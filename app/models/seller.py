from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
import sys

from .. import login


class Seller():
    def __init__(self, sid, uid):
        self.id = id
        self.uid = uid
    

    @staticmethod
    def get_sid(uid):
        rows = app.db.execute("""
SELECT id
FROM Sellers
WHERE uid = :uid
""",
                              uid=uid)
        return rows[0][0] if rows else None
        
    @staticmethod
    def get_uid(sid):
        rows = app.db.execute("""
SELECT uid
FROM Sellers
WHERE id = :id
""",
                              id=sid)
        print(rows, file = sys.stdout)
        return rows[0][0] if rows else None

    @staticmethod
    def get_uid(sid):
        rows = app.db.execute("""
SELECT uid
FROM Sellers
WHERE id = :id
""",
                              id=sid)
        return rows[0][0] if rows else None

    @staticmethod
    def registerSeller(uid):
        try:
            rows = app.db.execute("""
INSERT INTO Sellers(uid)
VALUES(:uid)
""",
                                  uid=uid)
            id = rows[0][0]
            return Seller.get(uid)
        except Exception as e:
           
            print(str(e))
            return None

