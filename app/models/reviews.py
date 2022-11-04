from flask import current_app as app


class ProductReview:
    """
    This is just a TEMPLATE for Review, you should change this by adding or 
        replacing new columns, etc. for your design.
    """
    def __init__(self, pid, uid, text, numPos, numNeg, time_purchased):

        self.pid = pid
        self.uid = uid
        self.text = text
        self.numPos = numPos
        self.numNeg = numNeg
        self.time_purchased = time_purchased

    @staticmethod
    def get(uid, pid):
        rows = app.db.execute('''
SELECT uid, pid, text, numPos, numNeg, time_purchased
FROM ProductReviews
WHERE uid = :uid AND pid = :pid
''',
                              uid =uid, pid = pid)
        return ProductReview(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT uid, pid, text, numPos, numNeg, time_purchased
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
SELECT uid, pid, text, numPos, numNeg, time_purchased
FROM ProductReviews
WHERE uid = :uid
ORDER BY time_purchased DESC
LIMIT 5
''',
                              uid=uid,)
        return [ProductReview(*row) for row in rows]

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT uid, pid, text, numPos, numNeg, time_purchased
FROM ProductReviews
ORDER BY time_purchased DESC
LIMIT 50
'''
                              )
        return [ProductReview(*row) for row in rows]