from flask import current_app as app


class Purchase:
    def __init__(self, purch_id, uid, time_purchased):
        self.purch_id = purch_id
        self.uid = uid
        self.time_purchased = time_purchased

    @staticmethod
    def get(purch_id):
        rows = app.db.execute('''
SELECT purch_id, uid, time_purchased
FROM Purchases
WHERE purch_id = :purch_id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT purch_id, uid, time_purchased
FROM Purchases
WHERE uid = :uid
AND time_purchased >= :since
ORDER BY time_purchased DESC
LIMIT 50
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_by_uid(uid):
        rows = app.db.execute('''
SELECT purch_id, uid, time_purchased
FROM Purchases
WHERE uid = :uid
ORDER BY time_purchased DESC
''',
                              uid=uid)
        return [Purchase(*row) for row in rows]

    
    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT purch_id, uid, time_purchased
FROM Purchases
LIMIT 50
''')
        return [Purchase(*row) for row in rows]

    @staticmethod
    def add_purchase(uid):
        try:
            rows = app.db.execute('''
INSERT INTO Purchases(uid)
VALUES(:uid)
RETURNING uid
''',
                              uid=uid)
            
            return rows
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def get_latest_purch_id(uid):
        try:
            rows = app.db.execute('''
SELECT purch_id
FROM Purchases 
WHERE time_purchased = 
(SELECT MAX(time_purchased) FROM Purchases)


''',
                                uid=uid)
            return rows
        except Exception as e:
            print(str(e))
            return None
                            