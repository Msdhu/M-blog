# _*_ coding: utf-8 _*_
#app包 (文件 app/__init__.py )
#yahoo openid: https://me.yahoo.com/a/e4D0Pd0atdy0GkpV44tCy3lkVHXHKbNFq0DJ4r5DzZ1gti.3G9SGuJVjmJ_FQUutP8LDS4o-
#              https://me.yahoo.com/a/rLKHErU_ufkol36Hx_DkCxWEmAAItZwg2O1BfNtHUxMDDU9tmodWURe0NnmmGfclXWKtdgM-

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir

app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)

# Flask-Login 需要知道哪个视图允许用户登录
lm.login_view = 'login'

# Flask-OpenID 扩展需要一个存储文件的临时文件夹的路径
oid = OpenID(app, os.path.join(basedir, "tmp"))

from app import views, models

if not app.debug:
	import logging
	from logging.handlers import RotatingFileHandler

	file_handler = RotatingFileHandler("tmp/M-blog.log", "a", 1*1024*1024, 10)
	file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
	app.logger.setLevel()
	