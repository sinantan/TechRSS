from run import app
from functools import wraps
from flask import render_template,flash,redirect,logging,session,url_for,request
from .models.database import user_register, user_login, get_feed, get_user_info, update_feed, change_password



#kullanıcı giriş decorator'u. bu yapı tüm decoratorlarda aynı. 
def login_required(f): #bunu kullanıcı girişi gerektiren her sayfada kullanabiliriz.
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if "logged_in" in session:
			return f(*args, **kwargs)
		else:
			flash("Lütfen giriş yap.","warning")
			return redirect(url_for("auth"))
	return decorated_function


def is_logged(f): #kullanıcı giriş yaptıysa login ve register a ulaşmamalı.
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if "logged_in" in session:
			return redirect(url_for("index"))
		else:
			return f(*args, **kwargs)
	return decorated_function



@app.route("/")
@login_required
def index():
	topics = get_feed()
	return render_template("index.html",topics = topics)

@app.route("/auth",methods=["GET","POST"])
@is_logged
def auth():
	if request.method=="POST":
		if request.form.get("login")=="Giriş Yap":
			email = request.form["user_email"]
			password = request.form["user_password"]
			status = user_login(email,password)
			
			if status==True:
				return redirect(url_for("auth"))
			elif status=="Yanlış şifre":
				flash("Hatalı şifre girdiniz.","danger")
				return redirect(url_for("auth"))
			elif status=="Hesap yok":
				flash("Böyle bir hesap yok.","warning")
				return redirect(url_for("auth"))

		elif request.form.get("register")=="Kayıt Ol":
			username = request.form["user_name"]
			email = request.form["user_email"]
			password = request.form["user_password"]
			
			if user_register(username,email,password):
				flash("Başarıyla kayıt olundu! Giriş yapabilirsin.","success")
				return redirect(url_for("auth"))
			else:
				flash("Bir hata meydana geldi.","warning")
				return redirect(url_for("auth"))
	else:
		return render_template("auth.html")


@app.route("/settings",methods=["POST","GET"])
@login_required
def settings():
	if request.method=="POST":
		if request.form.get("save_feed_settings") != None:
			webtekno_status = True if request.form.get("webtekno") != None else False #unchecked = None , checked = on
			technopat_status = True if request.form.get("technopat") != None else False
			shiftdelete_status = True if request.form.get("shiftdelete") != None else False
			donanimhaber_status = True if request.form.get("donanimhaber") != None else False
			chiptr_status = True if request.form.get("chiptr") != None else False

			query_status= update_feed(webtekno_status,technopat_status,shiftdelete_status,donanimhaber_status,chiptr_status)
			if query_status:
				flash("Ayarlarınız kaydedildi.", "success")
			else:
				flash("Bir hata meydana geldi.","danger")
			return redirect(url_for("settings"))

		elif request.form.get("save_password_settings") != None:
			old_password = request.form["oldpassword"]
			new_password = request.form["newpassword"]
			
			if change_password(old_password,new_password):
				flash("Parola başarıyla değiştirildi.","success")
			else:
				flash("Parolaları kontrol ediniz.","warning")
			return redirect(url_for("settings"))
	else:
		selected_websites,user_email = get_user_info()
		return render_template("settings.html",selected_websites=selected_websites,user_email=user_email,all_websites=["webtekno","shiftdelete","chiptr","donanimhaber","technopat"])


@app.route("/logout")
def logout():
	session.clear()
	return redirect(url_for("auth"))