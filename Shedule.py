from Server import send_message, path
from RWfile import Subscribers, SubscribersFile, Readfile_tour
import os, datetime

def check_shedule_date(input_time):
    delta_target = 1                                                #количество дней, за которое нужно сделать напоминание
    current_date = datetime.date.today()
    input_date = datetime.datetime.strptime(input_time.split()[0], "%Y.%m.%d").date()
    delta = input_date - current_date
    # Проверка, если разница в днях между текущей датой и входной датой больше заданной либо отрицательна - оповещение не выполняется
    print(delta.days)
    if (delta.days > delta_target) or (delta.days < 0):
        return False
    else:
        return True

def send_to_all(message):
    subscribers_file = SubscribersFile("_subscribers.txt")
    subscribers_login_list = subscribers_file.get_subscribers_login()  # список пользователей со включенной подпиской
    print('Запущена общая рассылка:')
    print(message)
    for subscriber_login in subscribers_login_list:
        subscriber_id = subscribers_file.get_id_by_login(subscriber_login)
        send_message(subscriber_id,message)


if __name__ == '__main__':

    site_url = 'http://scared.pythonanywhere.com/'
    subscribers_file1 = SubscribersFile("_subscribers.txt")
    subscribers_login_list = subscribers_file1.get_subscribers_login()                  #список пользователей со включенной подпиской
    tour_inf = Readfile_tour()
    round_num = tour_inf.num
    tour_date = tour_inf.date
    if check_shedule_date(tour_date):                                                              #проверка подошло ли время оповещения
        print('Запущен сервис напоминаний')
        for subscriber_login in subscribers_login_list:
            filename = round_num.replace('тур', '') + '_' + subscriber_login + '.txt'
            if not os.path.isfile(os.path.join(path, filename)):
                subscriber_id = subscribers_file1.get_id_by_login(subscriber_login)
                print(f'Напоминание пользователю {subscriber_id} отправить прогнозы на {round_num} не позднее {tour_date} ')
                send_message(subscriber_id, f'Не забудьте отправить прогнозы на {round_num} не позднее {tour_date}. Адрес сайта {site_url}')
    else:
        print('Время для напоминаний еще не пришло')
