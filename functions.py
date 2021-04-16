import sqlite3

# здесь хранятся данные о предпочтениях пользователя
user_topics = []
user_authors = []
# функция проверяющая по id является ли пользователь старым или новым
def is_new_user(id):
    con = sqlite3.connect("users_db.db")
    cur = con.cursor()

    list_id_users = cur.execute("""SELECT id FROM users""").fetchall()

    con.close()

    # если пользователь новый возвращаем True, если старый False
    if id in list_id_users:
        return False
    return True

def add_user(id):
    con = sqlite3.connect("users_db.db")
    cur = con.cursor()

    cur.execute(f"INSERT INTO users(id) VALUES({id})")

    con.close()

    