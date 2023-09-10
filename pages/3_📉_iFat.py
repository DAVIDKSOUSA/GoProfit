# Carregando as bibliotecas
#!pip install yfinance
#!pip install plotly
#!pip install kaleido

import os
from datetime import datetime
import streamlit_option_menu as st
import pandas as pd
import numpy as np
from numpy import mean, absolute
import yfinance as yf
from plotly.subplots import make_subplots
import plotly.graph_objects as go
#import kaleido
import warnings
warnings.filterwarnings("ignore")
import streamlit as st


def hidebar():
    #configuracao de pagina
    st.set_page_config(page_title="Relatório de Performance",
                       page_icon="📝",
                       layout="wide",
                       initial_sidebar_state="expanded",
                       menu_items={"Get Help": None, "Report a Bug": None, "About": None})

    # ocultar o menu
    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """
    st.markdown(hide_menu_style, unsafe_allow_html=True)
hidebar()

st.sidebar.markdown(f'<h3 style="text-align: center; color:#F63366; font-size:28px;">iFAT</h3>',
                    unsafe_allow_html=True)

form = st.sidebar.form(key="annotation")
form.write('Código da Ação')
ticker = form.text_input('Insira o código de acordo com o site Yahoo Finance.', value='USDBRL=X')
start_date = form.date_input('Data de Início', value=pd.to_datetime('2020-05-14'))
end_date = form.date_input('Data Final')
#form.write('Benchmark')
#benchmark = form.text_input('Insira o código de acordo com o site Yahoo Finance.', value='QQQ')
#form.write('Período da Análise')
#period = form.text_input('Escreva: ''5y, para 5 anos.',value='10y')
submit = form.form_submit_button("Gerar Dados")
if submit:
    # Get the data

    # valor da média móvel que iremos trabalhar
    p1 = 252

    df1 = yf.download(ticker, "2019-01-01", "2023-12-31")
    df1["Returns"] = df1["Adj Close"].pct_change(1)
    df1["Adj Low"] = df1["Low"] - (df1["Close"] - df1["Adj Close"])
    df1["Adj High"] = df1["High"] - (df1["Close"] - df1["Adj Close"])
    df1["Adj Open"] = df1["Open"] - (df1["Close"] - df1["Adj Close"])
    df1["Target"] = df1["Returns"].shift(-1)
    df1["MA"] = df1["Adj Close"].rolling(p1).mean()
    # df1 = df1.rename({"Adj Close": "AdjClose"}, axis = 1)
    df1.dropna(axis=0, inplace=True)
    df1.head()


    # Cálculo o MAD
    def mad_calc(data, axis=None):
        return mean(absolute(data - mean(data, axis)), axis)


    # Calcula o STD  MAD - Mean Absolute Deviation
    # aplicar a função apply para fazer um rolling da série

    # utilizamos 60 porque é mais ou menos 1 trimestre

    # sempre utilizar o retorno

    p = 60
    df1["MAD"] = df1["Returns"].rolling(p).apply(mad_calc)
    df1["STD"] = df1["Returns"].rolling(p).std()

    # Calcula o Índice Fat Tail

    df1["iFat"] = (df1["MAD"] / df1["STD"])  # .rolling(10).mean()  #esse roling seria um suavizador do índice

    # a média do fat tail é parecido com a da distribuição normal 0.7970
    # no caso da magazine Luiza não temos uma distribuição normal

    df1["iFat"].describe()

    # minha média menos o desvio padrão do meu iFAT
    # isso vai servir como um suporte para o iFAT
    # df1["iFat"].describe()[1] - df1["iFat"].describe()[2]

    # atribuindo o valor calculado acima a esta variável
    STD1 = df1["iFat"].describe()[1] - df1["iFat"].describe()[2]

    # isso é como criar uma suavização do índice criado, neste caso criamos um suavizador do movimetodo índice gerado acima
    p3 = 60
    df1["MSTD1"] = df1["iFat"].rolling(p3).mean() - df1["iFat"].rolling(
        p3).std()  # este cruzamento é apenas uma forma...
    df1.dropna(axis=0, inplace=True)

    # Analisando o histograma
    # distribuição dos valores do iFat

    fig = go.Figure(data=[go.Histogram(x=df1["iFat"])])

    fig.update_layout(height=600, width=800
                      , title_text="Histograma - iFat - " + ticker
                      , font_color="blue"
                      , title_font_color="black"
                      , xaxis_title="iFat"
                      , yaxis_title="Freq"
                      , font=dict(size=15, color="Black")
                      )

    fig.update_layout(hovermode="x")

    #st.plotly_chart(fig)

    # Gráfico para as zonas de entrada - com base na média móvel
    # linha vermelha zona mócel de 1 desvio para baixo

    fig = make_subplots(rows=2, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.19)

    fig.add_trace(go.Scatter(x=df1.index, y=df1["Adj Close"]
                             , name="Close", line=dict(color="rgb(0,0,150)", width=2))
                  , row=1, col=1)

    fig.add_trace(go.Scatter(x=df1.index
                             , y=np.where(((df1["iFat"] < df1["MSTD1"]) & (df1["iFat"] < 0.75))
                                          # Esse filtro também é uma das muitas formas
                                          # e deve ser ajustado de acordo com a volatilidade...ver GGBR4.SA
                                          # essa segunda condição abaixo de 0.7, foi um parâmetro empírico que o Lenadro
                                          # encontrou, pois quando o uiFat está abaixo desse valor as distribuições se
                                          # assemelham a distribuições bimodais
                                          , df1["Adj Close"]
                                          , None)
                             , name="Close"
                             , line=dict(color="rgb(250,0,0)", width=2))
                  , row=1, col=1)

    fig.add_trace(go.Scatter(x=df1.index
                             , y=np.where(df1["iFat"] >= df1["MSTD1"]
                                          , df1["Adj Close"]
                                          , None)
                             , name="Adj Close"
                             , line=dict(color="rgb(0,0,150)", width=2))
                  , row=1, col=1)

    fig.add_trace(go.Scatter(x=df1.index, y=df1["iFat"]
                             , name="iFat", line=dict(color="blue", width=1))
                  , row=2, col=1)

    fig.add_trace(go.Scatter(x=df1.index, y=df1["MSTD1"]
                             , name="M_STD1", line=dict(color="red", width=1))
                  , row=2, col=1)

    fig.update_layout(height=1000, width=800
                      , title_text="iFat Trimestral - Zonas de Entrada - " + ticker
                      , font_color="blue"
                      , title_font_color="black"
                      , xaxis2_title="Anos"
                      , yaxis_title="Close"
                      , yaxis2_title="iFat"
                      , legend_title="Indexes"
                      , font=dict(size=15, color="Black")
                      , xaxis_rangeslider_visible=True
                      )
    fig.update_layout(hovermode="x")

    # Código para excluir as datas vazias do dataframe
    dt_all = pd.date_range(start=df1.index[0]
                           , end=df1.index[-1]
                           , freq="D")
    dt_all_py = [d.to_pydatetime() for d in dt_all]
    dt_obs_py = [d.to_pydatetime() for d in df1.index]

    dt_breaks = [d for d in dt_all_py if d not in dt_obs_py]

    fig.update_xaxes(
        rangebreaks=[dict(values=dt_breaks)]
    )

    st.plotly_chart(fig)



