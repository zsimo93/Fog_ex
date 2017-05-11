#!thesis/DB

from mainDB import Database
from psycopg2.extensions import AsIs


def deleteNode(token):
    db = Database()
    conn = db.connection
    cur = conn.cursor()

    query = "DELETE FROM nodes WHERE id = %(id)s"
    data = {'id': token}
    cur.execute(query, data)
    conn.commit()
    conn.close()


def insertNode(dict):
    db = Database()
    conn = db.connection
    cur = conn.cursor()

    columns = dict.keys()
    values = [dict[col] for col in columns]

    query = "INSERT INTO nodes (%s) VALUES %s"
    cur.execute(query, (AsIs(','.join(columns)), tuple(values)))

    conn.commit()
    conn.close()


def updateResources(token, dict):
    db = Database()
    conn = db.connection
    cur = conn.cursor()

    query = "UPDATE nodes SET cpu = {}, memory = {}" \
            " WHERE id = '{}'".format(dict['memory'], dict['cpu'], token)
    cur.execute(query)

    conn.commit()
    conn.close()


def updateNode(token, col, value):
    db = Database()
    conn = db.connection
    cur = conn.cursor()

    query = "UPDATE nodes SET {} = '{}' WHERE id = '{}'".format(col, value, token)
    cur.execute(query)

    conn.commit()
    conn.close()
