import pandas as pa 
import datetime as dt
from datetime import datetime
import argparse as ap 
import math
import sys
sys.path.append("/Dokumente/financepy/inter/")
from testshell import *


def corr_stocks(stocka,stockb,start,end):
	
	# = 
	#name2 = 

	fr = pa.read_csv(stock,parse_dates= True, index_col = 0)
	fr.drop(['Volume', 'Close', 'High', 'Low', 'Open'], 1, inplace = True)
	fr.rename(columns={"Adj Close" : name}, inplace = True)

	rng = fr.loc[start : end]

	return rng


def corr_stocks(ind):

	summ1 = ind[ind.columns[0]].sum()

	summ2 = ind[ind.columns[1]].sum(skipna = True)

	summ3 = (ind[ind.columns[0]] * ind[ind.columns[1]]).sum()

	summ4 = (ind[ind.columns[0]] * ind[ind.columns[0]]).sum()

	summ5 = (ind[ind.columns[1]] * ind[ind.columns[1]]).sum()

	t = float(len(ind.index))

	corr1 = t * summ3 - (summ1 * summ2) 

	corr2 = math.sqrt((t * summ4 - math.pow(summ1,2)) *(t * summ5 -math.pow(summ2,2)))

	correlation = corr1 / corr2

	return correlation

def main():

	interpreter = Interp()
	Interp().cmdloop()


	
	start = datetime.strptime(args.stimeframe,"%Y-%m-%d")
	end = datetime.strptime(args.etimeframe, "%Y-%m-%d")
		
	one = prep_data(args.first,start,end)
	two = prep_data(args.second,start,end)
	
	ind = pa.concat([one, two], axis=1)


	print(ind)

	print("The correlation between the stocks is :\n" + str(corr_stocks(ind)))

if __name__ == '__main__':
	main()