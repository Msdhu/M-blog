# _*_ coding: utf-8 _*_

from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm

@app.route("/")
@app.route("/index")

def index():
	user = {"name": "M27", "isAdmin": False}
	articals = [{
		"author": "Msdhu",
		"title": "第一篇文章"
	},{
		"author": "Msdhu",
		"title": "第二篇文章"
	}]

	return render_template("index.html", user = user, articals = articals)

@app.route("/login", methods=["GET", "POST"])
def login():
	user = {"name": "M27", "isAdmin": False}
	form = LoginForm()

	if form.validate_on_submit():
		flash('Login requestd for OpenID = "' + form.openid.data + '", remember_me = ' + str(form.remember_me.data))
		return redirect("/index")

	return render_template("login.html", user = user, form = form)