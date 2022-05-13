#importar bibliotecas
import pandas as pd
import streamlit as st
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
from plotly import graph_objs as go

#chamar pagina
def prophet():

    #sidebar
    # with open("qts/IMG_4341.jpg", "rb") as pdf_file:
    #     PDFbyte = pdf_file.read()

    # st.download_button(label='Baixar Documento',
    #                    data=PDFbyte,
    #                    file_name="IMG_4341.jpg",
    #                    mime='application/octet-stream')

    #dados app sidebar

    #st.subheader('Previsão de Cotações com PROPHET')
    st.sidebar.header('Escolha a Data e o Ativo')
    ticker = st.sidebar.text_input('TICKER - Yahoo Finance', value='USDBRL=X ')
    start_date = st.sidebar.date_input('Data de Início', value=pd.datetime(2018, 1, 1))
    end_date = st.sidebar.date_input('Data Final')

    # mensagem warning
    if start_date >= end_date:
        st.error('DATA FINAL DEVE SER MAIOR QUE A DATA INICIAL !')
    df = yf.download(ticker, start=start_date, end=end_date)

    # st.write(df.info)
    # df = wb.get_data_yahoo(ticker, start = start_date, end = end_date, )
    # df.index = pd.to_datetime(df.index, format = '%Y-%m-d')
    #st.write(df)

    # plotar gráfico
    trace1 = {
        'x': df.index,
        'open': df.Open,
        'close': df.Close,
        'high': df.High,
        'low': df.Low,
        'type': 'candlestick',
        'name': ticker,
        'showlegend': True
    }
    data = [trace1]
    layout = go.Layout()

    # legenda
    layout = go.Layout({
        'title': {
            'text': 'Gráfico de Candlestick - ' + ticker,
            'font': {
                'size': 20
            }
        }
    })

    # instanciar objeto Figure e plotar o gráfico
    fig = go.Figure(data=data, layout=layout)
    st.plotly_chart(fig)
    # st.write(fig.show())

    # tempo de previsão
    n_dias = st.sidebar.slider('Quantidade de dias de previsão', 30, 90)
    df.reset_index(inplace=True)
    # df.Date = pd.Series(pd.to_datetime(df.index, format = '%Y-%m-%d'))

    # df=pd.concat([df, df.Date], axis = 1)

    # df = pd.DataFrame(['Date', 'Adj Close'])

    # st.dataframe(df['Date'])
    df_treino = df[['Date', 'Adj Close']]

    # renomear colunas
    df_treino = df_treino.rename(columns={'Date': 'ds', 'Adj Close': 'y'})

    modelo = Prophet()
    modelo.fit(df_treino)
    futuro = modelo.make_future_dataframe(periods=n_dias, freq='B')
    previsao = modelo.predict(futuro)
    st.write('___')
    st.header('Previsões')
    st.subheader('Legenda:')
    coluns = st.columns(2)
    coluns[0].write('ds - Data')
    coluns[0].write('yhat - Média')
    coluns[1].write('yhat_upper - Banda Superior')
    coluns[1].write('yhat_loewr - Banda Inferior')
    #para mostrar o data frame usar o código abaixo
    st.write(previsao[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(n_dias))

    # grafico1
    grafico1 = plot_plotly(modelo, previsao)
    st.plotly_chart(grafico1)

    # grafico2
    grafico2 = plot_components_plotly(modelo, previsao)
    st.plotly_chart(grafico2)