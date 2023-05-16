from flask import Flask, render_template, redirect, url_for, request
from FillForm import FillF
from AuthForm import AuthF
from Readfile import Readfile_tour, Readfile_users, Readfile_userscore

import datetime 


def Date_compare (date_str):                               # True если текущее время не позднее того что задано на входе строкой по формату
  
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
    email = request.args.get('email') 
    message = request.args.get('message') 
    return render_template('base.html', email = email, message = message)

@app.route('/read')                                                 #основное меню
def read():
    email = request.args.get('email') 
    #message = request.args.get('message') 
    tour_inf = Readfile_tour()
    match_data = tour_inf.data 
    round_num = tour_inf.num                                                #номер тура
    user_inf = Readfile_users(email)
    username = user_inf.name                                                #имя пользователя
    filename = round_num.replace('тур', '')+'_'+user_inf.login+'.txt'    #имя файла для записи прогноза пользователя
    shift = 2                                                       #номер строки начала основных данных
    forecast = Readfile_userscore(filename)
    userscore_data = forecast.data                                  #считываем прогнозы конкретного пользователя

    data = []
    for i in range (len(match_data)-shift):
        data.append((match_data[i+shift], userscore_data[i+shift]))

    return render_template('read.html', username = username, email = email, round_num = round_num, data = data)
    

@app.route('/fill', methods=['GET', 'POST'])                        #процедура заполнение формы
def fill():
    form = FillF()
    email = request.args.get('email')                         #прием переменных из url  
    tour_inf = Readfile_tour()
    round_num = tour_inf.num                                                #номер тура
    round_date = tour_inf.date 
    user_inf = Readfile_users(email)
    username = user_inf.name                                                #имя пользователя
    filename = round_num.replace('тур', '')+'_'+user_inf.login+'.txt'    #имя файла для записи прогноза пользователя

    if Date_compare (round_date):
        if form.validate_on_submit():                                            #запись в файл информации из формы 
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(f'{round_num}\n')
                file.write(f'{username}\n')
                file.write(f'{form.h_fields0.data}:{form.g_fields0.data}\n')
            return (redirect(url_for('base', email = email, message = 'Данные отправлены')))
        return render_template('fill.html', form=FillF(), username = username, round_num = round_num)  #эта строка должна создавать форму
    else:
        return (redirect(url_for('base', email = email, message = 'Прием прогнозов завершен')))


@app.route('/log', methods=['GET', 'POST'])                                                      #процедура логин
def log():
    form = AuthF()
    if form.validate_on_submit():
        with open('_users.txt', 'r', encoding='utf-8') as file:
            data = ' '.join(file.readlines())
        
        if form.email.data not in data:                                                                 #проверка логин
            return render_template('login.html', form=form, message='Вы не зарегистрированы')
        else:
            for i in data.split():
                if form.email.data in i:
                    if i.split(';')[-1] == form.password.data:                                          #проверка пароля
                        return (redirect(url_for('base', email = form.email.data, message = '')))         #вызов процедуры заполнения формы 
                    
                    else:
                       return render_template('login.html', form=form, message='Неверный пароль') 
            
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run()
