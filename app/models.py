# _*_ coding: utf-8 _*_

from app import db
from hashlib import md5

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	nickname = db.Column(db.String(64), index = True, unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
	about_me = db.Column(db.String(140))
	last_seen = db.Column(db.DateTime)
	
	#建立和Post表的关系
	posts = db.relationship("Post", backref = "author", lazy = "dynamic")

	def __repr__(self):
		return "<User {}>".format(self.nickname)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.id)

	def avatar(self, size):
		return "http://www.gravatar.com/avatar/" + md5(self.email.encode('utf-8')).hexdigest() + "?d=mm&s=" + str(size)


class Post(db.Model):
	#主键
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	#外键
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

	def __repr__(self):
		return "<Post {}>".format(self.body)
