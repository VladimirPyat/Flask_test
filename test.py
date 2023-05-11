from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, validators
from wtforms.validators import DataRequired

def Func_1():
    print ('Func_1')
    return

def Func_2():
    Func_1()
    print ('Func_2')
    return

Func_2()