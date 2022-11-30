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

    @staticmethod
    def addProduct(name, price, category, available, des, image):
        try:
            rows = app.db.execute("""
INSERT INTO Products(name, price, category, available, des, image)
VALUES(:name, :price, :category, :available, :des, :image)
RETURNING id
""",
                                  name = name, price=price, category=category,
                                  available=available, des=des, image=image)
            id = rows[0][0]
            return id
        except Exception as e:
            print(str(e))
            return e
