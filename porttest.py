from socket import socket, gethostbyname, AF_INET, SOCK_STREAM
import time
import datetime
import sqlite3
import os
import http.client
import sys



import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def connect(filedb):
	if not os.path.exists(filedb):
		# Создание таблицы
		conn = sqlite3.connect(filedb) # или :memory: чтобы сохранить в RAM
		cursor = conn.cursor()
		cursor.execute('CREATE TABLE log (datetime datetime, destination VARCRCHAR(100), target VARCRCHAR(100), port INTEGER, available boolean)')
		# cursor.execute('CREATE TABLE logg (port INTEGER, available INTEGER)')
		conn.commit()
	else:
		conn = sqlite3.connect(filedb)
	return conn





def stat(conn, target, port):
	connhttp = http.client.HTTPConnection("ifconfig.me")
	connhttp.request("GET", "/ip")
	myip = connhttp.getresponse().read()
	destination = myip.decode("utf-8")
	# //'123.45.67.89\n'
	# destination = ''

	cursor = conn.cursor()
	targetIP = gethostbyname(target)


	now = datetime.datetime.now()
	s = socket(AF_INET, SOCK_STREAM)

	result = s.connect_ex((targetIP, port))
	if (result == 0) :
		message = f'{now} Порт {port} на IP адресі  {target} відкритий'
		available = True
	else:
		message = f'{now} Порт {port} на IP адресі  {target} наразі не відповідає'
		available = False
	s.close()
	print(message)
	# Вставляем данные в таблицу
	cursor.execute('INSERT INTO log VALUES (:now, :destination, :target, :port, :available)', {'now':now, 'destination':destination, 'target':target, 'port':port, 'available':available} )
	# cursor.execute('INSERT INTO logg VALUES (:now)', {'now':now} )
	    # cursor.execute("SELECT Name from Artist ORDER BY Name LIMIT :limit", {"limit": 3})
	conn.commit() 





def histogram(data, n_bins, cumulative=False, x_label = "", y_label = "", title = ""):
    _, ax = plt.subplots()
    ax.hist(data, n_bins = n_bins, cumulative = cumulative, color = '#539caf')
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title(title)
    


def report(conn, ssstring):
	cursor = conn.cursor()
	# for row in cursor.execute("SELECT strftime('%s','datetime'), destination, target, port, available from log"):
	# for row in cursor.execute("SELECT strftime('%H',datetime), destination, target, port, available from log"):
	dates = []
	values = {}
	dpi = 80
	fig = plt.figure(dpi = dpi, figsize = (512 / dpi, 384 / dpi) )
	mpl.rcParams.update({'font.size': 10})

	plt.title('RU New Domain Names Registration')
	plt.xlabel('Year')
	plt.ylabel('Domains')

	ax = plt.axes()
	ax.yaxis.grid(True)
	ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
	ax.xaxis.set_major_locator(mdates.YearLocator())

	for row in cursor.execute("SELECT strftime('%H',datetime) As H, destination, target, port, available AS A from log"):
		# print(row.H)		
		plt.plot(row[0], row[4], linestyle = 'solid', label = 'aaa')
		print(row[0])
		print(row[4])

 		# df['one'].values 
		# print(row)

	plt.legend(loc='upper left', frameon = False)
	fig.savefig('diagram.png')


	print('hello')



