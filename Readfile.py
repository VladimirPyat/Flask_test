class Readfile_tour:

  def __init__(self):
    with open('_tour.txt', 'r', encoding='utf-8') as file:          #считывание из файла информации о текущем туре
      data = ' '.join(file.readlines()).split()
      self.num = data[0]                                            #номер тура
      self.date = (f'{data[1]} {data[2]}')                          #дата и время окончания приема прогнозов
      self.matches = data[3:len(data)]                              #пары команд

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
          self.login = email[:email.find("@")]                            #логин

user_inf = Readfile_users('scared@mail.ru')
username = user_inf.name