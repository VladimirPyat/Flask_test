from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, validators
from wtforms.validators import DataRequired



class Readfile_users:

  def __init__(self, email):
    with open('_users.txt', 'r', encoding='utf-8') as file:          #считывание из файла информации о пользователях
      data = ' '.join(file.readlines()).split()
    for user in data:
      if email in user:
        user_split = user.split(';')
        if user_split[1] == email:                                  #проверка пароля
          self.name = user_split[0]                                            #имя пользователя
          self.passw = user_split[2]                                           #пароль
          self.login = email[:email.find("@")]  

a = Readfile_users ('scared@mail.ru')
print (a.login)