import sqlite3

conn = None

def log_error(error):
    f = open('app_errors.log', 'a')
    f.write(error + '\n')
    f.close()

def get_connection():
    global conn
    if conn is None:
        conn = sqlite3.connect("database.db")
    return conn

def check_database():
    try:
        c = get_connection().cursor()
        c.execute('CREATE TABLE IF NOT EXISTS culturas (id INTEGER PRIMARY KEY, cultura TEXT)')
        c.execute(
            'CREATE TABLE IF NOT EXISTS areas ('
            'id INTEGER PRIMARY KEY, '
            'id_cultura INTEGER, '
            'figura TEXT, '
            'largura INTEGER, '
            'comprimento INTEGER, '
            'base INTEGER, '
            'altura INTEGER, '
            'raio INTEGER, '
            'base_menor INTEGER, '
            'area INTEGER'
            ')')
        get_connection().commit()
    except Exception as e:
        log_error(str(e))

def query(stmt) -> list:
    try:
        c = get_connection().cursor()
        c.execute(stmt)
        return c.fetchall()
    except Exception as e:
        log_error(str(e))

def run(stmt, params):
    try:
        c = get_connection().cursor()
        c.execute(stmt, params)
        get_connection().commit()
    except Exception as e:
        log_error(str(e))

def close_connection():
    global conn
    try:
        get_connection().close()
        conn = None
    except Exception as e:
        conn = None
        log_error(str(e))
