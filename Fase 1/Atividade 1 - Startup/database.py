import sqlite3

conn = sqlite3.connect('database.db', check_same_thread=False, timeout=10)

def log_error(error):
    f = open('app_errors.log', 'a')
    f.write(error + '\n')
    f.close()

def get_connection():
    return conn

def check_database():
    try:
        c = conn.cursor()
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
        conn.commit()
    except Exception as e:
        log_error(str(e))

def query(stmt) -> list:
    try:
        c = conn.cursor()
        c.execute(stmt)
        return c.fetchall()
    except Exception as e:
        log_error(str(e))

def run(stmt, params):
    try:
        c = conn.cursor()
        c.execute(stmt, params)
        conn.commit()
    except Exception as e:
        log_error(str(e))

def close_connection():
    try:
        conn.close()
    except Exception as e:
        log_error(str(e))
