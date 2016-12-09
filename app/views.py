# _*_ coding: utf-8 _*_

# flask.g 对象在请求整个生命周期中存储和共享数据. flask.session 提供了一个更加复杂的服务对于存储和共享数据.
# 一旦数据存储在会话对象中,在来自同一客户端的现在和任何以后的请求都是可用的. 数据保持在会话中直到会话被明确地删除.
# 为了实现这个,Flask 为我们应用程序中每一个客户端设置不同的会话文件.

from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from datetime import datetime
from .forms import LoginForm, EditForm
from .models import User

# login_required 装饰器. 确保index页面只被已经登录的用户看到
@app.route("/")
@app.route("/index")
@login_required
def index():
	user = g.user
	posts = [
		{"author": user, "body": "Test post1"},
		{"author": user, "body": "Test post2"}
	]

	return render_template("index.html", user = user, posts = posts)

# oid.loginhandle 告诉 Flask-OpenID 这是我们的登录视图函数
@app.route("/login", methods=["GET", "POST"])
@oid.loginhandler
def login():
	# 检查 g.user 是否被设置成一个认证用户
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for("index"))

	form = LoginForm()

	if form.validate_on_submit():
		session["remember_me"] = form.remember_me.data
		return oid.try_login(form.openid.data, ask_for = ["nickname", "email"])

	return render_template("login.html", form = form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("login"))

# OpenID 认证异步发生. 如果认证成功的话,Flask-OpenID 将会调用一个注册了 oid.after_login 装饰器的函数. 如果失败的话,用户将会回到登陆页面
@oid.after_login
def after_login(resp):
	if resp.email is None or resp.email == "":
		flash('Invalid login. Please try again.')
		return redirect(url_for('login'))

	user = User.query.filter_by(email = resp.email).first()

	if user is None:
		nickname = resp.nickname
		if nickname is None or nickname == "":
			nickname = resp.email.split('@')[0]

		user = User(nickname = nickname, email = resp.email)
		db.session.add(user)
		db.session.commit()

	remember_me = False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)

	login_user(user, remember = remember_me)

	return redirect(request.args.get('next') or url_for('index'))

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

# 任何使用了 before_request 装饰器的函数在接收请求之前都会运行
# 全局变量 current_user 是被 Flask-Login 设置的,因此我们只需要把它赋给 g.user,让访问起来更方便.
# 有了这个,所有请求将会访问到登录用户,即使在模版里.
@app.before_request
def before_request():
	g.user = current_user
	if g.user.is_authenticated:
		g.user.last_seen = datetime.utcnow()
		db.session.add(g.user)
		db.session.commit()

@app.route("/user/<nickname>")
@login_required
def user(nickname):
	user = User.query.filter_by(nickname = nickname).first()
	if user is None:
		flash("User" + nickname + "not found!")
		return redirect( url_for("index") )
		
	posts = [
		{"author": user, "body": "Test post1"},
		{"author": user, "body": "Test post2"}
	]

	return render_template("user.html", user = user, posts = posts)

@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
	form = EditForm()

	if form.validate_on_submit():
		g.user.nickname = form.nickname.data
		g.user.about_me = form.about_me.data
		db.session.add(g.user)
		db.session.commit()
		flash('Your change have been saved')
		return redirect(url_for("edit"))
	else:
		form.nickname.data = g.user.nickname
		form.about_me.data = g.user.about_me

	return render_template("edit.html", form = form)

@app.errorhandler(404)
def internal_error(error):
	return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template("500.html"), 500