import datetime

from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, SelectField, DateField, TimeField, validators
from wtforms.validators import DataRequired, InputRequired, Optional
from RWfile import Readfile_tour


class FillF(FlaskForm):
    MAX_SCORE = 10

    tour_inf = Readfile_tour()
    round_num = tour_inf.num
    data_split = tour_inf.matches

    h_name = [i.split('-')[0] for i in data_split]
    g_name = [i.split('-')[1] for i in data_split]

    h_fields0 = IntegerField(h_name[0], validators=[InputRequired(), validators.NumberRange(min=0, max=MAX_SCORE)])
    g_fields0 = IntegerField(g_name[0], validators=[InputRequired(), validators.NumberRange(min=0, max=MAX_SCORE)])

    h_fields1 = IntegerField(h_name[1], validators=[InputRequired(), validators.NumberRange(min=0, max=MAX_SCORE)])
    g_fields1 = IntegerField(g_name[1], validators=[InputRequired(), validators.NumberRange(min=0, max=MAX_SCORE)])

    h_fields2 = IntegerField(h_name[2], validators=[InputRequired(), validators.NumberRange(min=0, max=MAX_SCORE)])
    g_fields2 = IntegerField(g_name[2], validators=[InputRequired(), validators.NumberRange(min=0, max=MAX_SCORE)])

    h_fields3 = IntegerField(h_name[3], validators=[InputRequired(), validators.NumberRange(min=0, max=MAX_SCORE)])
    g_fields3 = IntegerField(g_name[3], validators=[InputRequired(), validators.NumberRange(min=0, max=MAX_SCORE)])

    h_fields4 = IntegerField(h_name[4], validators=[InputRequired(), validators.NumberRange(min=0, max=MAX_SCORE)])
    g_fields4 = IntegerField(g_name[4], validators=[InputRequired(), validators.NumberRange(min=0, max=MAX_SCORE)])

    h_fields5 = IntegerField(h_name[5], validators=[InputRequired(), validators.NumberRange(min=0, max=MAX_SCORE)])
    g_fields5 = IntegerField(g_name[5], validators=[InputRequired(), validators.NumberRange(min=0, max=MAX_SCORE)])

    h_fields6 = IntegerField(h_name[6], validators=[InputRequired(), validators.NumberRange(min=0, max=MAX_SCORE)])
    g_fields6 = IntegerField(g_name[6], validators=[InputRequired(), validators.NumberRange(min=0, max=MAX_SCORE)])

    h_fields7 = IntegerField(h_name[7], validators=[InputRequired(), validators.NumberRange(min=0, max=MAX_SCORE)])
    g_fields7 = IntegerField(g_name[7], validators=[InputRequired(), validators.NumberRange(min=0, max=MAX_SCORE)])

    submit = SubmitField("Отправить")

class PreTourForm(FlaskForm):
    _count=0
    MAX_TOUR=30
    tour_num = SelectField('Select Tour Number', coerce=int, validators=[InputRequired()])
    deadline_date = DateField('Deadline Date', validators=[validators.InputRequired()])
    deadline_time = TimeField('Deadline Time', validators=[Optional()])

    def __init__(self, n=1):
        super(PreTourForm, self).__init__()
        self.n = n
        self.tour_num.choices = [(i, str(i)) for i in range(1, self.MAX_TOUR + 1)]
        for i in range(self.n):
            setattr(PreTourForm, f'match_date_{i}', StringField(f'Match {i} Start Date'))
            setattr(PreTourForm, f'h_name_{i}', StringField(f'Home Name {i}', validators=[DataRequired()]))
            setattr(PreTourForm, f'g_name_{i}', StringField(f'Guest Name {i}', validators=[DataRequired()]))
            setattr(PreTourForm, f'match_time_{i}', StringField(f'Match {i} Start Time'))

    submit = SubmitField("Отправить")

    def get_count(self):
        self._count += 1
        return self._count