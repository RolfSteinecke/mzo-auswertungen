import streamlit as st
import pandas as pd
import plotly.express as px
import awesome_streamlit as ast
import pickle
import requests
from glob import glob


# Nachricht an slack
def send_slackmessage(logtext):
    # URLs laden
    url = ''
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
    def get_login_data():
        with st.spinner('Lade Daten...'):
            # Login-Daten aus login.pck lesen
            try:
                with open('login.pck', 'rb') as f:
                    df_login = pickle.load(f)
            except Exception as e:
                send_slackmessage('logins_per_day: Login-Daten konnten nicht gelesen werden')
                return pd.DataFrame()

        return df_login

    st.header('Auswertungen aus Anmeldedaten')
    choice = st.selectbox(
        'Auswertung wählen',
        ['Anmeldungen pro Tag']
    )

    if choice == 'Anmeldungen pro Tag':
        df_login = get_login_data()
        df_login_count = df_login.resample("D").count()
        df_login_count.columns = ["Anmeldungen"]
        df_login_count.reset_index(inplace=True)

        fig = px.bar(data_frame=df_login_count, x='date', y='Anmeldungen', title='Anzahl Anmeldungen pro Tag')
        st.write(fig)