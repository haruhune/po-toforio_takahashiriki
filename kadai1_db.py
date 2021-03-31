import MySQLdb
import hashlib
import random
import string
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def hash_pw(pw, salt):
    b_pw = bytes(pw,"utf-8")
    b_salt = bytes(salt,"utf-8")
    hashed_pw = hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 2560).hex()

    return hashed_pw

def insert_sql(mail,pw,name,jyusyo,tel,age,salt):
    error = None
    conn = MySQLdb.connect(user='root',passwd='riki0413',host='localhost',db='flasktest',charset="utf8")
    cur = conn.cursor()

    sql = "insert into saito values(%s,%s,%s,%s,%s,%s,%s)"

    try:
        cur.execute(sql,(mail,name,jyusyo,tel,age,pw,salt,))
    
    except Exception as e:
        print(e)
        error = "登録できませんでした！(´;ω;｀)"


    
    cur.close()
    conn.commit()
    conn.close()

    return error

def send_mail(mail):
        
    ID = "q.kuizu@gmail.com"
    PASS = "qkadaikadai"
    HOST = "smtp.gmail.com"
    PORT = 587

    
    msg = MIMEMultipart()
    msg.attach(MIMEText("この度はmusicTOWNにご登録していただきありがとうございます。\nあなたにとっていい音楽と巡り合えますように！", "html"))

    
    msg["Subject"] = "登録完了"
    msg["From"] = ID
    msg["To"] = mail

    server=SMTP(HOST, PORT)
    server.starttls()   

    server.login(ID, PASS) 

    server.send_message(msg)    

    server.quit()       
    print("メール送信完了！")