def report1(conn, ssstring):
	import numpy as np
	import matplotlib.pyplot as plt
	from matplotlib import dates
	import datetime as dt
	cursor = conn.cursor()


	fmt = dates.DateFormatter('%H:%M:%S')

	fig, ax = plt.subplots()

	# time_interval = ['19:0:0', '19:1:0', '19:2:0', '19:3:0', '19:4:0']
	# time_interval = ['00:0:0', '01:0:0', '02:0:0', '3:0:0', '19:4:0']
	
	# time_interval = [dt.datetime.strptime(i, "%H:%M:%S") for i in time_interval]



	sqltext1 = """
				DROP VIEW IF EXISTS alltimes
				;

				 CREATE TEMP VIEW IF NOT EXISTS alltimes (hh)
				 AS 
				 select '00' 
				 union ALL
				 select '01' 
				 union all
				 select '02' 
				 union all
				 select '03' 
				 union all
				 select '04'
				 union all
				 select '05'
				  union all
				 select '06'
				 union all
				 select '07'
				 union all
				 select '08'
				 union all
				 select '09'
				 union all
				 select '10'
				 union all
				 select '11'
				 union all
				 select '12'
				 union all
				 select '13'
				 union all
				 select '14'
				 union all
				 select '15'
				 union all
				 select '16'
				 union all
				 select '17'
				 union all
				 select '18'
				 union all
				 select '19'
				 union all
				 select '20'
				 union all
				 select '21'
				 union all
				 select '22'
				 union all
				 select '23'
				 
				 ; 
				 drop VIEW IF EXISTS timesinfo
				 
				 ;
				 CREATE TEMP VIEW IF NOT EXISTS timesinfo  AS 
				 SELECT strftime('%H', datetime) as hh,  round(avg(available), 0) as available from log GROUP by  strftime('%H', datetime)
				 
				 
				"""

			


	sqltext = """
				SELECT alltimes.hh AS hh, timesinfo.available AS available from alltimes as alltimes  LEFT JOIN timesinfo  AS timesinfo  ON  alltimes.hh = timesinfo.hh
				"""
				 
	cursor.executescript(sqltext1)

	times = []
	values_on = []
	values_off = []
	values_v = []

	# times.append('10')
	# values.append(2)

	# for row in cursor.execute("SELECT datetime, available from log"):
	for row in cursor.execute(sqltext):
	# zz = cursor.executescript(sqltext)
	# print(zz)
	# for row in zz:
		vOn = 0
		vOff = 0 
		vV = 0
		print(row[0])
		print(row[1])
		times.append(row[0]) 
		if row[1] == None:
			vV = 1
		if row[1] == 1.0:
			vOn = 1
		if row[1] == 0:
			vOff = 1	

		values_on.append(vOn)
		values_off.append(vOff)
		values_v.append(vV)
	
		

	# y = np.random.randn( 10  )
	# x = np.array([x for x in range(  len(time_interval)   )])


	# ax.plot(times, values_on, color="g") #наносим график доллара: оси x и y. Цвет зелёный.
	# plt.title("Доступність за ...", fontsize=20)


# !!!!!!!!!!!!!!!!!!!!
# SELECT strftime('%H', datetime),  avg(available), round(avg(available), 0) , CAST(avg(available) AS INTEGER )from log GROUP by  strftime('%H', datetime)




	# ax.xaxis.set_major_locator(dates.YearLocator(1)) #делаем так, чтобы на оси дат были не числа типа 10.12.2018, а только годы
	# ax.xaxis.set_major_formatter(dates.DateFormatter('%Y')) #формат оси x - годы.
	# plt.grid() #наносим сетку.
	# plt.show() #показываем график!

	
	# ax.plot(time_interval, y, "-o")
	# ax.xaxis.set_major_formatter(fmt)
	# fig.autofmt_xdate()
	# # plt.show()
	# fig.savefig('diagram.png')
	# conn.close()


	fig, ax = plt.subplots()
  	# _, ax = plt.subplots()
    # ax.hist(data, n_bins = n_bins, cumulative = cumulative, color = '#539caf')
	ax.bar(times, values_on,  color = 'g')
	ax.bar(times, values_off, color = 'r')
	
	plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

	ax.set_yticklabels([]) 




	# ax.set_ylabel("")
	ax.set_xlabel("Години доби")
	ax.set_title("Доступність")


	# import matplotlib.patches as mpatches
	# red_patch = mpatches.Patch(color='red', label='The red data')
	# plt.legend(handles=[red_patch])



	fig.savefig('diagram1.png')



