import sqlite3 as sq
async def db_start():
    global db, cur

    db = sq.connect("main.db")
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, name TEXT, count INTEGER, chance INTEGER)")

    db.commit()

async def create_profile(user_id):
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO profile VALUES(?, ?, ?, ?)", (user_id, '', '', 0))
        db.commit()

async def edit_profile(state, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE profile SET  name = '{}' WHERE user_id == '{}'".format(
            data['name'], user_id))
        db.commit()

async def edit_chance(state, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE profile SET  chance = '{}' WHERE user_id == '{}'".format(
            data['chance'], user_id))
        db.commit()

async def new_count(newcount,id) -> None:
    cur.execute("UPDATE profile SET count = count + ? WHERE user_id = ?", (newcount, id,))
    db.commit()
async def name_from_db(id):
    name = cur.execute("SElECT name FROM profile WHERE user_id = ?", (id,)).fetchone()
    return name
async def count_from_db(id):
    count = cur.execute("SElECT count FROM profile WHERE user_id = ?", (id, )).fetchone()
    return count
async def chance_from_db(id):
    chance = cur.execute("SElECT chance FROM profile WHERE user_id = ?", (id, )).fetchone()
    return chance
async def chance_set(id):
    newchance = cur.execute("UPDATE profile SET chance = ? WHERE user_id = ?", (1, id,)).fetchone()
    return newchance

async def get_all():
    all = cur.execute("SELECT * FROM profile").fetchall()
    return all

async def get_all_user(id):
    all = cur.execute("SELECT * FROM profile WHERE user_id = ?", (id,)).fetchall()
    return all