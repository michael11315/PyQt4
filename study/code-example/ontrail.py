# 藏檔案驗證
def onTrail():
	path = 'C:/Python/recordMic'
	if not os.path.exists(path):
		os.makedirs(path)
		with open(path + '/log', 'w') as file:
			file.write('good 1 c')
	else:
		tmp =''
		with open(path + '/log', 'r') as file:
			for line in file:
				if line.startswith('good'):
					line = line.split()
					count = int(line[1]) + 1
					tmp = '%s %s %s' % (line[0], count, line[2])
		
		with open(path + '/log', 'w') as file:
			file.write(tmp)
	
	if os.path.exists(path):
		with open(path + '/log', 'r') as file:
			fine = True
			for line in file:
				if line.startswith('good'):
					line = line.split()
					if line[2] == 'r':
						fine = False
					elif int(line[1]) > 1000:
						fine = False
			if not fine:
				return False


# 時間驗證
def onTrail():
	timeNow = time.strftime('%Y %m %d %H', time.localtime(time.time())).split()
	yearNow = int(timeNow[0])
	monthNow = int(timeNow[1])
	dayNow = int(timeNow[2])
	hourNow = int(timeNow[3])
	
	if yearNow == 2016 and monthNow == 7 and dayNow <= 31 and dayNow >= 17:
		return True
	elif yearNow == 2016 and monthNow == 8 and dayNow <= 10 and dayNow >= 1:
		return True
	else:
		return False