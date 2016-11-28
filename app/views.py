# _*_ coding: utf-8 _*_

from flask import render_template
from app import app

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