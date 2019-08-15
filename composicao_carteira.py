import os
import logging
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def configureLogging():
    log_format = "%(levelname)s [%(name)s] %(asctime)s - %(message)s"
    log_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), "logs")
    log_fname = os.path.join(log_dir, 'carteira.log')

    if (not os.path.exists(log_dir)):
        os.makedirs(log_dir)

    logging.basicConfig(filename=log_fname, level=logging.INFO, format=log_format)


def downloadCarteiraIBOV():
    logging.getLogger(name="ibov")
    logging.info("download started")

    downloadCarteira("http://bvmf.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice=IBOV&idioma=pt-br")
    logging.info("download finished")


def downloadCarteiraIBRX100():
    logging.getLogger(name="ibrx")
    logging.info("download started")

    downloadCarteira("http://bvmf.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice=IBRX&idioma=pt-br")
    logging.info("download finished")


def downloadCarteiraMLCX():
    logging.getLogger(name="mlcx")
    logging.info("download started")

    downloadCarteira("http://bvmf.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice=MLCX&idioma=pt-br")
    logging.info("download finished")


def downloadCarteiraSMLL():
    logging.getLogger(name="smll")
    logging.info("download started")

    downloadCarteira("http://bvmf.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice=SMLL&idioma=pt-br")
    logging.info("download finished")


def downloadCarteiraIDIV():
    logging.getLogger(name="idiv")
    logging.info("download started")

    downloadCarteira("http://bvmf.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice=IDIV&idioma=pt-br")
    logging.info("download finished")


def downloadCarteira(url_download):
    download_url = ""

    driver_dir = os.path.join(os.path.normpath(os.getcwd() + os.sep), "driver")
    driver_fname = os.path.join(driver_dir, 'chromedriver.exe')
    download_url = url_download

    driver = webdriver.Chrome(driver_fname)
    driver.get(download_url)

    soup_level1 = BeautifulSoup(driver.page_source, 'lxml')
    content = soup_level1.find_all('table', attrs={'class': 'rgMasterTable'})

    df = pd.read_html(str(content), header=0)

    driver.close()
    return df


def main():
    print("start")
    configureLogging()
    downloadCarteiraIBOV()
    downloadCarteiraIBRX100()
    downloadCarteiraMLCX()
    downloadCarteiraSMLL()
    downloadCarteiraIDIV()

if __name__ == "__main__":
    main()
