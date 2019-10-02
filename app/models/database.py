from run import db
from flask import session
from passlib.hash import sha256_crypt
from datetime import datetime
from app.scraper import Scrape

"""
Veritabanı tablolarımızı oluşturmak için önce tablo classlarını run.py içindeyken uygulamayı 1 kez
çalıştır ve sonra buraya geri ekle.
"""

class User(db.Model):  # ORM içindeki yapıdan todo tablomuzu türetiyoruz
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.Text, nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    verified = db.Column(db.Integer, default=0)


class Feed(db.Model):  # ORM içindeki yapıdan todo tablomuzu türetiyoruz
    username = db.Column(db.String(20), primary_key=True, nullable=False)
    webtekno = db.Column(db.Boolean,default=False, nullable=False)
    shiftdelete = db.Column(db.Boolean,default=False, nullable=False)
    technopat = db.Column(db.Boolean,default=False, nullable=False)
    chiptr = db.Column(db.Boolean,default=False, nullable=False)
    donanimhaber = db.Column(db.Boolean,default=False, nullable=False)
    


def user_register(username,email,password):
    hashed_password = sha256_crypt.encrypt(password)
    newUser=User(username = username, email = email,password=hashed_password)
    newUserFeed=Feed(username = username)
    control_username = User.query.filter_by(username=username).first()
    control_email = User.query.filter_by(email=email).first()

    
    if control_username or control_email: #eğer bu kullanıcı adı veya email veritabanında kayıtlıysa
        return False
    else:
        db.session.add(newUser)
        try:
            db.session.commit()
            db.session.add(newUserFeed)
            db.session.commit()
            return True 

        except Exception as e:
            db.session.rollback()
            db.session.flush()
            return False
    

def user_login(email,password):
    user_info = User.query.filter_by(email=email).first()
    if user_info:
        real_password=user_info.password
        if sha256_crypt.verify(password,real_password):
            session["logged_in"]=True
            session["username"] = user_info.username
            return True
        else:
            return "Yanlış şifre"
    else:
        return "Hesap yok"
    

def get_user_info():
    username = session["username"]

    user = User.query.filter_by(username=username).first()
    website_list = Feed.query.filter_by(username=username).first()

    user_email = user.email

    selected_websites = []
    if website_list.webtekno == True:
        selected_websites.append("webtekno")
    if website_list.shiftdelete == True:
        selected_websites.append("shiftdelete")
    if website_list.technopat == True:
        selected_websites.append("technopat")
    if website_list.donanimhaber == True:
        selected_websites.append("donanimhaber")
    if website_list.chiptr == True:
        selected_websites.append("chiptr")
    
    
    return selected_websites, user_email


def update_feed(webtekno_status,technopat_status,shiftdelete_status,donanimhaber_status,chiptr_status):
    username = session["username"]
    user = Feed.query.filter_by(username=username).first()

    user.webtekno=webtekno_status #değerler true veya false olarak geliyor.
    user.technopat=technopat_status
    user.shiftdelete=shiftdelete_status
    user.donanimhaber=donanimhaber_status
    user.chiptr=chiptr_status
    try:
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        return False

def change_password(old_pw, new_pw):
    username = session["username"]
    user = User.query.filter_by(username=username).first()
    if sha256_crypt.verify(old_pw,user.password):
        if old_pw != new_pw:
            user.password=sha256_crypt.encrypt(new_pw)
            db.session.commit()
            return True
        else:
            return False

def get_feed():
    username = session["username"]
    selected_feeds = Feed.query.filter_by(username=username).first()

    results = [] #scrape edilen tüm feed bu arrayin içinde views.py dosyasına gidiyor. oradan da html'e.

    if selected_feeds.webtekno == True: #denemek için false yap.
        topics = Scrape("webtekno").get_data() 
        if topics != None : results.append(topics)

    if selected_feeds.shiftdelete == True: #ilgili userın veritabanındaki shiftdelete alanı true ise.
        topics = Scrape("shiftdelete").get_data() #shiftdelete verilerini al
        if topics != None : results.append(topics) #eğer site çalışmıyorsa none döner. çalışıyorsa dönen verileri results dizisine at.

    if selected_feeds.technopat == True:
        topics = Scrape("technopat").get_data()
        if topics != None : results.append(topics)

    if selected_feeds.donanimhaber == True:
        topics = Scrape("donanimhaber").get_data()
        if topics != None : results.append(topics)
    
    if selected_feeds.chiptr == True:
        topics = Scrape("chiptr").get_data()
        if topics != None : results.append(topics)

    return results  #elimizdeki maksimum 5 sözlükten oluşan diziyi views.py'ye return ediyoruz.
    


    
    