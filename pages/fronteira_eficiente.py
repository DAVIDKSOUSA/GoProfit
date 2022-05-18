#artigo no medium
#https://towardsdatascience.com/efficient-frontier-in-python-detailed-tutorial-84a304f03e79

#importar as bibliotecas
import pandas as pd
import numpy as np
from tqdm import tqdm
import streamlit as st
#import plotly
import plotly.graph_objects as go
#from plotly.subplots import make_subplots
#import plotly.express as px
#import plotly.figure_factory as ff
import yfinance as yf
#import quantstats as qs

def fronteira_eficiente():
    # introducao
    st.subheader('FRONTEIRA EFICIENTE')
    st.markdown("<h5 style='text-align: left; color:grey;'>Teoria moderna do portfólio - Harry Markowitz 1952 </h5>",
                unsafe_allow_html=True)
    st.write(
        'Buscar reduzir o risco de um investimento, obtendo o máximo de Return on Investment (ROI) é o desejo de todo '
        'investidor. Uma maneira de unir esses dois fatores é através da fronteira eficiente.'
    )
    st.markdown("<h5 style='text-align: left; color:grey;'>O que é FRONTEIRA EFICIENTE ?</h5>",
                unsafe_allow_html=True)
    st.write(
        'Fronteira Eficiente é um conceito apresentado por Harry Markowitz. Nele é apresentado que o risco de uma carteira não é' 
        'dado simplesmente pela média dos ativos individuais, mas sim pela diversificação da carteira de investimento como um todo.'
    )
    start = st.sidebar.date_input('Data de Início', value=pd.datetime(2018, 1, 1))
    end = st.sidebar.date_input('Data Final')
    ticker_1 = st.sidebar.text_input('TICKER - Yahoo Finance', value='FB')
    ticker_2 = st.sidebar.text_input('TICKER - Yahoo Finance', value='F')
    ticker_3 = st.sidebar.text_input('TICKER - Yahoo Finance', value='GE')
    ticker_4 = st.sidebar.text_input('TICKER - Yahoo Finance', value='PYPL')
    ticker_5 = st.sidebar.text_input('TICKER - Yahoo Finance', value='QCOM')
    ticker_6 = st.sidebar.text_input('TICKER - Yahoo Finance', value='T')


    ticker = [ticker_1, ticker_2, ticker_3, ticker_4, ticker_5, ticker_6]
    data = yf.download(ticker, start=start, end=end)['Adj Close']
    #data = yf.download(ticker, start=pd.datetime(2015, 1, 1), end=pd.datetime(2022, 1, 1))['Adj Close']
    daily_returns = data.pct_change()
    daily_returns.head()
    #-- Get annualised mean returns
    mus = (1+daily_returns.mean())**252 - 1
    #-- Get covariances
    #- Multiply by 252 to annualise it (square root time for volatility but no square root for variance)
    #- Note: 252 trading days in a year
    #- https://quant.stackexchange.com/questions/4753/annualized-covariance
    cov = daily_returns.cov()*252
    # - How many assests to include in each portfolio
    n_assets = len(ticker)
    # -- How many portfolios to generate
    n_portfolios = 10000

    # -- Initialize empty list to store mean-variance pairs for plotting
    mean_variance_pairs = []

    np.random.seed(75)
    # -- Loop through and generate lots of random portfolios
    for i in range(n_portfolios):
        # - Choose assets randomly without replacement
        assets = np.random.choice(list(daily_returns.columns), n_assets, replace=True)
        # - Choose weights randomly
        weights = np.random.rand(n_assets)
        # - Ensure weights sum to 1
        weights = weights / sum(weights)

        # -- Loop over asset pairs and compute portfolio return and variance
        # - https://quant.stackexchange.com/questions/43442/portfolio-variance-explanation-for-equation-investments-by-zvi-bodie
        portfolio_E_Variance = 0
        portfolio_E_Return = 0
        for i in range(len(assets)):
            portfolio_E_Return += weights[i] * mus.loc[assets[i]]
            for j in range(len(assets)):
                # -- Add variance/covariance for each asset pair
                # - Note that when i==j this adds the variance
                portfolio_E_Variance += weights[i] * weights[j] * cov.loc[assets[i], assets[j]]

        # -- Add the mean/variance pairs to a list for plotting
        mean_variance_pairs.append([portfolio_E_Return, portfolio_E_Variance])

    #-- Plot the risk vs. return of randomly generated portfolios
    #-- Convert the list from before into an array for easy plotting
    mean_variance_pairs = np.array(mean_variance_pairs)
    risk_free_rate=0 #-- Include risk free rate here
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=(mean_variance_pairs[:,1]**0.5*100).round(1), y=(mean_variance_pairs[:,0]*100).round(1),
                          marker=dict(color=(mean_variance_pairs[:,0]-risk_free_rate)/(mean_variance_pairs[:,1]**0.5),
                                      showscale=True,
                                      size=7,
                                      line=dict(width=1),
                                      colorscale="RdBu",
                                      colorbar=dict(title="Sharpe<br>Ratio")
                                     ),
                          mode='markers'))
    fig.update_layout(template='plotly_white',
                      xaxis=dict(title='Risco Anual % (Volatilidade)'),
                      yaxis=dict(title='Retorno Anual %'),
                      title='Possíveis Portifólios',
                      width=850,
                      height=500)
    #fig.update_xaxes(range=[0.1, 0.1])
    #fig.update_yaxes(range=[0.1,0.1])
    fig.update_layout(coloraxis_colorbar=dict(title="Sharpe Ratio"))
    st.plotly_chart(fig)



    #-- Create random portfolio weights and indexes
    #- How many assests in the portfolio
    n_assets = len(ticker)
    mean_variance_pairs = []
    weights_list=[]
    tickers_list=[]

    for i in tqdm(range(12000)):
        next_i = False
        while True:
            #- Choose assets randomly without replacement
            assets = np.random.choice(list(daily_returns.columns), n_assets, replace=True)
            #- Choose weights randomly ensuring they sum to one
            weights = np.random.rand(n_assets)
            weights = weights/sum(weights)
            #-- Loop over asset pairs and compute portfolio return and variance
            portfolio_E_Variance = 0
            portfolio_E_Return = 0
            for i in range(len(assets)):
                portfolio_E_Return += weights[i] * mus.loc[assets[i]]
                for j in range(len(assets)):
                    portfolio_E_Variance += weights[i] * weights[j] * cov.loc[assets[i], assets[j]]
            #-- Skip over dominated portfolios
            for R,V in mean_variance_pairs:
                if (R > portfolio_E_Return) & (V < portfolio_E_Variance):
                    next_i = True
                    break
            if next_i:
                break
            #-- Add the mean/variance pairs to a list for plotting
            mean_variance_pairs.append([portfolio_E_Return, portfolio_E_Variance])
            weights_list.append(weights)
            tickers_list.append(assets)
            break
    # -- Plot the risk vs. return of randomly generated portfolios
    # -- Convert the list from before into an array for easy plotting
    mean_variance_pairs = np.array(mean_variance_pairs)
    risk_free_rate = 0  # -- Include risk free rate here
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=(mean_variance_pairs[:, 1] ** 0.5*100).round(1), y=(mean_variance_pairs[:, 0]*100).round(1),
                             marker=dict(color=(mean_variance_pairs[:, 0] - risk_free_rate) / (
                                         mean_variance_pairs[:, 1] ** 0.5),
                                         showscale=True,
                                         size=10,
                                         line=dict(width=1),
                                         colorscale="RdBu",
                                         colorbar=dict(title="Sharpe<br>Ratio")
                                         ),
                             mode='markers',
                             text=[str(np.array(tickers_list[i])) + "<br>" + str(np.array(weights_list[i]*100).round(0))
                                   for i in range(len(tickers_list))]))
    fig.update_layout(template='plotly_white',
                      xaxis=dict(title='Risco Anualizado % (Volatilidade)'),
                      yaxis=dict(title='Retorno Anual %'),
                      title='Portifólios',
                      width=850,
                      height=500)
    # fig.update_xaxes(range=[0.18, 0.35])
    # fig.update_yaxes(range=[0.05,0.29])
    fig.update_layout(coloraxis_colorbar=dict(title="Sharpe Ratio"))
    st.plotly_chart(fig)