from flask import Flask, render_template, redirect, url_for, request
from FillForm import FillF
from AuthForm import AuthF
from RWfile import readfile, writefile, Readfile_tour, Readfile_users, Readfile_userscore

import datetime, os

path = os.path.dirname(os.path.abspath(__file__))

def date_compare (date_str):                               # True если текущее время не позднее того что задано на входе строкой по формату
  
  format = '%Y.%m.%d %H:%M'
  deadline_time = datetime.datetime.strptime(date_str, format)
  current_time = datetime.datetime.today()

  return (current_time <= deadline_time)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dont know what this thing for'


@app.route('/')
def main():
    return (redirect(url_for('log')))


@app.route('/base')                                                 #основное меню
def base():
    login = request.args.get('login') 
    message = request.args.get('message') 
    tour_inf = Readfile_tour()
    round_num = tour_inf.num
    round_date = tour_inf.date 
    if date_compare (round_date):
        return render_template('base.html', login = login, message = message)
    else:
        return (redirect(url_for('table', message = 'Прием прогнозов завершен')))    
    

@app.route('/read')                                                 #основное меню
def read():
    login = request.args.get('login') 
    
    tour_inf = Readfile_tour()
    match_data = tour_inf.matches 
    round_num = tour_inf.num                                                #номер тура
    user_inf = Readfile_users(login)
    username = user_inf.name                                                #имя пользователя
    filename = round_num.replace('тур', '')+'_'+login+'.txt'             #имя файла для записи прогноза пользователя

    if os.path.isfile(os.path.join(path, filename)):  
        forecast = Readfile_userscore(filename)
        userscore_data = forecast.score                                  #считываем прогнозы конкретного пользователя
        data = list(zip(match_data, userscore_data))
        return render_template('read.html', username = username, login = login, round_num = round_num, data = data)
    else:
        return (redirect(url_for('base', login = login, message = 'Данные не заполнены'))) 
        
    

@app.route('/fill', methods=['GET', 'POST'])                        #процедура заполнение формы
def fill():
    form = FillF()
    login = request.args.get('login')                         #прием переменных из url  
    tour_inf = Readfile_tour()
    round_num = tour_inf.num                                                #номер тура
    round_date = tour_inf.date 
    user_inf = Readfile_users(login)
    username = user_inf.name                                                #имя пользователя
    filename = round_num.replace('тур', '')+'_'+login+'.txt'    #имя файла для записи прогноза пользователя

    if date_compare (round_date):
        if form.validate_on_submit():                                            #запись в файл информации из формы 
            file_strings = [f'{round_num}\n', f'{username}\n',
                            f'{form.h_fields0.data}-{form.g_fields0.data}\n',
                            f'{form.h_fields1.data}-{form.g_fields1.data}\n',
                            f'{form.h_fields2.data}-{form.g_fields2.data}\n',
                            f'{form.h_fields3.data}-{form.g_fields3.data}\n',
                            f'{form.h_fields4.data}-{form.g_fields4.data}\n',
                            f'{form.h_fields5.data}-{form.g_fields5.data}\n',
                            f'{form.h_fields6.data}-{form.g_fields6.data}\n',
                            f'{form.h_fields7.data}-{form.g_fields7.data}\n']
            writefile(os.path.join(path, filename), "".join(file_strings))

            return (redirect(url_for('base', login = login, message = 'Данные отправлены')))
        return render_template('fill.html', form=FillF(), round_date=round_date, username = username, round_num = round_num)  #cоздание формы
    else:
        return (redirect(url_for('table', message = 'Прием прогнозов завершен'))) 


@app.route('/table')                                                 #основное меню
def table ():
  message = request.args.get('message')
  tour_inf = Readfile_tour()
  round_num = tour_inf.num
  match_data = tour_inf.matches
  data = readfile('_users.txt')  # считывание из файла информации о пользователях
  match_data.pop()

  login_list = [user.split(';')[1] for user in data]  # список login для перебора пользователей
  user_list = [user.split(';')[0] for user in data]  # список имен для сводной
  score_list = []  # список прогнозов для сводной

  for login, username in zip(login_list, user_list):
      filename = round_num.replace('тур', '') + '_' + login + '.txt'

      if os.path.isfile(os.path.join(path, filename)):
          userscore_data = Readfile_userscore(filename)  # если файл создан - значит прогноз сделан, считываем
          userscore_data.score.insert(0, username)  # добавляем имя пользователя в первый столбец
          score_list.append(userscore_data.score)
      else:
          match_score = [' - ' for i in match_data]  # файла нет - заполняем пробелами, нет прогноза
          match_score.insert(0, username)  # добавляем имя пользователя в первый столбец
          score_list.append(match_score)

  filename = round_num.replace('тур', '') + '_' + 'forecast' + '.txt'
  if not os.path.isfile(os.path.join(path, filename)):                      #создаем файл для переноса в эксель если не создан
      teams_list = [i for i in match_data]                                  #список команд для сводного файла
      teams_list.insert(0, ' ')

      file_strings = []                                                     # список для записи в файл
      user_list.insert(0, ' ')
      file_strings.append(';'.join(user_list))                              #добавляем шапку таблицы с именами
      file_strings.append('\n')
      for i in range(1, len(teams_list)):
          onestring = []                                                    #строка для записи результатов домашних команд
          twostring = []                                                    #строка для записи результатов гостевых команд
          onestring.append(teams_list[i].split('-')[0])                     #разделение гостевой и домашней команды
          twostring.append(teams_list[i].split('-')[1])
          for users_scores in score_list:
              onestring.append(users_scores[i].split('-')[0])               #разделение результатов гостевой и домашней команды
              twostring.append(users_scores[i].split('-')[1])
          file_strings.append(';'.join(onestring) + '\n')
          file_strings.append(';'.join(twostring) + '\n')

      writefile(os.path.join(path, filename), "".join(file_strings))

  return render_template('table.html', round_num = round_num, score_list = score_list, match_data = match_data)


@app.route('/log', methods=['GET', 'POST'])                                                      #процедура логин
def log():
    form = AuthF()
    if form.validate_on_submit():
        data = readfile ('_users.txt', False)

        if form.login.data not in data:                                                                 #проверка логин
            return render_template('login.html', form=form, message='Вы не зарегистрированы')
        else:
            for i in data.split():
                if form.login.data in i:
                    if i.split(';')[-1] == form.password.data:                                          #проверка пароля
                        return (redirect(url_for('base', login = form.login.data, message = '')))         #вызов процедуры заполнения формы 
                    
                    else:
                       return render_template('login.html', form=form, message='Неверный пароль') 
            
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
