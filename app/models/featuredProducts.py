from flask import current_app as app

class FeaturedProduct:
    def __init__(self, id, name, price, category, available, rating):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.available = available
        self.rating=rating

    @staticmethod
    def get_featured():
        rows = app.db.execute('''
SELECT id, name, price, category, available, coalesce(ROUND(AVG(rating),2)::numeric::text, 'NA')
FROM Products
RIGHT OUTER JOIN ProductReviews
ON Products.id=ProductReviews.pid
WHERE available = True
GROUP BY id
ORDER by AVG(rating) DESC
LIMIT 10
''')
        return [FeaturedProduct(*row) for row in rows]

    @staticmethod
    def get_product_list(available, k, category, search, byPrice):
        base = '''
                SELECT id, name, price, category, available, ROUND(AVG(rating),2)
                FROM Products
                LEFT OUTER JOIN ProductReviews
                WHERE available = True
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

        base=base+"GROUP BY id"

        if byPrice == 'Price HightoLow':
            base = base+" ORDER BY price DESC "
        elif byPrice == 'Price LowtoHigh':
            base = base+" ORDER BY price ASC "
        elif byPrice == 'Rating HightoLow':
            base = base+" ORDER BY AVG(rating) DESC NULLS LAST "
        elif byPrice == 'Rating LowtoHigh':
            base = base+" ORDER BY AVG(rating) ASC NULLS LAST "
        else:
            base = base + " ORDER BY id ASC "
        
        if k != "":
            part3 = f"LIMIT {k}"
            base=base+part3

        rows = app.db.execute(base)
        return [FeaturedProduct(*row) for row in rows]  

    @staticmethod
    def get_product_list_with_sid(available, k, category, search, byPrice, sid):
        base = '''
                SELECT id, name, price, category, available, ROUND(AVG(rating),2)
                FROM Products
                RIGHT OUTER JOIN Inventory 
                ON Products.id = Inventory.pid
                LEFT OUTER JOIN ProductReviews
                ON Products.id=ProductReviews.pid
                '''
        part2 = f"WHERE Inventory.sid = {sid} "
        base = base+part2

        if category != "" or search != "":
            if category != 'All Categories':
                base = base+" AND "
            elif search !="":
                    base=base+ " AND "
            
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
        
        base=base+"GROUP BY id"

        if byPrice == 'Price HightoLow':
            base = base+" ORDER BY price DESC "
        elif byPrice == 'Price LowtoHigh':
            base = base+" ORDER BY price ASC "
        elif byPrice == 'Rating HightoLow':
            base = base+" ORDER BY AVG(rating) DESC NULLS LAST "
        elif byPrice == 'Rating LowtoHigh':
            base = base+" ORDER BY AVG(rating) ASC NULLS LAST "
        else:
            base = base + " ORDER BY id ASC "
        
        if k != "":
            part3 = f"LIMIT {k}"
            base=base+part3
        
        rows = app.db.execute(base)
        return [FeaturedProduct(*row) for row in rows] 