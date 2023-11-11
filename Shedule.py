from Server import send_message, path
from RWfile import Subscribers, SubscribersFile, Readfile_tour
import os

site_url = 'http://scared.pythonanywhere.com/'

subscribers_file1 = SubscribersFile("_subscribers.txt")
subscribers_login_list = subscribers_file1.get_subscribers_login()                  #список пользователей со включенной подпиской
tour_inf = Readfile_tour()
round_num = tour_inf.num
tour_date = tour_inf.date
for subscriber_login in subscribers_login_list:
    filename = round_num.replace('тур', '') + '_' + subscriber_login + '.txt'
    if not os.path.isfile(os.path.join(path, filename)):
        subscriber_id = subscribers_file1.get_id_by_login(subscriber_login)
        print(f'Напоминание пользователю {subscriber_id} отправить прогнозы на {round_num} не позднее {tour_date} ')
        send_message(subscriber_id, f'Не забудьте отправить прогнозы на {round_num} не позднее {tour_date}. Адрес сайта {site_url}')

