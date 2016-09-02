#!/usr/bin/env python
# coding=utf-8
# icloud 登录 钓鱼网站

import string, random
import requests
import time
import socket, struct
import thread

URL = 'http://gwktst.gq/ICloud13/save.asp' # 103.228.131.157
# URL = 'http://guofen-dingwei-ese.cn/ICloud13/save.asp' # 118.193.177.123
# URL = 'http://www.applecva.com/ICloud13/save.asp' # 103.206.22.173

def send_junk_data():

	while True:

		try:
			username = ''.join(random.choice(string.digits) for _ in range(int(time.time()) % 3 + 8)) + '@qq.com'
			password = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(int(time.time()) % 6 + 8))
			ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))) 

			response = requests.post(
				url = URL,
				data = {'u': username, 'p': password}, 
				headers = {'X-Forwarded-For': ip}, 
				timeout = 5,
			)
			print('ip:%s\tuser:%s\tpass:%s\t%s'%(ip, username, password, response))

		except Exception, e:
			print('timeout')
			time.sleep(1)


def main():

	thread.start_new_thread(send_junk_data, ())
	thread.start_new_thread(send_junk_data, ())
	thread.start_new_thread(send_junk_data, ())
	thread.start_new_thread(send_junk_data, ())

	while True:
		time.sleep(1024)

if __name__ == '__main__':
	main()
