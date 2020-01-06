import sys
import time
import os
import logging
import datetime
import csv
import requests
import sqlite3
import pandas as pd
from zipfile import ZipFile

def configureLogger():
	log_format = "%(levelname)s [%(name)s] %(asctime)s - %(message)s"
	log_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'logs')
	log_fname = os.path.join(log_dir, 'cotacao_historica.log')

	if not os.path.exists(log_dir):
		os.makedirs(log_dir)
	
	logging.basicConfig (level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_fname),
            logging.StreamHandler(sys.stdout)])

def configureDatabase():
	print("sqlite3.version:{0}".format(sqlite3.version))
	print("sqlite3.sqlite_version:{0}".format(sqlite3.sqlite_version))
	database_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'database')
	script_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'scripts')

	database_fname = os.path.join(database_dir, 'dados.db')
	if not os.path.exists(database_dir):
		os.makedirs(database_dir)

	conn = sqlite3.connect(database_fname)
	cursor = conn.cursor()

	create_file = os.path.join(script_dir, '09_b3_historico_create.sql')
	
	with open(create_file, 'r') as content_file:
		content = content_file.read()
		cursor.execute(content)	

	conn.close()

def configureTemporaryFolder():
    temp_directory = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'tmp')    
    if not os.path.exists(temp_directory):
        os.makedirs(temp_directory)

def downloadHistoryFile(ano):
    logger = logging.getLogger(name="download")

    file_name = "COTAHIST_A{}.ZIP".format(ano)
    download_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'download')
    download_destination = os.path.join(download_dir, file_name)
    download_url = "http://bvmf.bmfbovespa.com.br/InstDados/SerHist/{}".format(file_name)
    
    logger.info("start download")
    
    with requests.Session() as s:
        download_content = s.get(download_url)
        open(download_destination,'wb').write(download_content.content)                 
    
    logger.info("finish download")
    return download_destination


def unzipLatest(source_zip_filepath, destination_filepath):
    zip_file = ZipFile(source_zip_filepath, 'r')
    all_files = zip_file.infolist()
    latest_file = sorted(all_files, key=lambda k: k.date_time, reverse=True)[0]

    if not os.path.exists(destination_filepath):
        os.makedirs(destination_filepath)

    zip_file.extract(latest_file,destination_filepath)
    file_to_read = os.path.join(destination_filepath, latest_file.filename)

    return file_to_read

