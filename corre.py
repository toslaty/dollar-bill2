import pandas as pa
import math
import datetime as dt 
from datetime import datetime
from dbase import *


def corr_stocks(stocka,stockb,start,end):
	
	name1 = stocka	
	name2 = stockb

	fr1 = get_prices(name1,start,end)

	fr2 = get_prices(name2,start,end)
	print(fr1)

	fr1.rename(columns={"Close" : name1}, inplace = True)
	fr2.rename(columns={"Close" : name2}, inplace = True)

	ind = pa.concat([fr1,fr2], axis = 1)
	print(ind)

	mathemagic(ind)


def mathemagic(ind):
	
	summ1 = ind[ind.columns[0]].sum()

	summ2 = ind[ind.columns[1]].sum()

	summ3 = (ind[ind.columns[0]] * ind[ind.columns[1]]).sum()

	summ4 = (ind[ind.columns[0]] * ind[ind.columns[0]]).sum()

	summ5 = (ind[ind.columns[1]] * ind[ind.columns[1]]).sum()

	t = float(len(ind.index))

	corr1 = t * summ3 - (summ1 * summ2) 

	corr2 = math.sqrt((t * summ4 - math.pow(summ1,2)) *(t * summ5 -math.pow(summ2,2)))

	correlation = corr1 / corr2

	print(correlation)


def average_dx(stock, start, end):

	the_stock = get_prices(stock, start, end)

	print(the_stock)

#add period for RSI testing is 14
def relative_strength(sym,start, end):

	period = 14
	stock = get_prices(stock,start,end)

	print(stock)

#	avg_gain = 
#	avg_loss =



