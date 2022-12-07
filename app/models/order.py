from flask import current_app as app

class Order:
    def __init__(self, uid, pid, pname, sid, num_item, price, subtotal):
        self.uid = uid
        self.pid = pid
        self.pname = pname
        self.sid = sid
        self.num_item = num_item
        self.price = price
        self.subtotal = subtotal

    @staticmethod
    def get_order(uid):
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
        return [Order(*row) for row in rows]
