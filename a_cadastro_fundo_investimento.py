import os
import sys
import logging
import time
import datetime
import csv
import requests
import sqlite3
import psycopg2
import pandas as pd
import numbers as np
import io
from sqlalchemy import create_engine

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

def convertDate (x):
	if x != x:
		return None
	return datetime.datetime.strptime(str(x), '%Y-%m-%d')

def downloadFundosFile():
	logger = logging.getLogger(name="download")	
	
	download_url = "http://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv"	

	dtypes={'TP_FUNDO': str
		,'CNPJ_FUNDO': str
		,'DENOM_SOCIAL': str
		#,'DT_REG': 'datetime'
		#,'DT_CONST': 'datetime'
		,'CD_CVM': pd.Int32Dtype()
		#,'DT_CANCEL': 'datetime'
		,'SIT': str
		#,'DT_INI_SIT': 'datetime'
		#,'DT_INI_ATIV': 'datetime'
		#,'DT_INI_EXERC': 'datetime'
		#,'DT_FIM_EXERC': 'datetime'
		,'CLASSE': str
		#,'DT_INI_CLASSE': 'datetime'
		,'RENTAB_FUNDO': str
		,'CONDOM': str
		,'FUNDO_COTAS': str
		,'FUNDO_EXCLUSIVO': str
		,'TRIB_LPRAZO': str
		,'INVEST_QUALIF': str
		,'ENTID_INVEST': str
		,'TAXA_PERFM': float
		,'INF_TAXA_PERFM': str
		,'TAXA_ADM': float
		,'INF_TAXA_ADM': str
		,'VL_PATRIM_LIQ': float
		#,'DT_PATRIM_LIQ': 'datetime'
		,'DIRETOR': str
		,'CNPJ_ADMIN': str
		,'ADMIN': str
		,'PF_PJ_GESTOR': str
		,'CPF_CNPJ_GESTOR': str
		,'GESTOR': str
		,'CNPJ_AUDITOR': str
		,'AUDITOR': str
		,'CNPJ_CUSTODIANTE': str
		,'CUSTODIANTE': str
		,'CNPJ_CONTROLADOR': str
		,'CONTROLADOR': str		
		}
	
	dates_columns= ['DT_REG','DT_CONST','DT_CANCEL','DT_INI_SIT','DT_INI_ATIV','DT_INI_EXERC','DT_FIM_EXERC','DT_INI_CLASSE','DT_PATRIM_LIQ']	
	dateparse_func = lambda x: convertDate(x) 

	with requests.Session() as s:
		logger.info("start download")
		download_content = s.get(download_url)
		logger.info("finish download")
		logger.info("start reading")
		decoded_content = download_content.content.decode('latin-1')
		parsed_df = pd.read_csv(io.StringIO(decoded_content),delimiter=';', dtype=dtypes, date_parser=dateparse_func, parse_dates=dates_columns)
		logger.info("finish reading")
		return parsed_df
	
	return None	

def renameColumns(fundos_df):
	columns_rename={'TP_FUNDO'	: 'tp_fundo'
			,'CNPJ_FUNDO'		: 'cd_cnpj_fundo'
			,'DENOM_SOCIAL'		: 'nm_denom_social_fundo'
			,'DT_REG'			: 'dt_registro_fundo'
			,'DT_CONST'			: 'dt_constituicao_fundo'
			,'CD_CVM'			: 'cd_cvm'
			,'DT_CANCEL'		: 'dt_cancelamento_fundo'
			,'SIT'				: 'cd_situacao_fundo'
			,'DT_INI_SIT'		: 'dt_inicio_situacao_fundo'
			,'DT_INI_ATIV'		: 'dt_inicio_atividade'
			,'DT_INI_EXERC'		: 'dt_inicio_exec_soc_fundo'
			,'DT_FIM_EXERC'		: 'dt_fim_exec_soc_fundo'
			,'CLASSE'			: 'nm_classe'
			,'DT_INI_CLASSE'	: 'dt_inicio_classe'
			,'RENTAB_FUNDO'		: 'nm_indicador_rentabilidade'
			,'CONDOM'			: 'tp_condominio'
			,'FUNDO_COTAS'		: 'es_fundo_cota'
			,'FUNDO_EXCLUSIVO'	: 'es_fundo_exclusivo'
			,'TRIB_LPRAZO'		: 'es_tributacao_longo_prazo'
			,'INVEST_QUALIF'	: 'es_investidor_qualificado'
			,'ENTID_INVEST'		: 'es_entidade_investimento'
			,'TAXA_PERFM'		: 'vl_taxa_performance' 
			,'INF_TAXA_PERFM'	: 'tx_info_performance'
			,'TAXA_ADM'			: 'vl_taxa_adm'
			,'INF_TAXA_ADM'		: 'tx_info_adm'
			,'VL_PATRIM_LIQ'	: 'vl_patrimonio_liquido'
			,'DT_PATRIM_LIQ'	: 'dt_patrimonio_liquido'
			,'DIRETOR'			: 'nm_diretor'
			,'CNPJ_ADMIN'		: 'cd_cnpj_admin'
			,'ADMIN'			: 'nm_admin'
			,'PF_PJ_GESTOR'		: 'tp_pessoa_gestor'
			,'CPF_CNPJ_GESTOR'	: 'cd_cpf_cnpj_gestor'
			,'GESTOR'			: 'nm_gestor'
			,'CNPJ_AUDITOR'		: 'cd_cnpj_auditor'
			,'AUDITOR'			: 'nm_auditor'
			,'CNPJ_CUSTODIANTE'	: 'cd_cnpj_custodiante'
			,'CUSTODIANTE'		: 'nm_custodiante'
			,'CNPJ_CONTROLADOR'	: 'cd_cnpj_controlador'
			,'CONTROLADOR'		: 'nm_controlador'
			}

	fundos_renamed = fundos_df.rename(columns=columns_rename)
	return fundos_renamed


def saveFundosDatabasePostgres(conteudo):
	logger = logging.getLogger(name="database")
	#con = psycopg2.connect(host='localhost', database='finance',	user='postgres', password='12345')	
	engine = create_engine('postgresql+psycopg2://postgres:12345@localhost:5432/finance')
	#df.head(0).to_sql('table_name', engine, if_exists='replace',index=False)
	conteudo_sql = renameColumns(conteudo)
	tamanho_conteudo = len(conteudo)
	logger.info ("started saving {0} items to database".format(tamanho_conteudo))
	start = datetime.datetime.now()
	conteudo_sql.to_sql(name='tb_cvm_cadastro_fundo_investimento', schema='marketdata', con=engine, if_exists='append', index=False)
	finish = datetime.datetime.now()
	logger.info ("finished saving {0} items to database in {1}".format(tamanho_conteudo,(finish-start)))
	conn = engine.raw_connection()
	conn.commit()	

def saveFundosDatabaseSQLite(conteudo):
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
	df_fundos = downloadFundosFile()		
	if df_fundos is not None:
		saveFundosDatabasePostgres(df_fundos)

def main():
	configureLogger()
	configureDownload()
	#configureDatabase()
	
	downloadAndSave()	

if __name__ == "__main__":
	main()
	