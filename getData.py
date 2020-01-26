import os
import requests
import datetime as dt
from datetime import datetime
import pandas as pa
import pandas_datareader as web 
import bs4 as bs
import re
import string
from dbase import *
from fundamath import *
from knoema_req import *
import json


def scrape_wiki_sp500():

	req = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

	soup = bs.BeautifulSoup(req.text, 'html5lib')
	table = soup.find('table', {'class' : 'wikitable sortable'})
	symbols = []

	for row in table.findAll('tr')[1:] :
		symbol = row.findAll('td')[0].text.strip("\n")
		symbols.append(symbol)

	return symbols


def get_newest():

	companies = scrape_wiki_sp500()
	for i in companies:
		print('tryin '+i)
		get_special(i)


def get_ratios():

	companies = get_names()
	for i in companies:
		print(i)
		get_funda_ratios(i)


def table_stuff(req):

	supp = bs.BeautifulSoup(req.text, 'html5lib')
	tables = supp.findAll('table')
	outputs = []
	regexp = re.compile('[\.]+')

	for table in tables:
		for row in table.findAll('tr'):
			for cell in row.findAll('td'):
				if not(len(row) < 2):
					first = cell.text
					if(re.search(regexp,first)):
						first.split('.')
						outputs.append(first[0])
					else:
						outputs.append(first)

	return outputs			


def check_chars(list):

	numbers =[]
	regex = re.compile('[a-z]+')
	for i in list[5::]:
		if not(regex.search(i)):
			numbers.append(i)	

	return numbers		


def data_to_frame(cols, nlist,clist):
	
	print(nlist)

	if(len(cols) == 4):
		frame = pa.DataFrame(index = clist[5::5], columns = cols)
		for x in range(4):#nlist
			frame[cols[x]] = pa.Series(nlist[x::4], index = clist[5::5])

	elif(len(cols) == 3):
		frame = pa.DataFrame(index=clist[4::4], columns = cols)
		for x in range(3):
			frame[cols[x]] = pa.Series(nlist[x::3], index = clist[4::4])

	return frame

# Splits the string so we get the columns for the fundamental data
def splitter(rev):
	cols = []

	if(len(rev) < 5):
		for w in rev:
			wort = w.split('/')
			cols.append(wort[2])

	return cols

#kills comma in number cats everything to int64 and times 1000 because numbers o yahoo in thousands
def real_numbers(alldata):

	for col in alldata.columns[1:]:

		alldata[col] = alldata[col].replace(',' , '', regex = True)
		alldata[col] = alldata[col].astype('int64')
		alldata[col] = alldata[col] * 1000

	return alldata


# Gets the fundamental data for the given symbol from yahoo with the hardcoded addresses below
def get_special(symbol):

	symbol = symbol

	url2 = 'https://finance.yahoo.com/quote/'+symbol+'/financials?p='+symbol
	url3 = 'https://finance.yahoo.com/quote/'+symbol+'/balance-sheet?p='+symbol
	url4 = 'https://finance.yahoo.com/quote/'+symbol+'/cash-flow?p='+symbol

	y = requests.get(url2)
	z = requests.get(url3)
	c = requests.get(url4)
	revenue = table_stuff(y)
	balance = table_stuff(z)
	cflow = table_stuff(c)

	if(len(revenue) > 5):

		#looks for numeric in revenue[5] becuase some entries only have three cols
		regexp = re.compile('[0-9]+')
		if (regexp.search(revenue[5])):
			cols = splitter(revenue[1:4])
		else:
			cols = splitter(revenue[1:5])

		rnumbers = check_chars(revenue)
		bnumbers = check_chars(balance)
		cfnumbers= check_chars(cflow)

		rframe = data_to_frame(cols, rnumbers,revenue)
		bframe = data_to_frame(cols, bnumbers, balance)
		cfframe = data_to_frame(cols, cfnumbers, cflow)

		frames = [rframe,bframe,cfframe]

		alldata = pa.concat(frames, axis = 0)
		alldata.reset_index(inplace = True)
		alldata.replace('-', 0,inplace = True)
		real_numbers(alldata)

		frame_to_db(alldata, symbol)

	else:

		print('No data available\n')
		#takes index from other df to create empty df and fill with 0 for later iteration
		frame2 = get_funda('ABT')

		empty = pa.DataFrame(columns=['index', 2019, 2018, 2017,2016], index= frame2.index)
		empty['index'] = frame2.index
		empty = empty.fillna(0)
		frame_to_db(empty, symbol)


#gets the price from knoema for sym
def git_prices(sym, start, end):

	df = get_stock_us(sym,start,end)

	cols1 = df.columns.names
	cols1 = cols1[:4]

	df.columns = ['Close', 'High', 'Low', 'Open', 'Volume']

	prices_to_db(df ,sym)

def git_mo_prices(sym,start,end):

	req_string = 'https://eodhistoricaldata.com/api/eod/'+sym+'?from='+start+'&to='+end+'&api_token=5cfe8b81ad5ad8.95709345&fmt=json'
	print(req_string)

	resp = requests.get(req_string)

	patest = pa.read_json(resp.text)

	print(patest)
	prices_to_db(patest,sym)

def funda_api_test(sym):

	req_string = 'https://eodhistoricaldata.com/api/fundamentals/'+sym+'?api_token=OeAFFmMliFG5orCUuwAKQ8l4WWFQ67YX&filter=Financials::Balance_Sheet::yearly'

	resp = requests.get(req_string)
	print(resp.text)

	patest2 = pa.read_json(resp.text)
	print(patest2)