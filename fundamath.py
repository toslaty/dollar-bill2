import math
import numpy as np
import pandas as pa
from dbase import *


def get_funda_ratios(sym):
	
	frame = get_funda(sym)

	ind = ['current_ratio','acid-test_ratio','cash_ratio','operating_cash_flow',
	'debt_ratio','debt_to_equity','gross_profit_margin',
	'net_profit_margin', 'return_on_equity','return_on_assets']

	r_frame = pa.DataFrame(index = ind, columns = frame.columns)

	r_frame.loc['current_ratio'] = frame.loc['totalCurrentAssets'] / frame.loc['totalCurrentLiabilities']

	r_frame.loc['acid-test_ratio'] = (frame.loc['totalCurrentAssets'] - frame.loc['inventory']) / frame.loc['totalCurrentLiabilities']

	r_frame.loc['cash_ratio'] = frame.loc['cash'] / frame.loc['totalCurrentLiabilities']
	
	r_frame.loc['operating_cash_flow'] = frame.loc['totalCashFromOperatingActivities'] / frame.loc['totalCurrentLiabilities']


	r_frame.loc['debt_ratio'] = frame.loc['totalLiab'] / frame.loc['totalAssets']

	r_frame.loc['debt_to_equity'] = frame.loc['totalLiab'] / frame.loc['totalStockholderEquity']

	#needs to be done
	#r_frame.loc['interest_coverage_ratio'] = frame.iloc[8] / frame.iloc[11]#


	r_frame.loc['gross_profit_margin'] = frame.loc['grossProfit'] / frame.loc['totalRevenue']

	r_frame.loc['net_profit_margin'] = frame.loc['netIncome'] / frame.loc['totalRevenue']


	r_frame.loc['return_on_equity'] = frame.loc['netIncome'] / frame.loc['totalStockholderEquity']

	r_frame.loc['return_on_assets'] = frame.loc['netIncome'] / frame.loc['totalAssets']

	#r_frame.loc[''] = frame.loc[''] / frame.loc[]

	r_frame.replace(np.inf, 0, inplace=True)
	print(r_frame)

	fundas_to_db(r_frame, sym)

