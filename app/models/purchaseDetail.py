from flask import current_app as app


class PurchaseDetail:
    def __init__(self, purch_id,  total_amount, no_of_items):
        self.purch_id = purch_id
        self. total_amount =  total_amount
        self.no_of_items = no_of_items


    @staticmethod
    def get_by_purchaseid(purch_id):
        rows = app.db.execute('''
SELECT purch_id,  total_amount, no_of_items
FROM PurchasesDetails
WHERE purch_id = :purch_id
''',
                              purch_id=purch_id)
        return [PurchaseDetail(*row) for row in rows]

