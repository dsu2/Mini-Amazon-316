from flask import current_app as app


class PurchaseDetail:
    def __init__(self, purch_id,  total_amount, no_of_items, fulfilled):
        self.purch_id = purch_id
        self. total_amount =  total_amount
        self.no_of_items = no_of_items
        self.fulfilled = fulfilled

    @staticmethod
    def add_purchasedetail(purch_id, total_amount,no_of_items, fulfilled):
        try:
            rows = app.db.execute('''
INSERT INTO PurchasesDetails(purch_id, total_amount, no_of_items, fulfilled)
VALUES(:purch_id, :total_amount, :no_of_items, :fulfilled)
RETURNING pid
''',
                              uid=uid, pid=pid, sid=sid)
            return rows
        except Exception as e:
            print(str(e))
            return None
    
    

    @staticmethod
    def get_by_purchaseid(purch_id):
        rows = app.db.execute('''
SELECT purch_id,  total_amount, no_of_items, fulfilled
FROM PurchasesDetails
WHERE purch_id = :purch_id
''',
                              purch_id=purch_id)
        return [PurchaseDetail(*row) for row in rows]

