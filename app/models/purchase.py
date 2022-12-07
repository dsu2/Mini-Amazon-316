from flask import current_app as app


class Purchase:
    def __init__(self, id, uid, pid, time_purchased, sid):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.time_purchased = time_purchased
        self.sid = sid

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
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
SELECT id, uid, pid, time_purchased, sid
FROM Purchases
WHERE uid = :uid
ORDER BY time_purchased DESC
''',
                              uid=uid)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased, sid
FROM Purchases
LIMIT 50
''')
        return [Purchase(*row) for row in rows]
    
    @staticmethod
    def get_by_uid_pid(uid, pid):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased, sid
FROM Purchases
WHERE uid = :uid AND pid = :pid
ORDER BY time_purchased DESC
''',
                              uid=uid, pid = pid)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_by_uid_sid(uid, sid):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased, sid
FROM Purchases
WHERE uid = :uid AND sid = :sid
ORDER BY time_purchased DESC
''',
                              uid=uid, sid=sid)
        return [Purchase(*row) for row in rows]
        
    @staticmethod
    def add_purchase(uid,pid,sid):
        try:
            rows = app.db.execute('''
INSERT INTO Purchases(uid,pid,sid)
VALUES(:uid, :pid, :sid)
RETURNING pid
''',
                              uid=uid, pid=pid, sid=sid)
            return rows
        except Exception as e:
            print(str(e))
            return None
    
    @staticmethod
    def add_purchasedetail(uid,pid,sid):
        try:
            rows = app.db.execute('''
INSERT INTO PurchasesDetails(uid,pid,sid)
VALUES(:uid, :pid, :sid)
RETURNING pid
''',
                              uid=uid, pid=pid, sid=sid)
            return rows
        except Exception as e:
            print(str(e))
            return None
    
    