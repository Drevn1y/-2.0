import sqlite3

con = sqlite3.connect('base.db', check_same_thread=False)
sql = con.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER, name TEXT, number TEXT, location TEXT);""")


# Регистрация
def register(id, name, number, location):
    sql.execute('INSERT INTO users VALUES(?, ?, ?, ?);', (id, name, number, location))
    # Фиксируем изменения
    con.commit()


# Проверка на регистрацию
def checker(id):
    check = sql.execute('SELECT id FROM users WHERE id=?;', (id,))
    if check.fetchone():
        return True
    else:
        return False