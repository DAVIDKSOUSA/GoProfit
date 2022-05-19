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

    #hyperparameters
    seasonality_prior_scale = st.sidebar.number_input(label='Seasonality Prior Scale', min_value=0.01, max_value=10.0, value=10.0,
                                                      key='test',
                                                      help="""
                                                      This parameter controls the flexibility of the seasonality. Similarly, a large value allows the seasonality to fit large fluctuations, a small value shrinks the magnitude of the seasonality. The default is 10., which applies basically no regularization. That is because we very rarely see overfitting here (there’s inherent regularization with the fact that it is being modeled with a truncated Fourier series, so it’s essentially low-pass filtered). A reasonable range for tuning it would probably be [0.01, 10]; when set to 0.01 you should find that the magnitude of seasonality is forced to be very small. This likely also makes sense on a log scale, since it is effectively an L2 penalty like in ridge regression.
                                                      """)
    changepoint_prior_scale = st.sidebar.number_input(label='Changepoint Prior Scale', min_value=0.001, max_value=0.5, value=0.05,
                                                      key='teste1',
                                                      help="""
                                                      This is probably the most impactful parameter. It determines the flexibility of the trend, and in particular how much the trend changes at the trend changepoints. As described in this documentation, if it is too small, the trend will be underfit and variance that should have been modeled with trend changes will instead end up being handled with the noise term. If it is too large, the trend will overfit and in the most extreme case you can end up with the trend capturing yearly seasonality. The default of 0.05 works for many time series, but this could be tuned; a range of [0.001, 0.5] would likely be about right. Parameters like this (regularization penalties; this is effectively a lasso penalty) are often tuned on a log scale.
                                                      """)
    holidays_prior_scale = st.sidebar.number_input(label='Holidays Prior Scale', min_value=0.01, max_value=10.0, value=10.0,
                                                   help="""
                                                   This controls flexibility to fit holiday effects. Similar to seasonality_prior_scale, it defaults to 10.0 which applies basically no regularization, since we usually have multiple observations of holidays and can do a good job of estimating their effects. This could also be tuned on a range of [0.01, 10] as with seasonality_prior_scale.
                                                   """)
    seasonality_mode = st.sidebar.radio(label='Seasonality Mode', options=['additive', 'multiplicative'], index=0,
                                        help="""
                                         Options are ['additive', 'multiplicative']. Default is 'additive', but many business time series will have multiplicative seasonality. This is best identified just from looking at the time series and seeing if the magnitude of seasonal fluctuations grows with the magnitude of the time series (see the documentation here on multiplicative seasonality), but when that isn’t possible, it could be tuned.
                                         """)
    changepoint_range = st.sidebar.number_input(label='Changepoint Range', min_value=0.1, max_value=1.0, value=0.8,
                                                      key='test2',
                                                      help="""
                                                      This parameter controls the flexibility of the seasonality. Similarly, a large value allows the seasonality to fit large fluctuations, a small value shrinks the magnitude of the seasonality. The default is 10., which applies basically no regularization. That is because we very rarely see overfitting here (there’s inherent regularization with the fact that it is being modeled with a truncated Fourier series, so it’s essentially low-pass filtered). A reasonable range for tuning it would probably be [0.01, 10]; when set to 0.01 you should find that the magnitude of seasonality is forced to be very small. This likely also makes sense on a log scale, since it is effectively an L2 penalty like in ridge regression.
                                                      """)

    modelo = Prophet(seasonality_mode=seasonality_mode,
                     holidays_prior_scale=holidays_prior_scale,
                     seasonality_prior_scale=seasonality_prior_scale,
                     changepoint_prior_scale=changepoint_prior_scale,
                     changepoint_range=changepoint_range)
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