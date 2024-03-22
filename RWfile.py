import os

path = os.path.dirname(os.path.abspath(__file__))


def writefile(filename, data):
    with open(os.path.join(path, filename), 'w', encoding='utf-8') as file:  # !!!ИСПРАВЛЕНО!!! по аналогии с read
        file.write(data)


def readfile(filename, flag=True):                                            # flag = True - с разбивкой по строкам (иначе join)
    with open(os.path.join(path, filename), 'r', encoding='utf-8') as file:  # считывание из файла
        if flag:
            data = [line.strip() for line in file.readlines() if line.strip()]  # убираем пустые строки

        else:
            data = ' '.join(file.readlines())
    return data


class Readfile_tour:

    def __init__(self):
        shift = 2  # номер строки начала основных данных
        data = readfile('_tour.txt')  # считывание из файла информации о текущем туре

        self.data = data
        self.num = data[0]  # номер тура
        self.date = data[1]  # дата и время окончания приема прогнозов
        self.matches = data[shift:len(data)]  # пары команд


class Readfile_users:

    def __init__(self, login):
        data = readfile('_users.txt')  # считывание из файла информации о пользователях

        # self.data = data
        for user in data:
            if login in user:
                user_split = user.split(';')
                if user_split[1] == login:  # проверка пароля
                    self.name = user_split[0]  # имя пользователя
                    self.passw = user_split[2]  # пароль
        else:
            self.name = None
            self.passw = None



class Readfile_userscore:                       # считывание файла конкретного пользователя

    def __init__(self, filename):
        shift = 2
        data = readfile(filename)

        self.data = data
        self.score = data[shift:]


class SubscribersFile:
    def __init__(self, filename):
        self.filename = filename
        self.data = readfile(filename)


    def add_user (self, user_id, login):
        self.data.append(f'{user_id};{login};ON')
        writefile(self.filename, '\n'.join(self.data))

    def put_to_file(self, subscriber):
        for i in range (len(self.data)):
            split_data = self.data[i].split(';')
            if split_data[0] == subscriber.id:
                self.data[i] = f'{subscriber.id};{subscriber.login};{subscriber.status}'
                break
        writefile(self.filename, '\n'.join(self.data))

    def get_from_file(self, user_id):
        for i in range (len(self.data)):
            split_data = self.data[i].split(';')
            if split_data[0] == user_id:
                return split_data[1], split_data[2]

    def get_id_by_login(self, login):
        for i in range (len(self.data)):
            split_data = self.data[i].split(';')
            if split_data[1] == login:
                return split_data[0]

    def get_subscribers_login(self):                                #список пользователей с активной подпиской
        logins_list = []
        for i in range(len(self.data)):
            split_data = self.data[i].split(';')
            if split_data[2] == 'ON':
                logins_list.append(split_data[1])
        return logins_list


class Subscribers:
    def __init__(self, user_id):
        self.id = user_id
        self.subscribers_file = SubscribersFile("_subscribers.txt")
        self.login, self.status = self.get_subscriber_info(user_id)

    def get_subscriber_info(self, user_id):
        return self.subscribers_file.get_from_file(user_id)

    def on_subscriber(self):
        self.status = 'ON'
        self.subscribers_file.put_to_file(self)

    def off_subscriber(self):
        self.status = 'OFF'
        self.subscribers_file.put_to_file(self)

    def is_subscriber_on(self):
        return self.status == 'ON'