from flask import current_app as app
from datetime import datetime
from decimal import Decimal


class ProductReview:
    """
    This is just a TEMPLATE for Review, you should change this by adding or 
        replacing new columns, etc. for your design.
    """
    def __init__(self, pid, uid, text, rating, numPos, numNeg, time_purchased):

        self.pid = pid
        self.uid = uid
        self.text = text
        self.rating= rating
        self.numPos = numPos
        self.numNeg = numNeg
        self.time_purchased = time_purchased

    @staticmethod
    def get(uid, pid):
        rows = app.db.execute('''
SELECT uid, pid, text, rating, numPos, numNeg, time_purchased
FROM ProductReviews
WHERE uid = :uid AND pid = :pid
''',
                              uid =uid, pid = pid)
        return ProductReview(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT uid, pid, text, rating, numPos, numNeg, time_purchased
FROM ProductReviews
WHERE uid = :uid
AND time_purchased >= :since
ORDER BY time_purchased DESC
''',
                              uid=uid,
                              since=since)
        return [ProductReview(*row) for row in rows]

    @staticmethod
    def get_5_recent_uid(uid):
        rows = app.db.execute('''
SELECT uid, pid, text, rating, numPos, numNeg, time_purchased
FROM ProductReviews
WHERE uid = :uid
ORDER BY time_purchased DESC
LIMIT 5
''',
                              uid=uid,)
        return [ProductReview(*row) for row in rows]

    @staticmethod
    def get_all_by_pid(pid):
        rows = app.db.execute('''
SELECT uid, pid, text, rating, numPos, numNeg, time_purchased
FROM ProductReviews
WHERE pid = :pid
ORDER BY time_purchased DESC
''',
                              pid=pid)
        return [ProductReview(*row) for row in rows]


    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT uid, pid, text, rating, numPos, numNeg, time_purchased
FROM ProductReviews
ORDER BY time_purchased DESC
LIMIT 50
'''
                              )
        return [ProductReview(*row) for row in rows]

    @staticmethod
    def addProductReview(pid, uid, text, rating):
        try:
            rows = app.db.execute("""
INSERT INTO ProductReviews(uid, pid, text, rating, numPos, numNeg, time_purchased)
VALUES(:uid, :pid, :text, :rating, 0, 0, :time_purchased)
RETURNING pid, uid
""",
                                  pid = pid,
                                  uid = uid,
                                  text = text, rating = rating, time_purchased = datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return e


    @staticmethod
    def editProductReview(pid, uid, text, rating):
        try:
            rows = app.db.execute("""
UPDATE ProductReviews
SET text = :text, rating = :rating, time_purchased = :time_purchased
WHERE pid = :pid AND uid = :uid
""",
                                  pid = pid,
                                  uid = uid,
                                  text = text, rating = rating, time_purchased = datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return e


    @staticmethod
    def removeProductReview(uid, pid):
        try:
            rows = app.db.execute("""
DELETE FROM ProductReviews
WHERE pid = :pid AND uid = :uid
""",
                                  pid = pid,
                                  uid = uid,
                                  )
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return e


    @staticmethod
    def findAvgRating(pid):
        rows = app.db.execute("""
SELECT AVG(rating) 
FROM ProductReviews
WHERE pid = :pid
""",
                                pid = pid)
        return rows[0][0]
        
    
    @staticmethod
    def findNumReview(pid):
        rows = app.db.execute("""
SELECT COUNT(*) FROM ProductReviews
WHERE pid = :pid
""",
                                  pid = pid
                                  )
        return rows[0][0]
        