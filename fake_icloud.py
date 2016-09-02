#!/usr/bin/env python
# coding=utf-8
# find my iphone 钓鱼网站

import string, random
import requests
import time
import socket, struct
import thread, threading
from Queue import Queue
import re

# URL = 'http://icloud-capxz.com/Home/Save'
# URL = 'http://appcq-icloud.com/Home/Save'
# URL = 'http://123.60.77.99/Home/Save'
# URL = 'http://118.193.251.24/Home/Save'
# URL = 'http://118.193.251.18/Home/Save'

# fish_hosts = [
# 	'118.193.250.203',
# 	'118.193.250.206',
# 	'118.193.251.3',
# 	'118.193.251.5',
# 	'118.193.251.6',
# 	'118.193.251.10',
# 	'118.193.251.12',
# 	'118.193.251.15',
# 	'118.193.251.18',
# 	'118.193.251.22',
# 	'118.193.251.28',
# 	'123.60.77.100',
# 	'123.60.77.102',
# 	'123.60.77.115',
# 	'123.60.77.118',
# 	'123.60.77.125',

# 	'118.193.250.203',
# 	'123.60.77.108',
# 	'118.193.251.22',

# 	'103.42.28.217',
# 	'103.42.28.218',
# 	'103.230.123.166',
# 	'103.230.123.210',

# 	'122.9.163.10',
# 	'123.60.77.104',
# 	'123.60.77.102',
# 	'123.60.77.103',
# 	'123.60.77.106',
# 	'123.60.77.114',
# 	'123.60.77.122',
# ]

retry_count_dict = {}

def scan_find_my_iphone(host):
	try:
		url = 'http://%s/Home/Save' % host
		data = {'u': 'example@qq.com', 'p': 'test123456'}

		response = requests.post(
			url = url,
			data = data,
			timeout = 5,
		)

		if response.status_code == requests.codes.ok and response.json().get('type', '') == 'alert' and response.json().get('message', '') != '':
			return True

	except Exception, e:
		pass

	return False


def scan_worker(queue):

	# f = open('result.txt', 'w')
	# f.write('---------------- %s -----------------' % time.asctime(time.localtime(time.time())))

	while True:

		host = queue.get()
		if scan_find_my_iphone(host) == True:
			print(host)
			# f.write(host)

		queue.task_done()

def scanner():

	# (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
	# struct.unpack('>I',socket.inet_aton('127.0.0.1'))[0]
	# socket.inet_ntoa(struct.pack('>I', 2130706434))

	queue = Queue()

	print('开始扫描')
	for x in xrange(0, 500):
		t = threading.Thread(target = scan_worker, args = (queue,))
		t.daemon = True
		t.start()

	regx = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
	with open('香港ip段.txt') as f:
		for line in f.readlines():

			pm = re.search(regx, line)
			if pm == None:
				continue

			# print(pm.group())

			ip1 = pm.group(1)
			ip2 = pm.group(2)
			l = struct.unpack('>I',socket.inet_aton(ip1))[0]
			h = struct.unpack('>I',socket.inet_aton(ip2))[0]

			print('[%s --- %s]' % (ip1, ip2))
			for x in range(l, h):
				ip = socket.inet_ntoa(struct.pack('>I', x))
				queue.put(ip)

			queue.join()

	print('扫描结束.')

def send_junk_data(hosts):

	global retry_count_dict

	while True:

		host = hosts[int(time.time() * 1000) % len(hosts)]
		if retry_count_dict.get(host, 0) > 5:
			time.sleep(1)
			continue

		retry_count_dict[host] = retry_count_dict.get(host, 0) + 1

		try:
			
			url = 'http://%s/Home/Save' % host

			username = ''.join(random.choice(string.digits) for _ in range(int(time.time()) % 3 + 8)) + '@qq.com'
			password = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(int(time.time()) % 6 + 8))
			fake_ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))) 

			# username = 'jbdb29@sina.com'
			# password = 'Aa112211'

			response = requests.post(
				url = url,
				data = {'u': username, 'p': password}, 
				headers = {'X-Forwarded-For': fake_ip, 'Connection': 'close'}, 
				timeout = 5,
			)
			if response.status_code == requests.codes.ok:
				print('%s\t%s'%(host, response.text))
				retry_count_dict[host] = 0
			else:
				print(response)
				# print(response.text)

		except Exception, e:
			print(e)
			time.sleep(1)

def sender():

	fish_hosts = []
	regx = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
	with open('result.txt') as f:
		for line in f.readlines():
			pm = re.search(regx, line)
			if pm == None:
				continue

			ip = pm.group(0)
			fish_hosts.append(ip)


	print('开始发送')
	for x in xrange(0, 10):
		t = threading.Thread(target = send_junk_data, args = (fish_hosts, ))
		t.daemon = True
		t.start()

	raw_input()

def main():
	# scanner()
	sender()

if __name__ == '__main__':
	main()
