# _*_ coding: utf-8 _*_

from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(Form):
	openid = StringField("openid", validators = [DataRequired()])
	remember_me = BooleanField("remember_me", default = False)
	submit = SubmitField('Submit')