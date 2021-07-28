import collections
from glob import glob

import pandas as pd
import plotly.express as px
import streamlit as st
import requests
import pickle


# Nachricht an slack
def send_slackmessage(logtext):
    # URLs laden
    try:
        url = st.secrets['url_rolf']
    except Exception as e:
        print(f'URL konnte nicht geladen werden {e}')

    slackmessage = "MZO-Statistikdaten: {}".format(logtext)

    headers = {
        'Content-type': 'application/json',
    }

    data = '{"text": " ' + slackmessage + '"}'
    # Nachricht an monitorin-Channel
    # requests.post('https://hooks.slack.com/services/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', headers=headers, data=data)
    # zum testen PM an Rolf
    requests.post(url, headers=headers,
                  data=data)

def write():
    def get_article_data():
        with st.spinner('Lade Daten...'):
            try:
                with open('articles.pck', 'rb') as f:
                    articles = pickle.load(f)
            except Exception as e:
                send_slackmessage('logins_per_day: Login-Daten konnten nicht gelesen werden')
                return pd.DataFrame()

        return articles

    st.header('Artikelstatistiken')

    df_articles = get_article_data()

    choice = st.selectbox(
        'Auswertung wählen',
        ['Artikelaufrufe in Ausgabe']
    )

    if choice == 'Artikelaufrufe in Ausgabe':
        # Ausgabe wählen
        editions_unique = df_articles['edition'].unique()
        editions = {}
        for e in editions_unique:
            try:
                m, j = e.split('-')
                editions[f'{j}-{m}'] = e
            except:
                pass

        editions = collections.OrderedDict(sorted(editions.items(), reverse=True))
        edition = st.selectbox('Ausgabe', editions.keys())

        # Nach gewählter Ausgabe filtern
        articles_filterd = df_articles[df_articles['edition'] == editions[edition]]

        fig = px.histogram(data_frame=articles_filterd, x='article',
                           title=f'Aufrufe von Artikeln in Ausgabe {edition}'). \
            update_xaxes(categoryorder='total descending')
        st.write(fig)
