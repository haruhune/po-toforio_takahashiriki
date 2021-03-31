from flask import Flask, render_template, request, redirect, session, url_for
from datetime import timedelta
import string
import random
import kadai1_db
import kadai2_db
import re
app = Flask(__name__)



app.secret_key = "".join(random.choices(string.ascii_letters, k=256))

@app.route("/")
def top():
    return render_template("top.html")

@app.route("/shinki")
def shinki():
    error = request.args.get('error')
    return render_template("shinki.html",error=error)
    
    if "user" in session:
        return render_template("shinki.html")
    else:
        return redirect("/")

@app.route("/login")
def top_page():
    return render_template("index.html")


@app.route("/home", methods=['POST'])
def home():
    mail = request.form.get("mail")
    pw = request.form.get("pw")

    # ログイン認証業務ロジック
    result = kadai2_db.login(mail, pw)

    if result != None:
        session["user"] = True #セッションにキー：user、バリュー：Trueを格納します。
        session.permanent = True #セッションの有効期限有効化
        app.permanent_session_lifetime = timedelta(hours=1) #有効期限の値の設定
        return render_template("itiran.html")
    else:
        return redirect("/")

@app.route("/home", methods=['GET'])
def home_get():
#セッションにログイン情報があるか確認
    if "user" in session:
        return render_template("itiran.html")
    else:
        return redirect("/")

@app.route("/get", methods=['POST'])
def get():
    mail = request.form.get("mail")
    pw = request.form.get("pw")
    name = request.form.get("name")
    jyusyo = request.form.get("jyusyo")
    tel = request.form.get("tel")
    age = request.form.get("age")
    salt = "".join(random.choices(string.ascii_letters, k=20))
    hashed_pw = kadai1_db.hash_pw(pw,salt)

    error = kadai1_db.insert_sql(mail=mail,pw=hashed_pw,jyusyo=jyusyo,tel=tel,name=name,age=age,salt=salt)


    if error == None:
        kadai1_db.send_mail(mail=mail)
        session["user"] = True #セッションにキー：user、バリュー：Trueを格納します。
        session.permanent = True #セッションの有効期限有効化
        app.permanent_session_lifetime = timedelta(hours=1) #有効期限の値の設定
        return render_template("itiran.html")
    else:
        return redirect(url_for('shinki',error=error))

@app.route("/kakunin", methods=['POST'])
def kakunin():
    mail = request.form.get("mail")
    pw = request.form.get("pw")
    jyusyo = request.form.get("jyusyo")
    tel = request.form.get("tel")
    name = request.form.get("name")
    age = request.form.get("age")
    return render_template("kakunin.html",mail=mail,pw=pw,jyusyo=jyusyo,tel=tel,name=name,age=age)

    if "user" in session:
        return render_template("kakunin.html")
    else:
        return redirect("/")

@app.route("/kensakugo")
def kensakugo():
    if "user" in session:
        haru = request.args.get("kensaku")
        kensaku = kadai2_db.kensa(haru)
        return render_template("kensakugo.html",kensaku=kensaku)
    else:
        return redirect("/")
    

@app.route("/syousai", methods=['get'])
def syousai():
    if "user" in session:
        syohinId = int(request.args.get("syohinId"))
        syousai = kadai2_db.getsyohin(syohinId)
        return render_template("syousai.html",checkbgm=None,syohinId=syohinId,Artist=syousai[2],cdname=syousai[3],nedan=syousai[4],img=syousai[5],bgm=syousai[6])
    else:
        return redirect("/")
    
@app.route("/checkbgm")
def checkbgm():
    if "user" in session:
        syohinId = int(request.args.get("syohinId"))
        syousai = kadai2_db.getsyohin(syohinId)
        return render_template("syousai.html",checkbgm='Yes',syohinId=syohinId,Artist=syousai[2],cdname=syousai[3],nedan=syousai[4],img=syousai[5],bgm=syousai[6])
    else:
        return redirect("/")

@app.route("/logout")
def logout():
    session.pop("user", None) #セッションの削除
    return redirect("/")

@app.route("/add")
def add():
    # formからデータの取得
    Artist = request.args.get("Artist")
    cdname = request.args.get("cdname")
    nedan = request.args.get("nedan")
    print(Artist,cdname,nedan)

    # sessionの有効期限の設定
    session.permanent = True    # セッションの有効期限設定(デフォルト3日)
    app.permanent_session_lifetime = timedelta(minutes=30)  # 有効期限の値の設定

    if not "cart" in session:
        product = []
        product.append([Artist,cdname,nedan])
        session["cart"] = product
    else :
        product = session.pop("cart", None)
        product.append([Artist,cdname,nedan])
        session["cart"] = product

    print(session["cart"])

    return render_template("list.html",list=session["cart"])

@app.route("/cart_list")
def cart_list():
    if "cart" in session:
        return render_template("list.html", list=session["cart"])
    else:
        return render_template("not_list.html")

@app.route("/buy")
def buy():
    if "cart" in session:
        product = session.pop("cart", None) # カートの中身削除

        # 実際の購入処理は省略
        print(product)

        return render_template("result.html")
    else:
        return redirect(url_for("error_page"))

@app.route("/error")
def error_page():
    return render_template("error.html")

if __name__ == "__main__":
    app.run(debug=True)