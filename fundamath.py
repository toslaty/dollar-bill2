import math
import numpy as np
import pandas as pa
from dbase import *


def get_funda_ratios(sym):
	
	frame = get_funda(sym)
	frame  = frame.drop(columns = 'id')

	ind = ['current_ratio','acid-test_ratio','cash_ratio','operating_cash_flow',
	'debt_ratio','debt_to_equity','interest_coverage_ratio','gross_profit_margin',
	'net_profit_margin', 'return_on_equity','return_on_assets']

	r_frame = pa.DataFrame(index = ind, columns = frame.columns)

	r_frame.loc['current_ratio'] = frame.loc['Total Current Assets'] / frame.loc['Total Current Liabilities']

	r_frame.loc['acid-test_ratio'] = (frame.loc['Total Current Assets'] - frame.loc['Inventory']) / frame.loc['Total Current Liabilities']

	r_frame.loc['cash_ratio'] = frame.loc['Cash And Cash Equivalents'] / frame.loc['Total Current Liabilities']
	
	r_frame.loc['operating_cash_flow'] = frame.loc['Total Cash Flow From Operating Activities'] / frame.loc['Total Current Liabilities']


	r_frame.loc['debt_ratio'] = frame.loc['Total Liabilities'] / frame.loc['Total Assets']

	r_frame.loc['debt_to_equity'] = frame.loc['Total Liabilities'] / frame.loc['Total Stockholder Equity']

	r_frame.loc['interest_coverage_ratio'] = frame.iloc[8] / frame.iloc[11]


	r_frame.loc['gross_profit_margin'] = frame.loc['Gross Profit'] / frame.loc['Total Revenue']

	r_frame.loc['net_profit_margin'] = frame.loc['Net Income'] / frame.loc['Total Revenue']


	r_frame.loc['return_on_equity'] = frame.loc['Net Income'] / frame.loc['Total Stockholder Equity']

	r_frame.loc['return_on_assets'] = frame.loc['Net Income'] / frame.loc['Total Assets']


	#r_frame.loc[''] = frame.loc[''] / frame.loc[]

	r_frame.replace(np.inf, 0, inplace=True)
	print(r_frame)

	fundas_to_db(r_frame, sym)

