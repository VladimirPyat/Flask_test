from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, validators
from wtforms.validators import DataRequired, InputRequired
from RWfile import Readfile_tour

class FillF(FlaskForm):


    def __init__(self, *args, **kwargs):
        super(FillF, self).__init__(*args, **kwargs)
        self.max_score = 10
        self.tour_inf = Readfile_tour()
        self.round_date = self.tour_inf.date 
        self.round_num = self.tour_inf.num
        self.data_split = self.tour_inf.matches
        self.data_split.pop()
        self.h_names = [i.split('-')[0] for i in self.data_split]
        self.g_names = [i.split('-')[1] for i in self.data_split]

        for h_name in self.h_names:
            setattr(self, h_name, IntegerField(h_name, validators=[InputRequired(), validators.NumberRange(min=0, max=self.max_score)]))
        for g_name in self.g_names:
            setattr(self, g_name, IntegerField(g_name, validators=[InputRequired(), validators.NumberRange(min=0, max=self.max_score)]))
    
        self.submit = SubmitField("Отправить")
    