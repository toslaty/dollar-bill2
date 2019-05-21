import pandas as pa 
import datetime as dt
import math
import sys
from testshell import *
from dbase import checkDB


def main():

	#if not checkDB():
	#get_newest()
	get_ratios()

	#need to write checkDate()
	#if not checkDate():
	#	get_all_prices()	

	interpreter = Interp()
	Interp().cmdloop()

	
if __name__ == '__main__':
	main()