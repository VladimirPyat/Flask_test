from flask import Flask, render_template, redirect, url_for, request, json, session
from FillForm import FillF
from AuthForm import AuthF
from RWfile import readfile, writefile, Readfile_tour, Readfile_users, Readfile_userscore, Subscribers, SubscribersFile

import datetime, pytz, os, vk_api

path = os.path.dirname(os.path.abspath(__file__))

get_login = False                                                   #глобальная переменная. флаг необходимости запроса логина


def date_local_format ():
    timezone = pytz.timezone('Europe/Moscow')
    format = '%Y.%m.%d %H:%M'
    return  datetime.datetime.now(timezone).strftime(format)


def date_compare (date_str):                               # True если текущее время не позднее того что задано на входе строкой по формату

    format = '%Y.%m.%d %H:%M'
    deadline_time = datetime.datetime.strptime(date_str, format)
    timezone = pytz.timezone('Europe/Moscow')
    deadline_time = timezone.localize(deadline_time)
    current_time = datetime.datetime.now(timezone)
    return current_time <= deadline_time


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

    if os.path.isfile(os.path.join(path, filename)):                    #если файл с прогнозом существует
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
    round_num = tour_inf.num
    round_date = tour_inf.date
    matches = tour_inf.matches
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
            writefile(filename, "".join(file_strings))

            vk_send_note(login, tour_inf, user_inf, file_strings)

            return (redirect(url_for('base', login = login, message = 'Данные отправлены')))
        return render_template('fill.html', form=FillF(), round_date=round_date, username = username, round_num = round_num)  #cоздание формы
    else:
        return (redirect(url_for('table', message = 'Прием прогнозов завершен')))


def vk_send_note(login, tour_inf, user_inf, file_strings):
    subscribers_file1 = SubscribersFile("_subscribers.txt")
    user_id = subscribers_file1.get_id_by_login(login)
    subscriber1 = Subscribers(user_id)                          #создаем экземпляр подписчика по id
    if subscriber1.is_subscriber_on():
        round_num = tour_inf.num
        matches = tour_inf.matches
        username = user_inf.name
        message = f'{round_num}, {username}\n'
        shift = len(file_strings) - len(matches)
        for match, score in zip(matches, file_strings[shift:]):
            message += f'{match} {score}'                    #объединяем в сообщение имя, номер тура, матчи и прогноз пользователя
        send_message(user_id, message)

    else:
        print ('Подписка неактивна')


@app.route('/table')                                                 #таблица результатов
def table ():
  message = request.args.get('message')
  tour_inf = Readfile_tour()
  round_num = tour_inf.num
  round_date = tour_inf.date

  if not date_compare(round_date):
      match_data = tour_inf.matches
      data = readfile('_users.txt')  # считывание из файла информации о пользователях
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

          writefile(filename, "".join(file_strings))

      return render_template('table.html', round_num = round_num, score_list = score_list, match_data = match_data, message=date_local_format())
  else:
      return (redirect(url_for('log')))


@app.route('/log', methods=['GET', 'POST'])                                                      #процедура логин
def log():
    form = AuthF()
    if form.validate_on_submit():
        data = readfile ('_users.txt', False)

        if not is_login(form.login.data.strip()):                                                        #проверка логин, убираем лишние пробелы
            return render_template('login.html', form=form, message='Вы не зарегистрированы')
        else:
            for i in data.split():
                if form.login.data.strip() == i.split(';')[1]:                                           #!!!исправлено!!!
                    if i.split(';')[-1] == form.password.data:                                          #проверка пароля
                        return (redirect(url_for('base', login = form.login.data, message = '')))         #вызов процедуры заполнения формы

                    else:
                       return render_template('login.html', form=form, message='Неверный пароль')

    return render_template('login.html', form=form)


@app.route('/', methods=['POST'])                                       # приложение для VK API
def callback():
    data = request.get_json()                                           # Обрабатываем полученный callback
    return process_callback(data)


def process_callback(data):
    if data['type'] == 'confirmation':                                  # Проверяем тип события
        confirmation_token = '71755a8d'                                 # !!!Токен привязать к конкретному сайту!!!
        return confirmation_token
    elif data['type'] == 'message_new':
        if data['object']['message']['text'] != '':
            message_text = data['object']['message']['text'].strip(', . / : ; - _ + = ( )').lower()
            user_id = data['object']['message']['from_id']
            process_message(message_text, user_id)
        return 'ok'
    else:
        return 'ok'


def process_message (message_text, user_id):                            # отбработка сообщения
    global get_login
    filename = '_subscribers.txt'
    if not os.path.isfile(os.path.join(path, filename)):
        writefile(filename, '')
    subscribers_file1 = SubscribersFile(filename)
    subscribers_list = subscribers_file1.data
    if not get_login:                                                # если в предыдущей сессии не запрошен логин
        if str(user_id) in '\n'.join(subscribers_list):                      # если пользователь зарегистрирован в списке рассылки
            command_run(message_text, str(user_id))                          # расшифровка команд в тексте сообщения
        else:
            print(f'Запрашиваем логин {user_id}')
            send_message(user_id, 'Введите ваш логин для входа в веб форму сбора прогнозов')
            get_login = True
    elif is_login(message_text):                                        # поиск логина в списке пользователей
        print(f'Добавляем пользователя {user_id};{message_text};ON')
        subscribers_file1.add_user(user_id, message_text)               #если был запрошен ввод логина - добавляем пользователя в список
        get_login = False
        send_message(user_id, 'Подписка создана. Для включения/отключения уведомлений используйте команды start/stop')
    else:
        send_message(user_id, 'Пользователь с таким логином не найден')


def is_login(check_login):                                                    # проверка на наличие введенного логина в списке пользователей
    print(f'Проверка логина {check_login}')
    data = readfile('_users.txt')
    login_list = [user.split(';')[1] for user in data]  # список login для перебора пользователей
    result = any(login == check_login for login in login_list)
    return result


def command_run(message_text, user_id):                       #поиск команды в тексте
    print(message_text)
    if message_text == 'start':
        on_subscriber(user_id)
    elif message_text == 'stop':
        off_subscriber(user_id)


def on_subscriber(user_id):
    subscriber1 = Subscribers(user_id)
    if not subscriber1.is_subscriber_on():
        subscriber1.on_subscriber()
        message = "Вы подключили напоминания"
    else:
        message = "Напоминания уже подключены"
    print(f"Метод on_subscriber вызван для пользователя {user_id}")
    send_message(user_id, message)


def off_subscriber(user_id):
    subscriber1 = Subscribers(user_id)
    if subscriber1.is_subscriber_on():
        subscriber1.off_subscriber()
        message = "Вы отключили напоминания"
    else:
        message = "Напоминания уже отключены"
    print(f"Метод off_subscriber вызван для пользователя {user_id}")
    send_message(user_id, message)



def send_message(user_id, message):
    access_token = "vk1.a.WgywILuuetPdoMlWV5zJWCOBzzDhiPcSMznvnZvZbq6G_VZTjgcnZBK7bGEVPHGkAfsPlBRkJuwMzG_TrDom3AMV06BrDdy-IrFjDLzz3lwA1MYNTtJHCYpCcjyIb73rAozsapWJhw-Atdeg0CaxysZhKZSMgtV8_HNIQ9nlC7vUmXMfq4QTgVEQiTghrNuqnHipsBReqdcX-Q4QH6OOaQ"
    vk_session = vk_api.VkApi(token=access_token)
    vk = vk_session.get_api()
    vk.messages.send(user_id=user_id, message=message, random_id=vk_api.utils.get_random_id())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)                                # Запуск Flask приложения для сайта
