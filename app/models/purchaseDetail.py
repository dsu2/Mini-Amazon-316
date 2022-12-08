from flask import current_app as app
import sys

class PurchaseDetail:
    def __init__(self, purch_id, pid, sid, no_of_items, fulfilled, price, subtotal, name):
        self.purch_id = purch_id
        self.pid = pid
        self.sid = sid
        self.no_of_items = no_of_items
        self.fulfilled = fulfilled
        self.price = price 
        self.subtotal = subtotal
        self.name = name



    @staticmethod
    def get_details(purch_id):
        rows = app.db.execute('''
SELECT P.purch_id, P.pid, P.sid, P.no_of_items, P.fulfilled, T2.price, P.no_of_items*T2.price as subtotal, T2.name
FROM PurchasesDetailed as P
JOIN
(SELECT Products.id, Products.name, Products.price
FROM Products ) as T2
ON P.pid = T2.id
WHERE purch_id = :purch_id
''',
                              purch_id=purch_id)
        return [PurchaseDetail(*row) for row in rows]
    
    @staticmethod
    def add_purchasedetail(purch_id, pid, sid, no_of_items,fulfilled):
        try:
            rows = app.db.execute('''
INSERT INTO PurchasesDetailed(purch_id, pid, sid, no_of_items, fulfilled)
VALUES(:purch_id, :pid, :sid, :no_of_items, :fulfilled)
RETURNING purch_id
''',
                            purch_id=purch_id, pid=pid, sid=sid, no_of_items=no_of_items, fulfilled=fulfilled)
            return rows
        except Exception as e:
            print(str(e))
            return None
