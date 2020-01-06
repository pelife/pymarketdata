import os
import sys
import logging
import requests
import time
import datetime
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

def configureLogger():
    log_format = "%(levelname)s [%(name)s] %(asctime)s - %(message)s"
    log_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'logs')
    log_fname = os.path.join(log_dir, 'download_carteira.log')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    #logging.basicConfig (filename = log_fname, level = logging.INFO, format = log_format)
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

    create_file = os.path.join(script_dir, '07_b3_carteira_importacao_create.sql')    
    with open(create_file, 'r') as content_file:
        content = content_file.read()
        cursor.execute(content)

    create_file = os.path.join(script_dir, '08_b3_carteira_composicao_create.sql')    
    with open(create_file, 'r') as content_file:
        content = content_file.read()
        cursor.execute(content)

    conn.close()

def download(indice):
    logger = logging.getLogger(name="download")
    logger.info ("start downloading")
    
    colnames =['Codigo','Acao','Tipo','QtdeTeorica','Participacao']

    download_url = "http://bvmf.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice={}&idioma=pt-br".format(indice)
    with requests.Session() as s:
        download_content = s.post(download_url)
        root = BeautifulSoup(download_content.content.decode('utf-8','ignore'), "lxml")        
        tables = root.find_all("table",attrs={"class":"rgMasterTable"})
        data_carteira = root.find_all("li",attrs={"class":"last"})        
        if (len(data_carteira) > 0):
            texto_data = data_carteira[0].text
            texto_data = texto_data[-10:][:8]            
            data = datetime.datetime.strptime(texto_data, '%d/%m/%y')
            logger.info ("data carteira: {}".format(texto_data))
        if (len(tables) > 0):
            logger.info ("carteira: {}".format(indice))
            table = tables[0]
            result = pd.read_html(str(table), thousands='.')
            if (len(result) > 0):                
                result_df = result[0]                
                result_df.columns = colnames                

    logger.info ("finished downloading")
    return {"carteira": result_df, "data": data}
    
def carteiraExiste(codigo_carteira, data_carteira):
    #logger = logging.getLogger(name="database")
    existe = False
    database_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'database')
    database_fname = os.path.join(database_dir, 'dados.db')
    conn = sqlite3.connect(database_fname)
    
    commando = "select a.id_carteira from tb_b3_carteira_importacao a where a.sg_carteira =? and a.dt_inicio=?"    
        
    #logger.info(commando)
    
    cursor = conn.cursor()
    cursor.execute(commando,(codigo_carteira,data_carteira))
    row = cursor.fetchone()
    if (row == None):
        existe = False
    else:
        existe = True   
    
    conn.close()
    return existe

def salvarCarteira (codigo_carteira, data_carteira, composicao_carteira):
    logger = logging.getLogger(name="database")
    
    database_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), 'database')
    database_fname = os.path.join(database_dir, 'dados.db')
    conn = sqlite3.connect(database_fname,detect_types=sqlite3.PARSE_DECLTYPES |
                                           sqlite3.PARSE_COLNAMES)
    
    commando = "insert into tb_b3_carteira_importacao (sg_carteira,dt_inicio) values (?,?)"
        
    #logger.info(commando)
    
    cursor = conn.cursor()
    cursor.execute(commando,(codigo_carteira,data_carteira))
    id_carteira_importacao = cursor.lastrowid 

    composicao_carteira["IdCarteira"] = id_carteira_importacao
    
    commando =  """
                insert into tb_b3_carteira_composicao 
                (
                    cd_acao
                    ,nm_acao
                    ,tp_acao
                    ,qt_acao
                    ,ft_parcipacao
                    ,id_carteira
                )
                values
                (
                    :Codigo
                    ,:Acao
                    ,:Tipo
                    ,:QtdeTeorica
                    ,:Participacao
                    ,:IdCarteira
                )
                """
    
    tamanho_conteudo = len(composicao_carteira)
    logger.info ("started saving {0} items to database".format(tamanho_conteudo))
	
    cursor = conn.cursor()
    # for i in range(1, tamanho_conteudo):
    #     cursor.execute(commando, composicao_carteira[i])
    for index, row in composicao_carteira.iterrows():
        if (index!=tamanho_conteudo-1):
            cursor.execute(commando, row)
    
    conn.commit()
    conn.close()   

def downloadAndSave(codigo_indice):
    resultado = download(codigo_indice)
    if (not carteiraExiste (codigo_indice, resultado["data"])):
        salvarCarteira(codigo_indice, resultado["data"], resultado["carteira"])

def main():
    configureLogger()
    configureDatabase()
    downloadAndSave("IBOV")
    downloadAndSave("IBRX")
    downloadAndSave("IBXL")
    downloadAndSave("SMLL")
    downloadAndSave("IFNC")
    downloadAndSave("ICON")
    downloadAndSave("IFIX")
    downloadAndSave("IMAT")
    downloadAndSave("MLCX")
    downloadAndSave("IDIV")
    downloadAndSave("INDX")
    downloadAndSave("UTIL")
    downloadAndSave("IMOB")
    downloadAndSave("ICO2")
    downloadAndSave("ISEE")

if __name__ == "__main__":
	main()
