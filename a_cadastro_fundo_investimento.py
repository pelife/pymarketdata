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
	log_fname = os.path.join(log_dir, 'cadastro_fundo_investimento.log')

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

	create_file = os.path.join(os.path.normpath(os.getcwd() + os.sep + 'scripts'), '01_cvm_cadastro_fundo_investimento_create_table.sql')
	
	with open(create_file, 'r') as content_file:
		content = content_file.read()
		cursor.execute(content)	

	conn.close()

def downloadFundosFile():
	logger = logging.getLogger(name="download")

	download_url = "http://dados.cvm.gov.br/dados/FI/CAD/DADOS/inf_cadastral_fi_20190515.csv"
	#download_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'download')	

	logger.info("start download")

	with requests.Session() as s:
		download_content = s.get(download_url)
		decoded_content = download_content.content.decode('latin-1')
		#parsed_content = csv.reader(decoded_content.splitlines(), delimiter=';')
		parsed_content = csv.DictReader(decoded_content.splitlines(), delimiter=';')
		content_list = list(parsed_content)
		#content_list  = parsed_content
	
	logger.info("finish download")

	return content_list

def saveFundosDatabase(conteudo):
	logger = logging.getLogger(name="database")
	sql = ''

	database_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'database')	
	database_fname = os.path.join(database_dir, 'dados.db')

	insert_file = os.path.join(os.path.normpath(os.getcwd() + os.sep + 'scripts'), '02_cvm_cadastro_fundo_investimento_insert.sql')
	with open(insert_file, 'r') as content_file:
		sql = content_file.read()
	
	conn = sqlite3.connect(database_fname)
	cursor = conn.cursor()
	
	tamanho_conteudo = len(conteudo)
	logger.info ("started saving {0} items to database".format(tamanho_conteudo))

	start = datetime.datetime.now()
	for i in range(1, tamanho_conteudo):
		if (conteudo[i]["DT_CANCEL"]== ''):
			conteudo[i]["DT_CANCEL"]= None
		
		cursor.execute(sql, conteudo[i])
		
	# save data
	conn.commit()
	conn.close()
	finish = datetime.datetime.now()

	logger.info ("finished saving {0} items to database in {1}".format(tamanho_conteudo,(finish-start)))

def downloadAndSave():
	content_list = downloadFundosFile()
	saveFundosDatabase(content_list)

def main():
	configureLogger()
	configureDownload()
	configureDatabase()
	
	downloadAndSave()	

if __name__ == "__main__":
	main()