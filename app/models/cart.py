from flask import current_app as app

class Cart:
    def __init__(self, uid, pid, pname, sid, num_item, price, subtotal):
        self.uid = uid
        self.pid = pid
        self.pname = pname
        self.sid = sid
        self.num_item = num_item
        self.price = price
        self.subtotal = subtotal

    @staticmethod
    def addToCart(uid, pid, sid, num_items):
        try:
            rows = app.db.execute('''
                                INSERT INTO Line_item(uid, pid, sid, num_item)
                                VALUES(:uid, :pid, :sid, :num_items)
                                RETURNING uid
                                ''', uid=uid, pid=pid, sid=sid, num_items=num_items)
            uid = rows[0][0]
            return uid
        except Exception as e:
            print(str(e))
            return None

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
SELECT L.uid, L.pid, T2.name, L.sid, L.num_item, T2.price, L.num_item*T2.price as subtotal
FROM Line_item as L
FULL OUTER JOIN
(SELECT Products.id, Products.name,Products.price
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
SELECT L.uid, L.pid, T2.name, L.sid, L.num_item, T2.price, L.num_item*T2.price as subtotal
FROM Line_item as L
JOIN
(SELECT Products.id, Products.name, Products.price
FROM Products ) as T2
ON L.pid = T2.id
LIMIT 50
''')
        return [Cart(*row) for row in rows]

    @staticmethod
    def delete_item(pid):
        rows = app.db.execute('''
    DELETE 
    FROM Line_item 
    WHERE pid =:pid
    ''',
                              pid=pid)
        return

    @staticmethod
    def edit_num_item(pid, num_item):
        print(pid, num_item)
        rows = app.db.execute('''
    UPDATE Line_item
    SET num_item =:num_item
    WHERE pid =:pid
    ''',
                              pid=pid, num_item=num_item)
        return

