# _*_ coding: utf-8 _*_

#config Flask-WTF

CSRF_ENABLED = True
SECRET_KEY = "Msdhu"

#针对我们小型的应用,将采用 sqlite 数据库. sqlite数据库是小型应用的最方便的选择,每一个数据库都是存储在单个文件里
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# SQLALCHEMY_DATABASE_URI 是 Flask-SQLAlchemy 扩展需要的. 这是我们数据库文件的路径
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")

# SQLALCHEMY_MIGRATE_REPO 是文件夹,我们将会把 SQLAlchemy-migrate 数据文件存储在这里
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, "db_repository")
