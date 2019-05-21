import knoema
import requests
import pandas as pa

def get_stock_us(sym,start,end):


	frame = knoema.get('USINDSSP2017', **{'timerange': start+'-'+end,
			'frequency': 'D',
			'Company': sym,
			'indicator': 'KN.A1;KN.A2;KN.A3;KN.A4;KN.A5'
			})

	return frame

#def get_world():


