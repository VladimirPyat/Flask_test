class Readfile_tour:
  def __init__(self):
    with open('_tour.txt', 'r', encoding='utf-8') as file:          #считывание из файла информации о текущем туре
      data = ' '.join(file.readlines()).split()
      self.num = data[0]                                            #номер тура
      self.date = (f'{data[1]} {data[2]}')                          #дата и время окончания приема прогнозов
      self.matches = data[3:len(data)]                              #пары команд