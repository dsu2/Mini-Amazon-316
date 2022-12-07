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
    def get_by_pid(pid):
        rows = app.db.execute('''
SELECT sid, pid, invNum
FROM Inventory
WHERE pid = :pid
''',
                              pid=pid)
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

    @staticmethod
    def delete(pid):
        print(pid)
        rows = app.db.execute('''
DELETE 
FROM Inventory 
WHERE pid =:pid
''',
                              pid=pid)
        return

    @staticmethod
    def addInventory(sid, pid, invNum):
        try:
            rows = app.db.execute("""
INSERT INTO Inventory(sid, pid, invNum)
VALUES(:sid, :pid, :invNum)
RETURNING pid
""",
                            sid=sid, pid=pid, invNum=invNum)
            return pid
        except Exception as e:
            print(str(e))
            return None


    @staticmethod
    def editInventory(pid,value):
        rows = app.db.execute('''
    UPDATE Inventory
    SET invNum =:value
    WHERE Inventory.pid =:pid
    ''',
                        pid=pid, value=value)
        return
  
