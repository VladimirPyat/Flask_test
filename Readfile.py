class Readfile_tour:

  def __init__(self):
    shift = 2                                                       #номер строки начала основных данных
    with open('_tour.txt', 'r', encoding='utf-8') as file:          #считывание из файла информации о текущем туре
      data = ''.join(file.readlines()).split('\n')
    data.pop()
    self.data = data
    self.num = data[0]                                            #номер тура
    self.date = data[1]                           #дата и время окончания приема прогнозов
    self.matches = data[shift:len(data)]                              #пары команд

class Readfile_users:

  def __init__(self, email):
    with open('_users.txt', 'r', encoding='utf-8') as file:          #считывание из файла информации о пользователях
      data = ''.join(file.readlines()).split('\n')
    data.pop()
    #self.data = data
    for user in data:
      if email in user:
        user_split = user.split(';')
        if user_split[1] == email:                                  #проверка пароля
          self.name = user_split[0]                                            #имя пользователя
          self.passw = user_split[2]                                           #пароль
          self.login = email[:email.find("@")]                            #логин

class Readfile_userscore:

  def __init__(self, filename):
    shift = 2 
    with open(filename, 'r', encoding='utf-8') as file:
      data = ''.join(file.readlines()).split('\n')
    data.pop()
    self.data = data
    self.score = data[shift:]
    

