import sqlite3 as sq
async def db_start():
    global db, cur

    db = sq.connect("main.db")
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, name TEXT, count INTEGER, chance INTEGER, id INTEGER, LastData TEXT, DateNow TEXT, username TEXT)")

    db.commit()

async def create_profile(user_id):
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO profile VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (user_id, '', '', '', '', '', '', ''))
        db.commit()

async def edit_profile(state, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE profile SET name = '{}' WHERE user_id == '{}'".format(
            data['name'], user_id))
        db.commit()
async def set_name(name,id):
    cur.execute("UPDATE profile SET name = ? WHERE user_id = ?", (name,id,))
    db.commit()
async def edit_chance(state, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE profile SET  chance = '{}' WHERE user_id == '{}'".format(
            data['chance'], user_id))
        db.commit()

async def new_count(newcount, id):
    cur.execute("UPDATE profile SET count = ? + count WHERE user_id = ?", (newcount, id,))
    db.commit()
async def name_from_db(id):
    name = cur.execute("SElECT name FROM profile WHERE user_id = ?", (id,)).fetchone()
    return name
async def count_from_db(id):
    count = cur.execute("SElECT count FROM profile WHERE user_id = ?", (id, )).fetchone()
    return count
async def get_last_data(id):
    lastdata = cur.execute("SELECT LastData FROM profile WHERE user_id = ?", (id, )).fetchone()
    return lastdata
async def set_last_data(last_data,id):
    cur.execute("UPDATE profile SET LastData = ? WHERE user_id = ?", (last_data, id,))
    db.commit()

async def set_prise_count(count):
    cur.execute("UPDATE profile SET count = count + ?", (count,))
    db.commit()

async def set_username(username,id):
    cur.execute("UPDATE profile SET username = ? WHERE user_id = ?", (username,id,))
    db.commit()

async def get_username():
    username = cur.execute("SElECT username FROM profile ").fetchall()
    return username

async def set_data_now(data_now):
    cur.execute("UPDATE profile SET DateNow = ?", (data_now,))
    db.commit()
async def get_now_date():
    lol = cur.execute("SELECT DateNow FROM profile ").fetchone()
    return lol

async def get_user_id(id):
    user_id = cur.execute("SElECT user_id FROM profile WHERE user_id = ?", (id, )).fetchone()
    return user_id
async def chance_from_db(id):
    chance = cur.execute("SElECT chance FROM profile WHERE user_id = ?", (id, )).fetchone()
    return chance
async def chance_set(id):
    cur.execute("UPDATE profile SET chance = 1 WHERE user_id = ?", (id,)).fetchall()
    db.commit()
async def chance_set_zero(id):
    cur.execute("UPDATE profile SET chance = 0 WHERE user_id = ?", (id,)).fetchone()
    db.commit()

async def get_all():
    all = cur.execute("SELECT ROW_NUMBER() OVER(ORDER BY count DESC) AS id , * FROM profile").fetchall()
    return all

async def com(user_id):
    cur.execute("SELECT ROW_NUMBER() OVER(ORDER BY count DESC) AS id , * FROM profile WHERE user_id = ? " , (user_id,))
    db.commit()
async def get_id(id):
    id = cur.execute("SELECT ID FROM profile WHERE user_id = ?", (id,)).fetchone()
    return id
async def get_all_user(id):
    all = cur.execute("SELECT ROW_NUMBER() OVER(ORDER BY count DESC) AS id , * FROM profile WHERE user_id = ?", (id,)).fetchall()
    return all