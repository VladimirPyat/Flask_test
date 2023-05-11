from flask import Flask, render_template, redirect, url_for
from FillForm import FillF
from AuthForm import AuthF


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dont know what this thing for'


@app.route('/')
def main():
    return (redirect(url_for('log')))


@app.route('/fill', methods=['GET', 'POST'])
def fill():
    form = FillF()
    #filename = 'scared'
    #username = "Пятницкий"
    
    with open('_tour.txt', 'r', encoding='utf-8') as file:
        round_num = ' '.join(file.readline()) 
    if form.validate_on_submit():
        with open(filename+'.txt', 'w', encoding='utf-8') as file:
            file.write(f'{form.h_fields0.data}:{form.g_fields0.data}\n')
        return render_template('login.html', form=AuthF(), message='Неверный пароль') 
    return render_template('fill.html', form=FillF(), filename = filename, username = username, round_num = round_num) 


@app.route('/log', methods=['GET', 'POST'])
def log():
    form = AuthF()
    if form.validate_on_submit():
        with open('_users.txt', 'r', encoding='utf-8') as file:
            data = ' '.join(file.readlines())
        
        if form.email.data not in data:
            return render_template('login.html', form=form, message='Вы не зарегистрированы')
        else:
            for i in data.split():
                if form.email.data in i:
                    if i.split(';')[-1] == form.password.data:
                        filename = form.email.data[:form.email.data.find("@")]+'.txt'
                        username = i.split(';')[0]

                        with open('_tour.txt', 'r', encoding='utf-8') as file:
                            round_num = ' '.join(file.readline())  
                                                
                        return (redirect(url_for('fill'))) 
                    
                    else:
                       return render_template('login.html', form=form, message='Неверный пароль') 
            
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run()
