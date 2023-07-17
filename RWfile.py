import os

path = os.path.dirname(os.path.abspath(__file__))


def writefile (filename, data):
  with open(os.path.join(filename), 'w', encoding='utf-8') as file:
    file.write(data)

def readfile (filename, flag=True):                                 #flag - тип возвращаемых данных с разбивкой или без
  with open(os.path.join(path, filename), 'r', encoding='utf-8') as file:  # считывание из файла
    if flag:
      data = ''.join(file.readlines()).split('\n')
      data.pop()
    else:
      data = ' '.join(file.readlines())
  return data


class Readfile_tour:


  def __init__(self):
    shift = 2                                                                   #номер строки начала основных данных
    data = readfile ('_tour.txt')                          #считывание из файла информации о текущем туре

    self.data = data
    self.num = data[0]                                            #номер тура
    self.date = data[1]                                           #дата и время окончания приема прогнозов
    self.matches = data[shift:len(data)]                              #пары команд

class Readfile_users:

  def __init__(self, email):
    data = readfile ('_users.txt')                             #считывание из файла информации о пользователях

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
    data = readfile (filename)

    self.data = data
    self.score = data[shift:]
    

