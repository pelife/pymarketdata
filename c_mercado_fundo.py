import os
import sys
import logging
import time
import datetime
import csv
import requests
import sqlite3

def configureLogger():
	log_format = "%(levelname)s [%(name)s] %(asctime)s - %(message)s"
	log_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'logs')
	log_fname = os.path.join(log_dir, 'mercado_fundo.log')

	if not os.path.exists(log_dir):
		os.makedirs(log_dir)
	
	logging.basicConfig (level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_fname),
            logging.StreamHandler(sys.stdout)])

def configureDownload():
	download_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'download')	
	if not os.path.exists(download_dir):
		os.makedirs(download_dir)

def configureDatabase():
	print("sqlite3.version:{0}".format(sqlite3.version))	
	database_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'database')	
	database_fname = os.path.join(database_dir, 'dados.db')
	if not os.path.exists(database_dir):
		os.makedirs(database_dir)

	conn = sqlite3.connect(database_fname)
	cursor = conn.cursor()

	create_file = os.path.join(os.path.normpath(os.getcwd() + os.sep + 'scripts'), '05_cvm_mercado_fundo_create_table.sql')
	
	with open(create_file, 'r') as content_file:
		content = content_file.read()
		cursor.execute(content)	

	conn.close()

def generateYearMonth(quantity):
	yearMonth = []
	today = datetime.datetime.today()

	currentMonth = today.month
	currentYear = today.year
	for _ in range(0, quantity):
		yearMonth.append(tuple((currentYear, currentMonth)))
		if (currentMonth == 1):
			currentMonth = 12
			currentYear = currentYear - 1
		else:
			currentMonth = currentMonth -1

	return yearMonth

def saveFundosDatabase(conteudo):
	logger = logging.getLogger(name="database")
	sql = ''

	database_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'database')	
	database_fname = os.path.join(database_dir, 'dados.db')

	insert_file = os.path.join(os.path.normpath(os.getcwd() + os.sep + 'scripts'), '06_cvm_mercado_fundo_insert.sql')
	with open(insert_file, 'r') as content_file:
		sql = content_file.read()
	
	conn = sqlite3.connect(database_fname)
	cursor = conn.cursor()
	
	tamanho_conteudo = len(conteudo)
	logger.info ("started saving {0} items to database".format(tamanho_conteudo))

	start = datetime.datetime.now()
	for i in range(1, tamanho_conteudo):
		cursor.execute(sql, conteudo[i])
		
	# save data
	conn.commit()
	conn.close()
	finish = datetime.datetime.now()

	logger.info ("finished saving {0} items to database in {1}".format(tamanho_conteudo,(finish-start)))

def downloadFundosFile(year,month):
	logger = logging.getLogger(name="download")

	year_month = "{0}/{1:02d}".format(year,month)
	download_url = "http://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/inf_diario_fi_{0}{1:02d}.csv".format(year,month)
	#download_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'download')	

	logger.info("start download "+year_month)

	with requests.Session() as s:
		download_content = s.get(download_url)
		decoded_content = download_content.content.decode('latin-1')
		#parsed_content = csv.reader(decoded_content.splitlines(), delimiter=';')
		parsed_content = csv.DictReader(decoded_content.splitlines(), delimiter=';')
		content_list = list(parsed_content)
		#content_list  = parsed_content
	
	logger.info("finished download "+year_month)

	return content_list

def downlaodAndSave(year, month):
	content_list = downloadFundosFile(year,month)    
	saveFundosDatabase(content_list)

def main():

	#today = datetime.datetime.today()
	configureLogger()
	configureDownload()
	configureDatabase()

	list_year_month = generateYearMonth(50)
	for year_month in list_year_month:    
		downlaodAndSave(year_month[0],year_month[1])
	# years = [2019,2018,2017,2016,2015]
	# month = [1,2,3,4,5,6,7,8,9,10,11,12]
	# year_month =list(itertools.product(years,month))

	# for i in len(year_month):
	# 	if (i>numberOfMonth):
	# 		break
	# 	content_list = downloadFundosFile(year_month[i][1],year_month[i][2])    
	
if __name__ == "__main__":
	main()