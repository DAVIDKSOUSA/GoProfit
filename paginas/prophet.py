# importar bibliotecas
import yfinance as yf
from prophet import *
from prophet.plot import plot_plotly, plot_components_plotly
import streamlit as st
from streamlit_option_menu import option_menu
from plotly import graph_objs as go
import pandas as pd


    




#chamar pagina
def prophet():

    st.markdown(f'<h3 style="text-align: center; color:#F63366; font-size:28px;">Prophet</h3>',
                        unsafe_allow_html=True)
    form = st.form(key="annotation")
    form.subheader('Escolha a Data e o Ativo')
    ticker = form.text_input('TICKER - Yahoo Finance', value='VALE', 
                             help="""
                                        Para realizar a análise de um ativo deve-se inserir no campo abaixo mesmo código do site Yahoo Finance.
                                        Caso haja dúvidas em relação ao código a ser utilizado [clique aqui](https://finance.yahoo.com/quote/%5EBVSP/components/) 
                                        e digite o nome do ativo financeiro na barra de busca do site [Yahoo Finance](https://finance.yahoo.com/quote/%5EBVSP/components/). Exemplo:\n
                                        - PETR3 digite **PETR3.SA**\n
                                        - S&P500 digite **SPX**\n
                                        - Crude Oil Jun22 digite **CL=F**\n
                                        - Bitcoin digite **BTC-USD**\n
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

        """)
    start_date = form.date_input('Data de Início', value=pd.to_datetime('2020-05-14'))
    end_date = form.date_input('Data Final')

    #mensagem de aviso
    if start_date >= end_date:
        st.error('DATA FINAL DEVE SER MAIOR QUE A DATA INICIAL !')
    df = yf.download(ticker, start=start_date, end=end_date)
    df.index = df.index.tz_localize(None)

    #tempo de previsão
    form.subheader('Escolha os parâmetros para a análise')
    n_dias = form.slider('Quantidade de Dias', 30, 120, value=45, help='Escolha a quantidade de dias para a previsão.')
    df.reset_index(inplace=True)
    df_treino = df[['Date', 'Close']]

    # renomear colunas
    df_treino = df_treino.rename(columns={'Date': 'ds', 'Close': 'y'})

    #parâmetros
    #seasonality_mode = form.radio(label='Seasonality Mode', options=['additive', 'multiplicative'], index=0,
    #                               help="""
    #                                     "As opções são **aditivas** e **multiplicativas**. O padrão é aditivo, mas muitas séries \n
    #                                     temporais de negócios terão sazonalidade multiplicativa. Isso é melhor identificado apenas \n
    #                                     ao olhar para a série temporal e verificar se a magnitude das flutuações sazonais cresce com a \n
    #                                     magnitude da série temporal."                                         """)


    #seasonality_prior_scale = form.slider(label='Seasonality Prior Scale', min_value=0.01, max_value=10.0, value=10.0,
    #                                       key='test',
    #                                       help="""
    #                                                   This parameter controls the flexibility of the seasonality. Similarly, a large value allows\n
    #                                                   the seasonality to fit large fluctuations, a small value shrinks the magnitude of the \n
    #                                                   seasonality. The default is 10., which applies basically \nno regularization. That is \n
    #                                                   because we very rarely see overfitting here (there’s inherent regularization with the fact \n
    #                                                   that it is being modeled with a truncated Fourier series, so it’s essentially low-pass filtered).\n
    #                                                   A reasonable range for tuning it would probably be 0.01 - 10; when set to 0.01 you should find that \n
    #                                                   the magnitude of seasonality is forced to be very small. This likely also makes sense on a log scale, \n
    #                                                   since it is effectively an L2 penalty like in ridge regression.
    #                                                   """)
    changepoint_prior_scale = form.slider(label='Flexibilidade na Tendência do Ativo', min_value=0.001, max_value=0.5, value=0.05, key='teste1',
                                          help="""
                                                    Este é provavelmente o parâmetro mais importante. Ele define o quão flexível a linha\n
                                                    de tendência do gráfico será. Se o valor for muito baixo, a linha de tendência não se \n
                                                    ajustará bem aos dados e poderá parecer muito simples. Se o valor for muito alto, \n
                                                    a linha de tendência pode se ajustar demais aos dados, chegando ao ponto de seguir até mesmo \n
                                                    as menores variações, o que não é ideal.

                                                    """)

    # holidays_prior_scale = form.slider(label='Holidays Prior Scale', min_value=0.01, max_value=10.0, value=10.0,
    #                                                help="""
    #                                                This controls flexibility to fit holiday effects. Similar to seasonality_prior_scale, it \n
    #                                                defaults to 10.0 which applies basically no regularization, since we usually have multiple \n
    #                                                observations of holidays and can do a good job of estimating their effects. This could also be \n
    #                                                tuned on a range of [0.01, 10] as with seasonality_prior_scale.
    #                                                """)

    changepoint_range = form.slider(label='Intervalo de Pontos de Mudança', min_value=0.1, max_value=1.0, value= 0.2, key='test2',
                                    help="""
                                                Esse ajuste define o quanto as variações sazonais podem ser flexíveis no modelo. Se você usar um valor grande, \n
                                                o modelo vai se ajustar mais intensamente às grandes mudanças. Se usar um valor pequeno, o modelo \n
                                                vai atenuar essas variações sazonais. 

                                                """)
    modelo = Prophet(#seasonality_mode=seasonality_mode,
                     # holidays_prior_scale=holidays_prior_scale,
                     #seasonality_prior_scale=seasonality_prior_scale,
                     changepoint_prior_scale=changepoint_prior_scale,
                     changepoint_range=changepoint_range)
    submit = form.form_submit_button("Gerar Dados")

    if submit:
        modelo.fit(df_treino)
        futuro = modelo.make_future_dataframe(periods=n_dias, freq='B')
        previsao = modelo.predict(futuro)
    
        #para mostrar o data frame usar o código abaixo

        # grafico1
        st.header('Gráfico com Previsões')
        grafico1 = plot_plotly(modelo, previsao)
        grafico1.update_layout(xaxis=dict(fixedrange=False), yaxis=dict(fixedrange=False),
                               xaxis_title="Data", yaxis_title="Valor")
        st.plotly_chart(grafico1)

        st.header('Tabela com os Valores das Previsões')
        st.subheader('Legenda:')
        coluns = st.columns(2)
        coluns[0].write('ds - **Data**')
        coluns[0].write('yhat - **Média**')
        coluns[1].write('yhat_upper - **Banda Superior**')
        coluns[1].write('yhat_loewr - **Banda Inferior**')
        st.write(previsao[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(n_dias))

        # grafico2
        #verificar as funcoes de componentes na biblioteca prophet
        st.write('___')
        st.header('Componentes do Modelo')
        grafico2 = plot_components_plotly(modelo, previsao)
        grafico2.update_layout(xaxis=dict(fixedrange=False), yaxis=dict(fixedrange=False),
                               xaxis_title="", yaxis_title="")
        st.plotly_chart(grafico2)