def readHistoricFile(file_path):
    logger = logging.getLogger(name="reading")
    # Read in the table.
    colspecs=[
            [0,2],  #Type                                   = 0 + 2     = 2
            [2,10],  #TradeDate                             = 2 + 8     = 10
            [10,12], #BDICode                               = 10 + 2    = 12
            [12,24],#Ticker                                 = 12 + 12   = 24
            [24,27], #MarketTypeCode                        = 24 + 3    = 27
            [27,39],#ShortName                              = 27 + 12   = 39
            [39,49],#Specification                          = 39 + 10   = 49 
            [49,52],#ForwardDaysToExpiry                    = 49 + 3    = 52
            [52,56],#ReferenceCurrency                      = 52 + 4    = 56 
            [56,69],#Opening                                = 56 + 13   = 69 
            [69,82],#Maximum                                = 69 + 13   = 82
            [82,95],#Minimum                                = 82 + 13   = 95
            [95,108],#Average                               = 85 + 13   = 108
            [108,121],#Last                                 = 98 + 13   = 121 
            [121,134],#BestBidPrice                         = 111 + 13  = 134
            [134,147],#BestAskPrice                         = 124 + 13  = 147
            [147,152],#TradeQuantity                        = 137 + 5   = 152
            [152,170],#ContractQuantity                     = 142 + 18  = 170
            [170,188],#FinancialVolume                      = 160 + 18  = 188
            [188,201],#StrikePrice                          = 178 + 13  = 201
            [201,202],#StrikePriceCorrectionIndicator       = 191 + 1   = 202
            [202,210],#ExpiryDate                           = 192 + 8   = 210
            [210,217],#QuoteFactor                          = 200 + 7   = 217
            [217,230],#DollarOptionPointsStrikePrice        = 207 + 13  = 230
            [230,242],#ISIN                                 = 220 + 12  = 242
            [242,245]]#InstrumentDistributionNumber         = 232 + 3   = 245
    
    colnames=[
        'Type'
        ,'TradeDate'
        ,'BDICode'
        ,'Ticker'
        ,'MarketTypeCode'
        ,'ShortName'
        ,'Specification'
        ,'ForwardDaysToExpiry'
        ,'ReferenceCurrency'
        ,'Opening'
        ,'Maximum'
        ,'Minimum'
        ,'Average'
        ,'Last'
        ,'BestBidPrice'
        ,'BestAskPrice'
        ,'TradeQuantity'
        ,'ContractQuantity'
        ,'FinancialVolume'
        ,'StrikePrice'
        ,'StrikePriceCorrectionIndicator'
        ,'ExpiryDate'
        ,'QuoteFactor'
        ,'DollarOptionPointsStrikePrice'
        ,'ISIN'
        ,'InstrumentDistributionNumber']

    colconverters={
        'Opening': lambda x: float(x)/100.0
        ,'Maximum': lambda x: float(x)/100.0
        ,'Minimum': lambda x: float(x)/100.0
        ,'Average': lambda x: float(x)/100.0
        ,'Last': lambda x: float(x)/100.0
        ,'BestBidPrice': lambda x: float(x)/100.0
        ,'BestAskPrice': lambda x: float(x)/100.0
        ,'FinancialVolume': lambda x: float(x)/100.0
        ,'StrikePrice': lambda x: float(x)/100.0
        ,'DollarOptionPointsStrikePrice': lambda x: float(x)/100.0
        #,'TradeDate': lambda x: pd.to_datetime(str(x), format='%Y%m%d')       
    }

    logger.info("started reading")
    result = pd.read_fwf(file_path,
                        colspecs=colspecs, 
                        names=colnames,
                        converters=colconverters,
                        header=None,
                        skipfooter=1,
                        skiprows=1)

    logger.info("started convert date")
    #result['TradeDate'] = pd.to_datetime(result['TradeDate'].astype(str), format='%Y%m%d')
    logger.info("finished convert date")
    logger.info("finished reading")
   
    return result

def saveHistoricoDatabase(conteudo):
	logger = logging.getLogger(name="database")
	sql = ''

	database_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'database')
	script_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'scripts')

	database_fname = os.path.join(database_dir, 'dados.db')

	insert_file = os.path.join(script_dir, '10_b3_historico_insert.sql')
	with open(insert_file, 'r') as content_file:
		sql = content_file.read()
	
	conn = sqlite3.connect(database_fname)
	cursor = conn.cursor()
	
	tamanho_conteudo = len(conteudo)
	logger.info ("started saving {0} items to database".format(tamanho_conteudo))

	start = datetime.datetime.now()
	try:        
		for _ , row in conteudo.iterrows():     
			cursor.execute(sql, row)
			#print("entubado {} / {}".format(index,tamanho_conteudo))
			#updt(tamanho_conteudo,index)
	except sqlite3.Error as e:
		print ("sql error",e.args[0])
	except Exception as e:
		print ("generic error",str(e))
		
	# save data
	conn.commit()
	conn.close()
	finish = datetime.datetime.now()

	logger.info ("finished saving {0} items to database in {1}".format(tamanho_conteudo,(finish-start)))

def downloadUnzipAndSave(year):
    temp_directory = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'tmp')
    file_downloaded =  downloadHistoryFile(year) #'C:\python\importacao\download\COTAHIST_A2019.zip'
    if (file_downloaded != ""):
        file_to_read = unzipLatest(file_downloaded,temp_directory)
        result = readHistoricFile(file_to_read)
        #print(result.head())
        saveHistoricoDatabase(result)

def main():
    configureLogger()
    configureDatabase()
    configureTemporaryFolder()
    downloadUnzipAndSave(2019)
    downloadUnzipAndSave(2018)

if __name__ == "__main__":
	main()
