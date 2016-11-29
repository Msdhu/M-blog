# _*_ coding: utf-8 _*_
#app包 (文件 app/__init__.py )

from flask import Flask

app = Flask(__name__)
app.config.from_object("config")

from app import views 