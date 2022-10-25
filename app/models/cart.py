from flask import current_app as app


class Cart:

    def __init__(self, uid, pid, sid, num_item):
        self.uid = uid
        self.pid = pid
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
SELECT uid, pid, sid, num_item
FROM Line_item
WHERE uid = :uid
''',
                              uid=uid)
        return [Cart(*row) for row in rows]

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT uid, pid, sid, num_item
FROM Line_item
LIMIT 50
''')
        return [Cart(*row) for row in rows]