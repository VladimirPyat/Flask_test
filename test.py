from flask import Flask
from Server import on_subscriber, off_subscriber, process_message, callback, is_login
from RWfile import Subscribers, SubscribersFile

#on_subscriber('87313')
#off_subscriber('87313')
on_subscriber('208935045')

# subscribers_file1 = SubscribersFile("_subscribers.txt")
# subscribers_file1.add_user('12345', 'login1')
# subscribers_file1.add_user('2222', 'login2')
# subscribers_file1.add_user('3333', 'login3')
#
# subscriber1 = Subscribers('12345')
# subscriber2 = Subscribers('2222')
# subscriber3 = Subscribers('3333')
# subscriber3.off_subscriber()
# subscriber2.off_subscriber()
# subscriber2.on_subscriber()
# print(subscriber3.status+' - '+subscriber3.id)
# print(subscriber2.status+' - '+subscriber2.id)





