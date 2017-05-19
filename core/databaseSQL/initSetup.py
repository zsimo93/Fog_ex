import mainDB


def setup():
    db = mainDB.Database()
    cur = db.connection.cursor()

    cur.execute("CREATE TYPE role_type AS ENUM ('MASTER', 'NODE', 'BACKUP')")
    cur.execute("CREATE TYPE arch_type AS ENUM ('ARM', 'x86')")
    cur.execute(''' CREATE TABLE nodes
                    (id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    ip TEXT NOT NULL,
                    role role_type NOT NULL,
                    architecture arch_type NOT NULL,
                    mqtt_Topic TEXT NOT NULL,
                    cpu REAL NOT NULL,
                    memory REAL NOT NULL)''')

    cur.execute(''' CREATE TABLE actions
                    (id TEXT PRIMARY KEY,
                    name TEXT,
                    uri TEXT)''')

    db.connection.commit()
    db.connection.close()
