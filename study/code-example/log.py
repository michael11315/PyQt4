def log(msg):
	try:
		path = 'log'
		if not os.path.exists(path):
			os.makedirs(path)
		
		filename = path + '/%s.log' % startTime
		timeNow = time.strftime('%Y%m%d %H:%M:%S', time.localtime(time.time()))
		with open(filename, 'a') as file:
			file.write('[%s] %s\n' % (timeNow, str(msg)))
	except:
		pass