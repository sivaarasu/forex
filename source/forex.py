import urllib2
import csv
import pickle
from datetime import date
from datetime import timedelta
from time import sleep
from datetime import datetime
##
#for now we need all currency 
#from SGD to local or vice versa
#from USD to local or vice versa
#
##
#forex will help in giving exchange rates information for a given date
#this is fucking awesome
#
##
#
#pickle structure
#
# date:
# 	from:
# 		to:1
# 		to:2
# 		to:3
# 		...
# 	from:
# 		to:1
# 		to:2
# 		to:3
# 		...
# date:
# 	from:
# 		...
# 		
# EXAMPLE INPUT
# 
# ('2014-11-1', 'SGD', 'PHP')

CURRENCY_FROM = ['USD', 'SGD']
CURRENCY_TO = ['THB', 'SGD', 'MYR', 'IDR', 'PHP', 'VND']
PICKLE = 'lzd.forex.dat'
TMP_FILE = '/tmp/boo'
class forex:

	currency_value = {}
	today = (date.today()).strftime('%Y-%-m-%-d')
	def get_currency(self, dt, f, to):
		currency = self.__read_pickle()
		try:
			return float(currency[dt][f][to].replace(',', ''))
		except Exception, e:
			#here the currency is not present i pickle
			try:
				return self.__call_oanda(dt, f, to)
			except Exception, e:
				return None


	def cron(self):
		csv_var = {}
		for currency_from in CURRENCY_FROM:
			csv_var[currency_from] = {}
			for currency_to in CURRENCY_TO:
				sleep(1)
				try:
					csv_var[currency_from][currency_to] = self.__call_oanda(
						self.today, currency_from, currency_to)
				except Exception, e:
					print str(e)
					csv_var[currency_from][currency_to] = 0

		self.__write_pickle(csv_var)

	def __write_pickle(self, currency_value):
		pk = self.__read_pickle()
		pk[self.today] = currency_value;

		try:
			f = open(PICKLE, 'w')
			pickle.dump(pk, f)
		except Exception, e:
			print str(e)

	def __read_pickle(self):
		try:
			f = open(PICKLE, 'r')
			pk = pickle.load(f)
		except Exception, e:
			pk = {}
		
		return pk
	#
	#cron will get the given date's exchange rate
	def __call_oanda(self, start_date, currency_from, currency_to):
		if currency_from == currency_to:
			return float(1)
		
		url = "http://www.oanda.com/currency/historical-rates/" +\
			"download?quote_currency=" + currency_from + "&end_date=2015-8-24&" +\
			"start_date=" + start_date + "&period=daily&display=absolute&" +\
			"rate=0&data_range=c&price=bid&view=table&" +\
			"base_currency_0=" + currency_to + "&download=csv"
		dt_format = datetime.strptime(start_date, '%Y-%m-%d').date().strftime('%-d-%-m-%Y')
		currencyfile = urllib2.urlopen(url)
		f = open(TMP_FILE, 'w')
		f.write(currencyfile.read())
		f.close()
		f = open(TMP_FILE, 'r')
		for cell in list(csv.reader(f, delimiter=',', quotechar='"')):
			try:
				cell[0]
			except Exception, e:
				print str(e)
			if cell[0] == start_date:
				return float(cell[1].replace(',', ''))

		raise Exception('Invalid CSV')


#c = forex()
# #c.cron()
#print float(c.get_currency('2014-11-16', 'SGD', 'VND')) * 1000
