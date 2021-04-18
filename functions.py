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

def add_topic(id, topic):
    con = sqlite3.connect("users_db.db")
    cur = con.cursor()
    topics = get_topic(id)

    if topic in topics or topic[0] == '/':
        return

    if topics != 'None':
        topics.append(topic)
        topic = topics
        topic = ', '.join(topic)


    cur.execute(f"""UPDATE users
        SET topics = '{topic}'
        WHERE id = {id}""")
    
    con.commit()
    con.close()


def get_topic(id):
    con = sqlite3.connect("users_db.db")
    cur = con.cursor()

    list_topic = cur.execute("""SELECT topics FROM users""").fetchall()

    con.commit()
    con.close()

    if list_topic == [(None,)]:
        return 'None'

    list_topic = list_topic[0][0].split(', ')

    return list_topic
