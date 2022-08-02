# importar bibliotecas
import pandas as pd
import streamlit as st
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
from plotly import graph_objs as go


# chamar pagina
def prophet_dolar():
    # sidebar
    # with open("qts/IMG_4341.jpg", "rb") as pdf_file:
    #     PDFbyte = pdf_file.read()

    # st.download_button(label='Baixar Documento',
    #                    data=PDFbyte,
    #                    file_name="IMG_4341.jpg",
    #                    mime='application/octet-stream')

    # dados app sidebar

    # st.subheader('Previsão de Cotações com PROPHET')
    st.sidebar.markdown(f'<h3 style="text-align: center; color:#F63366; font-size:28px;">GoProfit</h3>',
                        unsafe_allow_html=True)
    form = st.sidebar.form(key="annotation")
    form.subheader('Escolha a Data e o Ativo')
    ticker = form.text_input('TICKER - Yahoo Finance', value='USDBRL=X', help=
    """
    Para realizar a análise de um ativo deve-se inserir no campo abaixo mesmo código do site Yahoo Finance.
    Caso haja dúvidas em relação ao código a ser utilizado [clique aqui](https://finance.yahoo.com/quote/%5EBVSP/components/) 
    e digite o nome do ativo financeiro na barra de busca do site [Yahoo Finance](https://finance.yahoo.com/quote/%5EBVSP/components/). Exemplo:\n

    - PETR3 digite **PETR3.SA**\n
    - S&P500 digite **SPX**\n
    - Crude Oil Jun22 digite **CL=F**\n

     """)

    expander = form.expander('Códigos')
    expander.write("""
                    **Futures**\n
            ES=F	E-Mini S&P 500 Jun 22\n
            YM=F	Mini Dow Jones Indus.-$5 Jun 22\n
            NQ=F   	Nasdaq 100 Jun 22\n
            RTY=F	E-mini Russell 2000 Index Futur\n
            ZB=F	U.S. Treasury Bond Futures,Jun-\n
            ZN=F	10-Year T-Note Futures,Jun-2022\n
            ZF=F	Five-Year US Treasury Note Futu\n
            ZT=F	2-Year T-Note Futures,Jun-2022\n
            GC=F	Gold\n
            MGC=F	Micro Gold Futures,Aug-2022\n
            SI=F	Silver\n
            SIL=F	Micro Silver Futures,Jul-2022\n
            PL=F	Platinum Jul 22\n
            HG=F	Copper Jul 22\n
            PA=F	Palladium Jun 22\n
            CL=F	Crude Oil\n
            HO=F	Heating Oil Jun 22\n
            NG=F	Natural Gas Jun 22\n
            RB=F	RBOB Gasoline Jun 22\n
            BZ=F	Brent Crude Oil Last Day Financ\n
            B0=F	Mont Belvieu LDH Propane (OPIS)\n
            ZC=F	Corn Futures,Jul-2022\n
            ZO=F	Oat Futures,Jul-2022\n
            KE=F	KC HRW Wheat Futures,Jul-2022\n
            ZR=F	Rough Rice Futures,Jul-2022\n
            ZM=F	Soybean Meal Futures,Jul-2022\n
            ZL=F	Soybean Oil Futures,Jul-2022\n
            ZS=F	Soybean Futures,Jul-2022\n
            GF=F	Feeder Cattle Futures,Aug-2022\n
            HE=F	Lean Hogs Futures,Jun-2022\n
            LE=F	Live Cattle Futures,Jun-2022\n
            CC=F	Cocoa Jul 22\n
            KC=F	Coffee Jul 22\n
            CT=F	Cotton Jul 22\n
            LBS=F	Lumber Jul 22\n
            OJ=F	Orange Juice Jul 22\n
            SB=F	Sugar #11 Jul 22\n
             **World Indices**\n
            ^BVSP	IBOVESPA\n
            ^GSPC	S&P 500\n
            ^DJI	Dow 30\n
            ^IXIC	Nasdaq\n
            ^NYA	NYSE COMPOSITE (DJ)\n
            ^XAX	NYSE AMEX COMPOSITE INDEX\n
            ^RUT	Russell 2000\n
            ^VIX	CBOE Volatility Index\n
            ^FTSE	FTSE 100\n
            ^GDAXI	DAX PERFORMANCE-INDEX\n
            ^FCHI	CAC 40\n
            ^STOXX50E	ESTX 50 PR.EUR\n
            ^N100	Euronext 100 Index\n
            ^BFX	BEL 20\n
             ^N225	Nikkei 225\n
            ^HSI	HANG SENG INDEX\n
            ^STI	STI Index\n
            ^AXJO	S&P/ASX 200\n
            ^AORD	ALL ORDINARIES\n
            ^BSESN	S&P BSE SENSEX\n
            ^JKSE	Jakarta Composite Index\n
            ^KLSE	FTSE Bursa Malaysia KLCI\n
            ^NZ50	S&P/NZX 50 INDEX GROSS\n
            ^KS11	KOSPI Composite Index\n
            ^TWII	TSEC weighted index\n
            ^GSPTSE	S&P/TSX Composite index\n
            ^MXX	IPC MEXICO\n
            ^IPSA	S&P/CLX IPSA\n
            ^MERV	MERVAL\n
            **Cryptocurrencies**\n
            Symbol	Name\n
            BTC-USD	Bitcoin USD\n
            ETH-USD	Ethereum USD\n
            USDT-USD	Tether USD\n
            USDC-USD	USD Coin USD\n
            BNB-USD	Binance Coin USD\n
            XRP-USD	XRP USD\n
            HEX-USD	HEX USD\n
            BUSD-USD	Binance USD USD\n
            ADA-USD	Cardano USD\n
            SOL-USD	Solana USD\n
            DOGE-USD	Dogecoin USD\n
            DOT-USD	Polkadot USD\n
            WBTC-USD	Wrapped Bitcoin USD\n
            AVAX-USD	Avalanche USD\n
            WTRX-USD	Wrapped TRON USD\n
            TRX-USD	TRON USD\n
            STETH-USD	Lido stETH USD\n
            DAI-USD	Dai USD\n
            SHIB-USD	SHIBA INU USD\n
            MATIC-USD	Polygon USD\n
            LTC-USD	Litecoin USD\n
            CRO-USD	Crypto.com Coin USD\n
            LEO-USD	UNUS SED LEO USD\n
            YOUC-USD	yOUcash USD\n
            NEAR-USD	NEAR Protocol USD\n
        """)
    start_date = form.date_input('Data de Início', value=pd.datetime(2020, 5, 14))
    end_date = form.date_input('Data Final')

    # mensagem warning
    if start_date >= end_date:
        st.error('DATA FINAL DEVE SER MAIOR QUE A DATA INICIAL !')
    df = yf.download(ticker, start=start_date, end=end_date)

    # st.write(df.info)
    # df = wb.get_data_yahoo(ticker, start = start_date, end = end_date, )
    # df.index = pd.to_datetime(df.index, format = '%Y-%m-d')
    # st.write(df)

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
    form.subheader('Escolha os parâmetros para a análise')

    n_dias = form.slider('Quantidade de dias de previsão', 30, 90)
    df.reset_index(inplace=True)
    df_treino = df[['Date', 'Close']]

    # renomear colunas
    df_treino = df_treino.rename(columns={'Date': 'ds', 'Close': 'y'})

    # hyperparameters
    seasonality_mode = form.radio(label='Seasonality Mode', options=['additive', 'multiplicative'], index=0,
                                  help="""
                                             Options are **additive**, **multiplicative**. Default is additive, but many business time series will have multiplicative seasonality. This is best identified just from looking at the time series and seeing if the magnitude of seasonal fluctuations grows with the magnitude of the time series.
                                             """)
    seasonality_prior_scale = form.slider(label='Seasonality Prior Scale', min_value=0.01, max_value=10.0, value=10.0,
                                          key='test',
                                          help="""
                                                      This parameter controls the flexibility of the seasonality. Similarly, a large value allows the seasonality to fit large fluctuations, a small value shrinks the magnitude of the seasonality. The default is 10., which applies basically no regularization. That is because we very rarely see overfitting here (there’s inherent regularization with the fact that it is being modeled with a truncated Fourier series, so it’s essentially low-pass filtered). A reasonable range for tuning it would probably be 0.01 - 10; when set to 0.01 you should find that the magnitude of seasonality is forced to be very small. This likely also makes sense on a log scale, since it is effectively an L2 penalty like in ridge regression.
                                                      """)
    changepoint_prior_scale = form.slider(label='Changepoint Prior Scale', min_value=0.001, max_value=0.5, value=0.05,
                                          key='teste1',
                                          help="""
                                                      This is probably the most impactful parameter. It determines the flexibility of the trend, and in particular how much the trend changes at the trend changepoints. As described in this documentation, if it is too small, the trend will be underfit and variance that should have been modeled with trend changes will instead end up being handled with the noise term. If it is too large, the trend will overfit and in the most extreme case you can end up with the trend capturing yearly seasonality. The default of 0.05 works for many time series, but this could be tuned; a range of 0.001 - 0.5 would likely be about right. Parameters like this (regularization penalties; this is effectively a lasso penalty) are often tuned on a log scale.
                                                      """)
    # holidays_prior_scale = form.slider(label='Holidays Prior Scale', min_value=0.01, max_value=10.0, value=10.0,
    #                                                help="""
    #                                                This controls flexibility to fit holiday effects. Similar to seasonality_prior_scale, it defaults to 10.0 which applies basically no regularization, since we usually have multiple observations of holidays and can do a good job of estimating their effects. This could also be tuned on a range of [0.01, 10] as with seasonality_prior_scale.
    #                                                """)

    changepoint_range = form.slider(label='Changepoint Range', min_value=0.1, max_value=1.0, value=0.5,
                                    key='test2',
                                    help="""
                                                      This parameter controls the flexibility of the seasonality. Similarly, a large value allows the seasonality to fit large fluctuations, a small value shrinks the magnitude of the seasonality. The default is 10., which applies basically no regularization. That is because we very rarely see overfitting here (there’s inherent regularization with the fact that it is being modeled with a truncated Fourier series, so it’s essentially low-pass filtered). A reasonable range for tuning it would probably be [0.01, 10]; when set to 0.01 you should find that the magnitude of seasonality is forced to be very small. This likely also makes sense on a log scale, since it is effectively an L2 penalty like in ridge regression.
                                                      """)

    modelo = Prophet(seasonality_mode=seasonality_mode,
                     # holidays_prior_scale=holidays_prior_scale,
                     seasonality_prior_scale=seasonality_prior_scale,
                     changepoint_prior_scale=changepoint_prior_scale,
                     changepoint_range=changepoint_range)
    submit = form.form_submit_button("Gerar Dados")

    if submit:
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
        # para mostrar o data frame usar o código abaixo
        st.write(previsao[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(n_dias))

        # grafico1
        grafico1 = plot_plotly(modelo, previsao)
        st.plotly_chart(grafico1)

        # grafico2
        grafico2 = plot_components_plotly(modelo, previsao)
        st.plotly_chart(grafico2)

