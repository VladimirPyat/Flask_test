from flask import Flask, render_template, redirect, url_for, request
from FillForm import FillF
from AuthForm import AuthF
from Readfile import Readfile_tour

import datetime 


def Date_compare (date_str):                               # True если текущее время не позднее того что задано на входе строкой
  
  format = '%Y.%m.%d %H:%M'
  deadline_time = datetime.datetime.strptime(date_str, format)
  current_time = datetime.datetime.today()

  return (current_time <= deadline_time)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dont know what this thing for'


@app.route('/')
def main():
    return (redirect(url_for('log')))


@app.route('/fill', methods=['GET', 'POST'])                        #процедура заполнение формы
def fill():
    form = FillF()
    filename = request.args.get('filename')                         #прием переменных из url
    username = request.args.get('username')
    tour_inf = Readfile_tour()
    round_num = tour_inf.num
   

    if form.validate_on_submit():                                   #запись в файл информации из формы 
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f'{round_num}\n')
            file.write(f'{username}\n')
            file.write(f'{form.h_fields0.data}:{form.g_fields0.data}\n')
        return ('Данные отправлены') 
    return render_template('fill.html', form=FillF(), filename = filename, username = username, round_num = round_num)  #эта строка должна создавать форму


@app.route('/log', methods=['GET', 'POST'])                                                      #процедура логин
def log():
    form = AuthF()
    if form.validate_on_submit():
        with open('_users.txt', 'r', encoding='utf-8') as file:
            data = ' '.join(file.readlines())
        
        if form.email.data not in data:                                                           #проверка логин
            return render_template('login.html', form=form, message='Вы не зарегистрированы')
        else:
            for i in data.split():
                if form.email.data in i:
                    if i.split(';')[-1] == form.password.data:                                  #проверка пароля
                        filename = form.email.data[:form.email.data.find("@")]+'.txt'          #подготовка информации для передачи в форму
                        username = i.split(';')[0]

                        return (redirect(url_for('fill', filename = filename, username = username)))                     #вызов процедуры заполнения формы 
                    
                    else:
                       return render_template('login.html', form=form, message='Неверный пароль') 
            
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run()
