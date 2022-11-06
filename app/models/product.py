from flask import current_app as app


class Product:
    def __init__(self, id, name, price, available):
        self.id = id
        self.name = name
        self.price = price
        self.available = available

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, price, available
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, price, available
FROM Products
WHERE available = :available
LIMIT 50
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_expensive_k(available, k):
        rows = app.db.execute('''
SELECT id, name, price, available
FROM Products
WHERE available = :available
ORDER BY price DESC
LIMIT :k
''',
                              available=available, 
                              k=k)
        return [Product(*row) for row in rows]




   