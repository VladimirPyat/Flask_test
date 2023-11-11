from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, validators
from wtforms.validators import DataRequired, InputRequired
from RWfile import Readfile_tour


class FillF(FlaskForm):
    max_score = 10

    tour_inf = Readfile_tour()
    round_num = tour_inf.num
    data_split = tour_inf.matches

    h_name = [i.split('-')[0] for i in data_split]
    g_name = [i.split('-')[1] for i in data_split]

    h_fields0 = IntegerField(h_name[0], validators=[InputRequired(), validators.NumberRange(min=0, max=max_score)])
    g_fields0 = IntegerField(g_name[0], validators=[InputRequired(), validators.NumberRange(min=0, max=max_score)])

    h_fields1 = IntegerField(h_name[1], validators=[InputRequired(), validators.NumberRange(min=0, max=max_score)])
    g_fields1 = IntegerField(g_name[1], validators=[InputRequired(), validators.NumberRange(min=0, max=max_score)])

    h_fields2 = IntegerField(h_name[2], validators=[InputRequired(), validators.NumberRange(min=0, max=max_score)])
    g_fields2 = IntegerField(g_name[2], validators=[InputRequired(), validators.NumberRange(min=0, max=max_score)])

    h_fields3 = IntegerField(h_name[3], validators=[InputRequired(), validators.NumberRange(min=0, max=max_score)])
    g_fields3 = IntegerField(g_name[3], validators=[InputRequired(), validators.NumberRange(min=0, max=max_score)])

    h_fields4 = IntegerField(h_name[4], validators=[InputRequired(), validators.NumberRange(min=0, max=max_score)])
    g_fields4 = IntegerField(g_name[4], validators=[InputRequired(), validators.NumberRange(min=0, max=max_score)])

    h_fields5 = IntegerField(h_name[5], validators=[InputRequired(), validators.NumberRange(min=0, max=max_score)])
    g_fields5 = IntegerField(g_name[5], validators=[InputRequired(), validators.NumberRange(min=0, max=max_score)])

    h_fields6 = IntegerField(h_name[6], validators=[InputRequired(), validators.NumberRange(min=0, max=max_score)])
    g_fields6 = IntegerField(g_name[6], validators=[InputRequired(), validators.NumberRange(min=0, max=max_score)])

    h_fields7 = IntegerField(h_name[7], validators=[InputRequired(), validators.NumberRange(min=0, max=max_score)])
    g_fields7 = IntegerField(g_name[7], validators=[InputRequired(), validators.NumberRange(min=0, max=max_score)])

    submit = SubmitField("Отправить")
