from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class Seller():
    def __init__(self, id, sid):
        self.id = id
        self.sid = sid
    

    @staticmethod
    def get_sid(uid):
        rows = app.db.execute("""
SELECT id, uid
FROM Sellers
WHERE uid = :uid
""",
                              uid=uid)
        return rows[0][0] if rows else None

    @staticmethod
    def registerSeller(uid):
        try:
            rows = app.db.execute("""
INSERT INTO Sellers(uid)
VALUES(:uid)
RETURNING id
""",
                                  uid=uid)
            id = rows[0][0]
            return Seller.get(id)
        except Exception as e:
           
            print(str(e))
            return None