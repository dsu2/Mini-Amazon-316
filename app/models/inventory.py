from flask import current_app as app

class Order_fulfillment:
    def __init__(self, firstname, uid, address, no_of_items, time_purchased, fulfilled, purch_id):
        self.firstname = firstname
        self.uid = uid
        self.address = address
        self.no_of_items = no_of_items
        self.time_purchased = time_purchased
        self.fulfilled = fulfilled
        self.purch_id = purch_id


    @staticmethod
    def get_orders(sid):
    #         rows = app.db.execute('''
    # SELECT sid, pid, invNum
        # FROM Inventory
        # WHERE sid = :sid
    # ''',
    #                               sid=sid)
    #         return [Inventory(*row) for row in rows]
        rows = app.db.execute('''
        SELECT u.firstname, u.id, u.address, T2.no_of_items, T2.fulfilled, T2.purch_id, T2.time_purchased
        FROM Users as u
        FULL OUTER JOIN
        (SELECT PurchasesDetailed.no_of_items, PurchasesDetailed.fulfilled, T1.purch_id, T1.uid, T1.time_purchased, PurchasesDetailed.sid
        FROM PurchasesDetailed
            FULL OUTER JOIN
            (SELECT Purchases.purch_id, Purchases.uid, Purchases.time_purchased
            FROM Purchases) as T1
            ON PurchasesDetailed.purch_id = T1.purch_id
        WHERE PurchasesDetailed.sid =:sid
        ) as T2 
        ON U.id = T2.uid
        LIMIT 50
        ''',
                          sid=sid)
        return [Order_fulfillment(*row) for row in rows]

    @staticmethod
    def mark_fulfilled(purch_id):
        rows = app.db.execute('''
        UPDATE PurchasesDetailed
        SET fulfilled = TRUE 
        WHERE purch_id =:purch_id
        ''',
                              purch_id=purch_id)
        return

class Inventory:
    """
    This is just a TEMPLATE for Inventory, you should change this by adding or
        replacing new columns, etc. for your design.
    """
    def __init__(self, sid, pid, pname, invNum):
        self.sid = sid
        self.pid = pid
        self.pname = pname
        self.invNum = invNum

    @staticmethod
    def get_by_pid(pid):
        #         rows = app.db.execute('''
        # SELECT sid, pid, invNum
        # FROM Inventory
        # WHERE sid = :sid
        # ''',
        #                               sid=sid)
        #         return [Inventory(*row) for row in rows]
        rows = app.db.execute('''
        SELECT I.sid, I.pid, T2.name, I.invNum
        FROM Inventory as I
        FULL OUTER JOIN
        (SELECT Products.id, Products.name, Products.price
        FROM Products) as T2
        ON I.pid = T2.id
        WHERE I.pid =:pid
        LIMIT 50
        ''',
                              pid=pid)
        return [Inventory(*row) for row in rows]


    @staticmethod
    def get_by_sid(sid):
#         rows = app.db.execute('''
# SELECT sid, pid, invNum
# FROM Inventory
# WHERE sid = :sid
# ''',
#                               sid=sid)
#         return [Inventory(*row) for row in rows]
        rows = app.db.execute('''
    SELECT I.sid, I.pid, T2.name, I.invNum
    FROM Inventory as I
    FULL OUTER JOIN
    (SELECT Products.id, Products.name, Products.price
    FROM Products ) as T2
    ON I.pid = T2.id
    WHERE I.sid =:sid
    LIMIT 50
    ''',
                              sid=sid)
        return [Inventory(*row) for row in rows]



 #   @staticmethod
  #  def get_by_sid(id):
  #      rows = app.db.execute('''
#SELECT uid, pid, count
#FROM Inventory
#WHERE sid = :sid
#''',
#                              id=id)
#        return Inventory(*(rows[0])) if rows else None

    @staticmethod
    def get_all():
        rows = app.db.execute('''
        SELECT I.sid, I.pid, T2.name, I.invNum
        FROM Inventory as I
        FULL OUTER JOIN
        (SELECT Products.id, Products.name,Products.price
        FROM Products ) as T2
        ON I.pid = T2.id
        LIMIT 50
        ''')
        return [Inventory(*row) for row in rows]

    @staticmethod
    def delete(pid, sid):
        print(pid)
        rows = app.db.execute('''
DELETE 
FROM Inventory 
WHERE pid =:pid and sid =:sid
''',
                              pid=pid, sid=sid)
        return

    @staticmethod
    def edit_num_item(pid, sid, num_item):
        rows = app.db.execute('''
        UPDATE Inventory
        SET invNum =:num_item
        WHERE pid =:pid and sid =:sid
        ''',
                              pid=pid, num_item=num_item, sid=sid)
        return

    @staticmethod
    def addInventory(sid, pid, invNum):
        try:
            rows = app.db.execute("""
INSERT INTO Inventory(sid, pid, invNum)
VALUES(:sid, :pid, :invNum)
RETURNING pid
""",
                            sid=sid, pid=pid, invNum=invNum)
            return pid
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def get_seller_id(uid):
        rows = app.db.execute("""
SELECT id
FROM Sellers
WHERE uid = :uid
""",
                              uid=uid)
        if not rows:  # email not found
            return False
        else:
            return rows