import os
import pymysql

def conn():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "db"), port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "refound"), password=os.getenv("DB_PASSWORD", "refound"),
        database=os.getenv("DB_NAME", "refound"), charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor, autocommit=True)

def query(sql, params=()):
    c = conn()
    try:
        with c.cursor() as cur:
            cur.execute(sql, params)
            return list(cur.fetchall())
    finally:
        c.close()
