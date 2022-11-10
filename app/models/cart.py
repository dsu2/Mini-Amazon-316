from flask import current_app as app


class Cart:

    def __init__(self, uid, pid, pname, sid, num_item):
        self.uid = uid
        self.pid = pid
        self.pname = pname
        self.sid = sid
        self.num_item = num_item

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_added_to_cart
FROM Cart
WHERE id = :id
''',
                              id=id)
        return Cart(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, pid, time_added_to_cart
FROM Cart
WHERE uid = :uid
AND time_added_to_cart >= :since
ORDER BY time_added_to_cart DESC
''',
                              uid=uid,
                              since=since)
        return [Cart(*row) for row in rows]

    @staticmethod
    def get_cart(uid):
        rows = app.db.execute('''
SELECT L.uid, L.pid, T2.name, L.sid, L.num_item
FROM Line_item as L
FULL OUTER JOIN
(SELECT Products.id, Products.name 
FROM Products ) as T2
ON L.pid = T2.id
WHERE L.uid =:uid
LIMIT 50
''',
                              uid=uid)
        return [Cart(*row) for row in rows]

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT L.uid, L.pid, T2.name, L.sid, L.num_item
FROM Line_item as L
JOIN
(SELECT Products.id, Products.name 
FROM Products ) as T2
ON L.pid = T2.id
LIMIT 50
''')
        return [Cart(*row) for row in rows]


