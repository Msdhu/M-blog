# _*_ coding: utf-8 _*_

from app import app

@app.route("/")
@app.route("/index")

def index():
	return "Hello Flask!"