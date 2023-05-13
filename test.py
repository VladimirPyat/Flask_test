from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, validators
from wtforms.validators import DataRequired
from Readfile import Readfile_tour

import datetime 

def Date_compare (date_str):                               # True если текущее время не позднее того что задано на входе строкой
  
  format = '%Y.%m.%d %H:%M'
  deadline_time = datetime.datetime.strptime(date_str, format)
  current_time = datetime.datetime.today()

  return (current_time <= deadline_time)

  
tour_inf = Readfile_tour()
print (tour_inf.date)
print(Date_compare (tour_inf.date))