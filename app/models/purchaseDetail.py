from flask import current_app as app


class PurchaseDetail:
    def __init__(self, id, tot_amt, no_of_items):
        self.id = id
        self.tot_amt = tot_amt
        self.no_of_items = no_of_items


    @staticmethod
    def get_by_purchaseid(id):
        rows = app.db.execute('''
SELECT id, tot_amt, no_of_items
FROM PurchasesDetails
WHERE id = :id
''',
                              id=id)
        return [PurchaseDetail(*row) for row in rows]

