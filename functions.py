import sqlite3

# здесь хранятся данные о предпочтениях пользователя
user_topics = []
user_authors = []
iter_time = 15 # время между запросами


# функция проверяющая по id является ли пользователь старым или новым
def is_new_user(id):
    con = sqlite3.connect("users_db.db")
    cur = con.cursor()

    list_id_users = cur.execute("""SELECT id FROM users""").fetchall()
    con.commit()
    con.close()

    if list_id_users == []:
        return True
    # если пользователь новый возвращаем True, если старый False
    if id in list_id_users[0]:
        return False
    return True


def add_user(id):
    con = sqlite3.connect("users_db.db")
    cur = con.cursor()

    cur.execute(f"INSERT INTO users(id) VALUES({id})")
    con.commit()
    con.close()


def update_salary(id, salary):
    con = sqlite3.connect("users_db.db")
    cur = con.cursor()

    if salary[0] == '/':
        return

    salary_min, salary_max = salary[0], salary[1]

    cur.execute(f"""UPDATE users
        SET salary_max = '{salary_max}', salary_min = '{salary_min}'
        WHERE id = {id}""")

    con.commit()
    con.close()


def update_specialization(id, specialization):
    con = sqlite3.connect("users_db.db")
    cur = con.cursor()

    if specialization[0] == '/':
        return

    cur.execute(f"""UPDATE users
        SET specialization = '{specialization}'
        WHERE id = {id}""")

    con.commit()
    con.close()


def get_salary(id):
    con = sqlite3.connect("users_db.db")
    cur = con.cursor()

    salary = cur.execute("""SELECT salary_max, salary_min FROM users
        WHERE id = {id}""").fetchall()

    con.commit()
    con.close()

    if salary == (None,):
        return 'None'

    salary_min, salary_max = int(salary[0]), int(salary[1])

    return salary_min, salary_max


def get_specialization(id):
    con = sqlite3.connect("users_db.db")
    cur = con.cursor()

    specialization = cur.execute("""SELECT specialization FROM users
        WHERE id = {id}""").fetchall()

    con.commit()
    con.close()

    if specialization == (None,):
        return 'None'

    return specialization


def add_used_id(id, used_id):
    con = sqlite3.connect("users_db.db")
    cur = con.cursor()
    used_id_old = get_used_id(id)

    if used_id in used_id_old or used_id[0] == '/':
        return

    if used_id_old != 'None':
        used_id_old.append(used_id)
        used_id = used_id_old
        used_id = ', '.join(used_id)

    print(topic)
    cur.execute(f"""UPDATE users
        SET used_id = '{used_id}'
        WHERE id = {id}""")
    
    con.commit()
    con.close()


def get_used_id(id):
    con = sqlite3.connect("users_db.db")
    cur = con.cursor()

    list_used_id = cur.execute("""SELECT used_id FROM users""").fetchall()

    con.commit()
    con.close()

    if list_used_id == [(None,)]:
        return 'None'

    list_used_id = list_used_id[0][0].split(', ')

    return list_used_id
