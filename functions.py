import sqlite3

# здесь хранятся данные о предпочтениях пользователя
user_topics = []
user_authors = []
# функция проверяющая по id является ли пользователь старым или новым
def is_new_user(id):
    con = sqlite3.connect("users_db.db")
    cur = con.cursor()

    list_id_users = cur.execute("""SELECT id FROM users""").fetchall()
    con.commit()
    con.close()

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

    salary = salary.replace(' ', '')
    salary = salary.split('-')

    salary_min, salary_max = int(salary[0]), int(salary[1])

    cur.execute(f"""UPDATE users
        SET salary_max = '{salary_max}'
        SET salary_min = '{salary_min}'
        WHERE id = {id}""")
    
    con.commit()
    con.close()

def update_specialization(id, specialization):
    con = sqlite3.connect("users_db.db")
    cur = con.cursor()

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
