from flask import Flask, render_template, redirect, url_for
from FillForm import FillF
from AuthForm import AuthF


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dont know what this thing for'


@app.route('/')
def main():
    return (redirect(url_for('log')))


@app.route('/fill', methods=['GET', 'POST'])                        #процедура заполнение формы
def fill():
    form = FillF()
    filename = 'scared'                                             #задание переменных вручную для проверки, поскольку передача через вызов процедур не работает
    username = "Пятницкий"
    
    with open('_tour.txt', 'r', encoding='utf-8') as file:          #считывание из файла информации необходимой для заполнения
        round_num = ' '.join(file.readline()) 
    if form.validate_on_submit():                                   #запись в файл информации из формы 
        with open(filename+'.txt', 'w', encoding='utf-8') as file:
            file.write(f'{form.h_fields0.data}:{form.g_fields0.data}\n')
        return ('Данные отправлены') 
    return render_template('fill.html', form=FillF(), filename = filename, username = username, round_num = round_num)  #по идее эта строка должна создавать форму


@app.route('/log', methods=['GET', 'POST'])                         #процедура логин
def log():
    form = AuthF()
    if form.validate_on_submit():
        with open('_users.txt', 'r', encoding='utf-8') as file:
            data = ' '.join(file.readlines())
        
        if form.email.data not in data:                               #проверка логин
            return render_template('login.html', form=form, message='Вы не зарегистрированы')
        else:
            for i in data.split():
                if form.email.data in i:
                    if i.split(';')[-1] == form.password.data:                                  #проверка пароля
                        filename = form.email.data[:form.email.data.find("@")]+'.txt'          #подготовка информации для передачи в форму
                        username = i.split(';')[0]

                        with open('_tour.txt', 'r', encoding='utf-8') as file:      #считывание из файла информации необходимой для заполнения
                            round_num = ' '.join(file.readline())  
                                                
                        return (redirect(url_for('fill')))                     #вызов процедуры заполнения формы работает только так
                    
                    else:
                       return render_template('login.html', form=form, message='Неверный пароль') 
            
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run()
