from flask import current_app as app


class Inventory:
    """
    This is just a TEMPLATE for Inventory, you should change this by adding or 
        replacing new columns, etc. for your design.
    """
    def __init__(self, sid, pid, invNum):
        self.sid = sid
        self.pid = pid
        self.invNum = invNum

    @staticmethod
    def get_by_pid(id):
        rows = app.db.execute('''
SELECT sid, pid, invNum
FROM Inventory
WHERE pid = :id
''',
                              id=id)
        return [Inventory(*row) for row in rows]

    @staticmethod
    def get_by_sid(sid):
        rows = app.db.execute('''
SELECT sid, pid, invNum
FROM Inventory
WHERE sid = :sid
''',
                              sid=sid)
        return [Inventory(*row) for row in rows]

 #   @staticmethod
  #  def get_by_sid(id):
  #      rows = app.db.execute('''
#SELECT uid, pid, count
#FROM Inventory
#WHERE sid = :sid
#''',
#                              id=id)
#        return Inventory(*(rows[0])) if rows else None

    @staticmethod
    def get_all():
        rows = app.db.execute('''
SELECT sid, pid, invNum
FROM Inventory
LIMIT 50
''')
        return [Inventory(*row) for row in rows]