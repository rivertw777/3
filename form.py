from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed

from database import User
from wtforms import StringField, PasswordField, FileField, BooleanField, SelectField
from wtforms.validators import DataRequired, EqualTo


class SignupForm(FlaskForm):
    user_id = StringField('user_id', validators=[DataRequired()])
    user_pw = PasswordField('user_pw', validators=[DataRequired(), EqualTo('re_pw')])
    re_pw = PasswordField('re_pw', validators=[DataRequired()])


class LoginForm(FlaskForm):
    user_id = StringField('user_id', validators=[DataRequired()])
    user_pw = PasswordField('user_pw', validators=[DataRequired()])


class ProductForm(FlaskForm):
    photo = FileField('photo', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    price = StringField('price', validators=[DataRequired()])
    check = BooleanField('check')
    keyword = SelectField('keyword', choices= [('모자','모자'), ('안경','안경'), ('셔츠','셔츠'), ('바지','바지'), ('신발','신발'), ('악세사리','악세사리')])
    descript = StringField('descript', validators=[DataRequired()])