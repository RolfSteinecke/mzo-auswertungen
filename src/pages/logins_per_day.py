import streamlit as st
import pandas as pd
import plotly.express as px
import awesome_streamlit as ast
from glob import glob

def write():
    @st.cache()
    def get_login_data():
        with st.spinner('Lade Daten...'):
            # Login-Daten lesen
            df_list = []
            df_login = pd.DataFrame()
            for datei in glob("./data/login-*.csv"):
                print(datei)
                df = pd.read_csv(datei, delimiter=";", parse_dates=["date"])
                df_list.append(df)
            df_login = pd.concat(df_list)
            df_login = df_login.set_index("date").sort_index()
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