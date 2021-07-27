import collections
from glob import glob

import pandas as pd
import plotly.express as px
import streamlit as st


def write():
    @st.cache()
    def get_article_data():
        with st.spinner('Lade Daten...'):
            # Artikeldaten lesen
            df_list = []
            articles = pd.DataFrame()
            for datei in glob("./data/article-*.csv"):
                print(datei)
                df = pd.read_csv(datei, delimiter=";", parse_dates=["date"])
                df_list.append(df)
            articles = pd.concat(df_list)
            articles = articles.set_index("date").sort_index()
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
