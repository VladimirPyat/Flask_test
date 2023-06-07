from flask import Flask, render_template, redirect, url_for, request
from FillForm import FillF
from AuthForm import AuthF
from Readfile import readfile, writefile, Readfile_tour, Readfile_users, Readfile_userscore

import datetime, os
path = os.path.dirname(os.path.abspath(__file__))

tour_inf = Readfile_tour()
round_num = tour_inf.num
match_data = tour_inf.matches
data = readfile('_users.txt')  # считывание из файла информации о пользователях
match_data.pop()

mail_list = [user.split(';')[1] for user in data]  # список email для перебора пользователей
user_list = [user.split(';')[0] for user in data]  # список имен для сводной
score_list = []  # список прогнозов для сводной

for email, username in zip(mail_list, user_list):
    filename = round_num.replace('тур', '') + '_' + email[:email.find('@')] + '.txt'

    if os.path.isfile(os.path.join(path, filename)):
        userscore_data = Readfile_userscore(filename)  # если файл создан - значит прогноз сделан, считываем
        userscore_data.score.insert(0, username)  # добавляем имя пользователя в первый столбец
        score_list.append(userscore_data.score)
    else:
        match_score = [' - ' for i in match_data]  # файла нет - заполняем пробелами, нет прогноза
        match_score.insert(0, username)  # добавляем имя пользователя в первый столбец
        score_list.append(match_score)
#print (score_list)

filename = round_num.replace('тур', '') + '_' + 'forecast' + '.txt'
if not os.path.isfile(os.path.join(path, filename)):
    teams_list = [i for i in match_data]
    teams_list.insert(0, ' ')
    #print (teams_list)
    file_strings = []
    user_list.insert(0, ' ')
    file_strings.append(';'.join(user_list))
    file_strings.append('\n')
    for i in range (1, len(teams_list)):
        onestring = []
        twostring = []
        onestring.append(teams_list[i].split('-')[0])
        twostring.append(teams_list[i].split('-')[1])
        for users_scores in score_list:
            onestring.append(users_scores[i].split('-')[0])
            twostring.append(users_scores[i].split('-')[1])
        file_strings.append(';'.join(onestring)+'\n')
        file_strings.append(';'.join(twostring)+'\n')

    writefile (filename, "".join(file_strings))






