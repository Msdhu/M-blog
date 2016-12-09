# _*_ coding: utf-8 _*_

from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
	openid = StringField("openid", validators = [DataRequired()])
	remember_me = BooleanField("remember_me", default = False)
	submit = SubmitField('Submit')

class EditForm(Form):
	nickname = StringField("nickname", validators = [DataRequired()])
	about_me = TextAreaField("about_me", validators = [Length(min = 0, max = 140)])
	submit = SubmitField('Submit')