from flask import current_app as app


class Product:
    def __init__(self, id, name, price, category, available):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.available = available



    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, price, category, available
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_by_name(name):
        rows = app.db.execute('''
SELECT id, name, price, category, available
FROM Products
WHERE name = :name
''',
                              name=name)
        return rows[0][0] if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, price, category, available
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]
    

    

    



    
    


   
            








   