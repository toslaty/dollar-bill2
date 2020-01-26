import os
import cmd
import sys
from corre import *
from getData import *
from fundamath import *


class Interp(cmd.Cmd):

	intro ="\nDollarbill greets you $$\n\n"
	prompt = '(Dollarbill$)'

	def do_get_corr(self,line):
		"""get_corr [symbol1] [symbol2] [YYYY-MM-DD] [YYYY-MM-DD]"""
		x = line.split(' ')
		#print(x)
		corr_stocks(x[0],x[1],x[2],x[3])

	#def do_get_beta(self, line):
		#x = line.split(' ')

	def do_get_prices(self, line):
		"""get_prices [Company Symbol] [DD/MM/YYYY] [DD/MM/YYYY]
		gets the prices from knoema for given symbol, startdate and enddate
		"""
		p = line.split(' ')	
		git_mo_prices(p[0],p[1], p[2])

	def do_adx(self,line):
		com = line.split('')
		average_dx(stock,start,end)

	#def do_get_most_profitable():	

	#def do_get_most_liquidity():

	#def do_set_mailalarm():

	#for testing purpoae after test it will be done automaticly
	def do_get_fundamental_ratios(self, line):
		y = line.split(' ')
		funda_api_test(y[0])

	def do_test_sql(self,line):
		"""tests sql to frame for further work"""
		y = line.split(' ') 
		t = get_funda(y[0])
		print(t)

	def do_get_fundamentals(self,line):
		"""get_fundamentals [Company Symbol] 
		gets the fundmental data for the given company"""
		x = line.split(' ')
		z = str(x[0])
		get_special(z)

	def do_print(self,line):
		print('Test')






