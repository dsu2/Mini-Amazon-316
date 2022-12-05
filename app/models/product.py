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

    @staticmethod
    def get_expensive_k(available, k):
        rows = app.db.execute('''
SELECT id, name, price, category, available
FROM Products
WHERE available = :available
ORDER BY price DESC
LIMIT :k
''',
                              available=available, 
                              k=k)
        return [Product(*row) for row in rows] 
    
    @staticmethod
    def get_most_expensive(available):
        rows = app.db.execute('''
SELECT id, name, price, category, available
FROM Products
WHERE available = :available
ORDER BY price DESC
''',
                              available=available)
        return [Product(*row) for row in rows] 

    @staticmethod
    def get_least_expensive(available):
        rows = app.db.execute('''
SELECT id, name, price, category, available
FROM Products
WHERE available = :available
ORDER BY price ASC
''',
                              available=available)
        return [Product(*row) for row in rows] 

    @staticmethod
    def get_category(available, category):
        rows = app.db.execute('''
SELECT id, name, price, category, available
FROM Products
WHERE category LIKE :category
''',
                              available=available,
                              category=category)
        return [Product(*row) for row in rows]
    
    @staticmethod
    def get_search(available, search):
        search = '%'+search+'%'
        rows = app.db.execute('''
SELECT id, name, price, category, available
FROM Products
WHERE name LIKE :search
''',
                              available=available,
                              search=search)
        return [Product(*row) for row in rows]


    @staticmethod
    def get_product_list(available, k, category, search, byPrice):
        base = '''
                SELECT id, name, price, category, available
                FROM Products
                '''

        if category != "" or search != "":
            if category != 'All Categories':
                base = base+" WHERE "
            elif search !="":
                    base=base+ " WHERE "
            

        if category != "":
            if category != 'All Categories':
                part1 = f"category iLIKE '{category}'"
                base = base+part1
            
                    

        if search != "":
            if category != "" and category != 'All Categories':
                base = base+" AND " 
            search = '%'+search+'%'
            part2 = f"name LIKE '{search}'"
            base=base+part2

        if byPrice == 'HightoLow':
            base = base+" ORDER BY price DESC "
        
        elif byPrice == 'LowtoHigh':
            base = base+" ORDER BY price ASC "
        
        else:
            base = base + " ORDER BY id ASC "
        
        if k != "":
            part3 = f"LIMIT {k}"
            base=base+part3
        


        rows = app.db.execute(base)
        return [Product(*row) for row in rows]   
    


   
            








   