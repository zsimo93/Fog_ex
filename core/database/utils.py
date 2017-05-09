from mainDB import Database


def deleteNode(token):
    db = Database()
    conn = db.connection
    cur = conn.cursor()

    query = "DELETE FROM nodes WHERE id = %(id)d"
    data = {'id': token}
    cur.execute(query, data)
    conn.commit()
    conn.close()

def insertNode(dict):
    db = Database()
    conn = db.connection
    cur = conn.cursor()

    query = "DELETE FROM nodes WHERE id = %(id)d"
    cur.execute(query, dict)
    conn.commit()
    conn.close()