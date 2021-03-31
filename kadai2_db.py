import MySQLdb
import hashlib


def login(mail, pw):
    salt = search_salt(mail)
    if salt == None:
        return None 

    b_pw = bytes(pw, "utf-8")
    b_salt = bytes(salt, "utf-8")
    hashed_pw = hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 2560).hex()
    result = search_account(mail, hashed_pw)

    return result

def search_salt(mail):
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT salt FROM saito WHERE mail = %s"

    try:
        cur.execute(sql, (mail,))
    except Exception as e:
        print("SQL実行に失敗：" , e)

    result = cur.fetchone()

    cur.close()
    conn.close()

    if result:
        return result[0]

    return None

def search_account(mail, pw):
    conn = get_connection()
    cur = conn.cursor()

    sql = "SELECT mail FROM saito WHERE mail = %s AND pw = %s"

    try:
        cur.execute(sql, (mail,pw))
    except Exception as e:
        print("SQL実行に失敗：" , e)

    result = cur.fetchone()

    cur.close()
    conn.close()

    return result

def getsyohin(syohinId):
    conn = get_connection()
    cur = conn.cursor()

    sql = "select * from syohin where syohinId = %s"

    try:
        cur.execute(sql,(syohinId,))
    except Exception as e:
        print(e)

    result = cur.fetchone()

    cur.close()
    conn.close()

    return result

def kensa(Artist):
    conn = get_connection()
    cur = conn.cursor()

    sql = "select * from syohin where Artist like %s or cdname like %s"
    Art = "%" + Artist + "%"

    try:
        cur.execute(sql,(Art,Art))
    except Exception as e:
        print(e)

    result = cur.fetchall()

    cur.close()
    conn.close()

    if result:
        return result
    
    return None

    return result

def get_connection():
    return MySQLdb.connect(user='root',passwd='riki0413',host='localhost',db='flasktest',charset="utf8")