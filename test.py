from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, validators
from wtforms.validators import DataRequired
from Readfile import Readfile_tour


max_score = 10
h_name = []
g_name = []
    
tour_inf = Readfile_tour()
round_num = tour_inf.num
data_split = tour_inf.matches
round_date = tour_inf.date 


print (round_date)
