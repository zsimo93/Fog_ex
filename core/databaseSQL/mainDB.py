#!thesis/DB

import psycopg2

class Database():
    ip = 'localhost'
    port = 8080
    username = 'simone'
    password = 'simone'
    connection = None

    def __init__(self):
        host = self.ip  # + ":" + str(self.port)
        self.connection = psycopg2.connect("dbname='template1' user=" + self.username +
                                           " host=" + host + " password=" + self.password)
