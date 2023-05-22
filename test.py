from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, validators
from wtforms.validators import DataRequired
from Readfile import Readfile_tour, Readfile_users, Readfile_userscore

import datetime, os


def alltable ():
  tour_inf = Readfile_tour()
  round_num = tour_inf.num
  
  with open('_users.txt', 'r', encoding='utf-8') as file:          #считывание из файла информации о пользователях
    data = ''.join(file.readlines()).split('\n')
  data.pop()
  mail_list = [user.split(';')[1] for user in data]               #список email для перебора пользователей
  user_list = [user.split(';')[0] for user in data]               #список имен для сводной
  score_list = []                                                 #список прогнозов для сводной

  for email, username in zip (mail_list, user_list):
    filename = round_num.replace('тур', '')+'_'+email[:email.find('@')]+'.txt'
    
    if os.path.isfile(filename):                                  
      userscore_data = Readfile_userscore(filename)               #если файл создан - значит прогноз сделан, считываем
      userscore_data.score.insert(0, username)
      score_list.append(userscore_data.score)
    else:
      match_score = ['.' for i in tour_inf.matches]               # файла нет - заполняем точками, нет прогноза
      match_score.insert(0, username)
      score_list.append(match_score)
  return (score_list)

print (alltable ())
