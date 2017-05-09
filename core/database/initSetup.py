import mainDB


def setup():
    db = mainDB.Database()
    cur = db.connection.cursor()

    cur.execute(''' CREATE TABLE nodes
                    (id PRIMARY KEY,
                    name TEXT NOT NULL,
                    ip TEXT NOT NULL,
                    role TEXT NOT NULL,
                    architecture TEXT NOT NULL,
                    mqtt_Topic TEXT NOT NULL,
                    cpu REAL NOT NULL,
                    memory REAL NOT NULL)''')

    cur.execute(''' CREATE TABLE actions
                    (id SERIAL PRIMARY KEY,
                    name TEXT,
                    uri TEXT)''')

    db.connection.commit()
    db.connection.close()
