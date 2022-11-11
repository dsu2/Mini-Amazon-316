from flask import current_app as app

class ProductDetails:
    def __init__(self, id, name, price, category, available, des, image):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.available = available
        self.des = des
        self.image = image

    @staticmethod
    def get_details(id):
        rows = app.db.execute('''
SELECT id, name, price, category, available, des, image
FROM Products
WHERE id = :id 
''',
                              id=id)
        return ProductDetails(*(rows[0])) if rows is not None else None 
