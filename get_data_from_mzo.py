#!/usr/bin/python3
# coding=UTF-8
import argparse
from datetime import date
import logging
import os
import io
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
import configparser

# Datenpfad anlegen
if not os.path.exists('./data/'):
    os.makedirs('./data/')

# Argumente parsen
parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true', help="set debug mode")
args = parser.parse_args()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("get_data_from_mzo.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("")

# Logging mode einstellen
if args.debug:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


# Nachricht an slack
def send_slackmessage(logtext):
    slackmessage = "MZO-Statistikdaten: {}".format(logtext)

    headers = {
        'Content-type': 'application/json',
    }

    data = '{"text": " ' + slackmessage + '"}'
    # Nachricht an monitorin-Channel
    # requests.post('https://hooks.slack.com/services/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', headers=headers, data=data)
    # zum testen PM an Rolf
    requests.post('https://hooks.slack.com/services/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', headers=headers,
                  data=data)

def get_data(url:str, typ:str, monat:str, jahr:int):
    response = requests.get(url, auth=HTTPBasicAuth('aemka', 'aemka'))

    if response.status_code == 200:
        datei = f'./data/{typ}-{jahr}-{monat}.csv'
        with open(datei, 'w') as f:
            f.write(response.content.decode('utf-8'))
        logger.info(f'Daten abgerufen {url} und in {datei} geschrieben')
    else:
        logger.info(f'Daten nicht abrufbar: {url}')
        send_slackmessage(f'Datenabruf fehlgeschlagen {url} - {response.status_code}')


# Nachricht in OSX anzeigen
def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))


if __name__ == '__main__':
    logger.info('Programm gestartet')

    if os.path.isfile('get_data_from_mzo.cnf'):    # aus Datei lesen
        configParser = configparser.RawConfigParser()
        configFilePath = r'get_data_from_mzo.cnf'
        configParser.read(configFilePath)

        url_login_data = configParser.get('main', 'url_login_data')
        url_article_data = configParser.get('main', 'url_article_data')
        user = configParser.get('main', 'user')
        pw = configParser.get('main', 'pw')
    else:
        logger.error('FEHLER: Konfigurationsdatei nicht gefunden!')
        exit(1)

    # aktuelles Jahr und Monat bilden
    jahr = date.today().year
    monat = date.today().month
    tag = date.today().day
    # am ersten Tag eines Monats nochmal Daten des Vormonats abrufen
    if tag == 1:
        if monat == 1:  # Dezember des Vorjahres wählen
            monat = 12
            jahr -= 1
        else:
            monat -= 1

    # Monat muss zweistellig sein
    if monat >= 10:
        monat_str = str(monat)
    else:
        monat_str = f'0{str(monat)}'

    logger.info(f'Datenabruf für {monat_str}-{jahr}')

    # Login-Daten holen
    url = url_login_data.format(monat_str, jahr)
    get_data(url, 'login', monat_str, jahr)

    # Artikel-Daten holen
    url = url_article_data.format(monat_str, jahr)
    df = get_data(url, 'article', monat_str, jahr)


# Calling the function
notify(title    = 'MZO-Statistikdaten',
       subtitle = 'Datenabruf',
       message  = 'Daten von mieterzeitung.de abgerufen')
