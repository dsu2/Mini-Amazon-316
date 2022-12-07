from flask import current_app as app
from datetime import datetime
from decimal import Decimal


class ProductReview:
    """
    This is just a TEMPLATE for Review, you should change this by adding or 
        replacing new columns, etc. for your design.
    """
    def __init__(self, uid, pid, text, rating, numPos, numNeg, time_purchased):

        self.uid = uid
        self.pid = pid
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
    def get_all_by_uid(uid):
        rows = app.db.execute('''
SELECT uid, pid, text, rating, numPos, numNeg, time_purchased
FROM ProductReviews
WHERE uid = :uid
ORDER BY time_purchased DESC
''',
                              uid=uid)
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
                                  text = text, rating = rating, time_purchased = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            return rows
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None


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
                                  text = text, rating = rating, time_purchased = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
        
    @staticmethod
    def get_uid_pid(uid, pid):
        rows = app.db.execute('''
SELECT COUNT(*)
FROM Purchases
WHERE uid = :uid AND pid = :pid
''',
                              uid=uid, pid=pid)
        return rows[0][0]


class SellerReview:
    """
    This is just a TEMPLATE for Review, you should change this by adding or 
        replacing new columns, etc. for your design.
    """
    def __init__(self, uid, sid, text, rating, numPos, numNeg, time_written):

        self.uid = uid
        self.sid = sid
        self.text = text
        self.rating= rating
        self.numPos = numPos
        self.numNeg = numNeg
        self.time_purchased = time_written

    @staticmethod
    def get(uid, sid):
        rows = app.db.execute('''
SELECT uid, sid, text, rating, numPos, numNeg, time_written
FROM ProductReviews
WHERE uid = :uid AND sid = :sid
''',
                              uid =uid, sid = sid)
        return SellerReview(*(rows[0])) if rows else None
    
    @staticmethod
    def get_all_by_sid(sid):
        rows = app.db.execute('''
SELECT uid, sid, text, rating, numPos, numNeg, time_written
FROM SellerReviews
WHERE sid = :sid
ORDER BY time_written DESC
''',
                              sid=sid)
        return [SellerReview(*row) for row in rows]


    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT uid, sid, text, rating, numPos, numNeg, time_written
FROM SellerReviews
ORDER BY time_written DESC
LIMIT 50
'''
                              )
        return [SellerReview(*row) for row in rows]

    @staticmethod
    def addSellerReview(sid, uid, text, rating):
        try:
            rows = app.db.execute("""
INSERT INTO SellerReviews(uid, sid, text, rating, numPos, numNeg, time_written)
VALUES(:uid, :sid, :text, :rating, 0, 0, :time_written)
RETURNING sid, uid
""",
                                  sid = sid,
                                  uid = uid,
                                  text = text, rating = rating, time_written = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            return rows
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None


    @staticmethod
    def editSellerReview(sid, uid, text, rating):
        try:
            rows = app.db.execute("""
UPDATE SellerReviews
SET text = :text, rating = :rating, time_written = :time_written
WHERE sid = :sid AND uid = :uid
""",
                                  sid = sid,
                                  uid = uid,
                                  text = text, rating = rating, time_written = datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return e


    @staticmethod
    def removeSellerReview(uid, sid):
        try:
            rows = app.db.execute("""
DELETE FROM SellerReviews
WHERE sid = :sid AND uid = :uid
""",
                                  sid = sid,
                                  uid = uid,
                                  )
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return e


    @staticmethod
    def findAvgRating(sid):
        rows = app.db.execute("""
SELECT AVG(rating) 
FROM SellerReviews
WHERE sid = :sid
""",
                                sid = sid)
        return rows[0][0]
        
    
    @staticmethod
    def findNumReview(sid):
        rows = app.db.execute("""
SELECT COUNT(*) FROM SellerReviews
WHERE sid = :sid
""",
                                  sid = sid
                                  )
        return rows[0][0]
        
    @staticmethod
    def get_uid_sid(uid, sid):
        rows = app.db.execute('''
SELECT COUNT(*)
FROM Purchases
WHERE uid = :uid AND sid = :sid
''',
                              uid=uid, sid=sid)
        return rows[0][0]