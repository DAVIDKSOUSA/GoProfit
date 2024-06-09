# Importar bibliotecas necessárias
import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from streamlit_option_menu import option_menu

# Função principal
def regression():
    st.markdown(f'<h3 style="text-align: center; color:#F63366; font-size:28px;">Log-Log Regression</h3>',
                unsafe_allow_html=True)
    
    form = st.form(key="loglog_regression")
    form.subheader('Escolha a Data e o Ativo')
    ticker = form.text_input('TICKER - Yahoo Finance', value='^BVSP', help=
        """
        Para realizar a análise de um ativo deve-se inserir no campo abaixo mesmo código do site Yahoo Finance.
        Caso haja dúvidas em relação ao código a ser utilizado [clique aqui](https://finance.yahoo.com/quote/%5EBVSP/components/) 
        e digite o nome do ativo financeiro na barra de busca do site [Yahoo Finance](https://finance.yahoo.com/quote/%5EBVSP/components/). Exemplo:\n
        - PETR3 digite **PETR3.SA**\n
        - S&P500 digite **SPX**\n
        - Crude Oil Jun22 digite **CL=F**\n
        - Bitcoin digite **BTC-USD**\n"""
    )
    
    start_date = form.date_input('Data de Início', value=pd.to_datetime('2020-01-01'))
    end_date = form.date_input('Data Final', value=pd.to_datetime('2025-12-31'))
    lengths = form.multiselect('Períodos de Regressão (em dias)', options=[800, 300, 120], default=[800, 300, 120])
    dev_mult = form.slider('Multiplicador de Desvio', min_value=0.5, max_value=5.0, value=2.0, step=0.1)

    submit = form.form_submit_button("Gerar Gráfico")
    
    if submit:
        # Baixar dados do Yahoo Finance
        data = yf.download(ticker, start=start_date, end=end_date)
        data = data.dropna(subset=['Close'])
        data['log_price'] = np.log(data['Close'])
        data['log_time'] = np.log(np.arange(1, len(data) + 1))

        def regression(df, length):
            x_array = df['log_time'][-length:].values
            y_array = df['log_price'][-length:].values
            sum_x = np.sum(x_array)
            sum_y = np.sum(y_array)
            sum_xy = np.sum(x_array * y_array)
            sum_x2 = np.sum(x_array**2)
            b = (length * sum_xy - sum_x * sum_y) / (length * sum_x2 - sum_x**2)
            a = (sum_y - b * sum_x) / length
            predictions = a + b * x_array
            slope = (predictions[0] - predictions[-1]) / (x_array[0] - x_array[-1])
            y_mean = np.mean(y_array)
            SS_res = np.sum((predictions - y_array)**2)
            SS_tot = np.sum((y_mean - y_array)**2)
            r_sq = 1 - SS_res / SS_tot
            dev = np.sqrt(SS_res / length)
            return predictions, slope, r_sq, dev

        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(go.Candlestick(x=data.index,
                                     open=data['Open'],
                                     high=data['High'],
                                     low=data['Low'],
                                     close=data['Close'],
                                     name='Candlesticks'))

        colors = ['red', 'green', 'blue']
        for i, length in enumerate(lengths):
            predictions, slope, r_sq, dev = regression(data, length)
            dev_up = np.exp(predictions + dev_mult * dev)
            dev_dn = np.exp(predictions - dev_mult * dev)
            predictions_exp = np.exp(predictions)
            fig.add_trace(go.Scatter(x=data.index[-length:], y=dev_up, mode='lines', name=f'Deviation Up {length} days', line=dict(color=colors[i], dash='dash')))
            fig.add_trace(go.Scatter(x=data.index[-length:], y=dev_dn, mode='lines', name=f'Deviation Down {length} days', line=dict(color=colors[i], dash='dash')))

        fig.update_layout(title=f'Log-Log Regression for {ticker}',
                          xaxis_title='Date',
                          yaxis_title='Price',
                          xaxis_rangeslider_visible=False,
                          showlegend=True)

        dt_all = pd.date_range(start=data.index[0], end=data.index[-1], freq="D")
        dt_all_py = [d.to_pydatetime() for d in dt_all]
        dt_obs_py = [d.to_pydatetime() for d in data.index]
        dt_breaks = [d for d in dt_all_py if d not in dt_obs_py]
        fig.update_xaxes(rangebreaks=[dict(values=dt_breaks)])
        
        st.plotly_chart(fig)

# if __name__ == "__main__":
#     loglog_regression_app()