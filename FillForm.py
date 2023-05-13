from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, validators
from wtforms.validators import DataRequired
from Readfile import Readfile_tour

class FillF(FlaskForm):
    max_score = 10
    h_name = []
    g_name = []
    
    tour_inf = Readfile_tour()
    round_num = tour_inf.num
    data_split = tour_inf.matches

    for i in data_split:
        h_name.append (i.split(':')[0])
        g_name.append (i.split(':')[1])

    h_fields0 = IntegerField(h_name[0], validators=[DataRequired(), validators.NumberRange(min=0, max=max_score)])
    g_fields0 = IntegerField(g_name[0], validators=[DataRequired(), validators.NumberRange(min=0, max=max_score)])
  
    submit = SubmitField("Отправить")
    