from sqlalchemy import create_engine
from sqlalchemy import VARCHAR
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import inspect
import pandas as pa


engine = create_engine('mysql://dollar-bill:dollar_bill@localhost/company_fundamentals', pool_recycle= 3600) 
engine2 = create_engine('mysql://phpmyadmin:Datenbanken@localhost/company_daily', pool_recycle= 3600)
engine3 = create_engine('mysql://dollar-bill:dollar_bill@localhost/company_ratios', pool_recycle = 3600)

def checkDB():

	x = database_exists(engine.url)
	return x


def frame_to_db(frame,symbol):

	if not database_exists(engine.url):
			create_database(engine.url, encoding= 'utf8')

	connection = engine.connect()
	print(frame.index.name)

	frame.to_sql(symbol, con = engine, if_exists='replace', dtype={frame.index.name:VARCHAR(50)})
	print(symbol+" is now in Database!")


def fundas_to_db(frame, symbol):

	if not database_exists(engine3.url):
		create_database(engine3.url, encoding = 'utf8')

	connection = engine3.connect()

	frame.set_index('ID')
	frame.to_sql(symbol, con = engine3, if_exists = 'replace', index = True, index_label = 'id')
	print(symbol +" ratios in db")

#prices from knoema to DB
def prices_to_db(frame, symbol):
	
	if not database_exists(engine2.url):
		create_database(engine2.url, encoding = 'utf8')

	connection = engine2.connect()

	frame.to_sql(symbol, con = engine2, if_exists='replace', index = True, index_label = 'dt')

#gets fundamentals from database
def get_funda(sym):
		
	connection = engine.connect()
	dbquery = "SELECT * From " +sym

	try:
		frame = pa.read_sql('SELECT * FROM '+str(sym), index_col = 'entry', con = engine)
		return frame
	except Exception as e:
		print(e)	
	

def get_prices(sym,start,end):  
	
	connect = engine2.connect()

	dbquery = "SELECT Close, dt FROM "+str(sym)+" WHERE dt BETWEEN DATE('"+str(start)+"') AND DATE('"+str(end)+"');"
	print(dbquery)
	frame = pa.read_sql(dbquery, con = engine2, index_col= 'dt')
	print(frame)

	return frame

#get the names of all companies in the db
def get_names():

	companies = [] 
	inspector = inspect(engine)
	the_names = inspector.get_table_names()

	for table_name in the_names:
		companies.append(table_name)
	return(companies)

