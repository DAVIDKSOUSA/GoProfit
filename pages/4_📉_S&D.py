#Bibliotecas
import pandas as pd
import numpy as np
import yfinance as yf
import warnings
warnings.filterwarnings("ignore")
import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go

#get_ipython().run_line_magic("matplotlib", "inline")

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
#hidebar()

st.sidebar.markdown(f'<h3 style="text-align: center; color:#F63366; font-size:28px;">S&D</h3>',
                    unsafe_allow_html=True)

form = st.sidebar.form(key="annotation")
form.write('Código da Ação')
ticker1 = form.text_input('Insira o código de acordo com o site Yahoo Finance.', value='USDBRL=X')
start_date = form.date_input('Data de Início', value=pd.to_datetime('2020-05-14'))
end_date = form.date_input('Data Final')
#form.write('Benchmark')
#benchmark = form.text_input('Insira o código de acordo com o site Yahoo Finance.', value='QQQ')
#form.write('Período da Análise')
#period = form.text_input('Escreva: ''5y, para 5 anos.',value='10y')
submit = form.form_submit_button("Gerar Dados")
if submit:

    # Get the data

    df1 = yf.download(ticker1, start_date,  end_date)
    df1["Returns"] = df1["Adj Close"].pct_change(1)
    df1["Adj Low"] = df1["Low"] - (df1["Close"] - df1["Adj Close"])
    df1["Adj High"] = df1["High"] - (df1["Close"] - df1["Adj Close"])
    df1["Adj Open"] = df1["Open"] - (df1["Close"] - df1["Adj Close"])
    df1["Target"] = df1["Returns"].shift(-1)
    df1.head()

    # In[3]:

    vol_p1 = 20
    df1["Vol"] = np.round(df1["Returns"].rolling(vol_p1).std() * np.sqrt(252), 4)

    # - Multiplying daily volatility by the square root of 252 gives annualized volatility;
    # - If you divide the annualized volatility by the square root of:
    #  - 12, it gives the monthly volatility
    #  - 52, it gives the weekly volatility

    # # Annual S&D Volatility Zones

    # In[4]:

    # For the Annualized Volatility Chart

    # Restante do código permanece igual


    fig = make_subplots(rows=1, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.08)

    fig.add_trace(go.Scatter(x=df1.index, y=df1["Vol"] * 100
                             , name="Vol", line=dict(color="blue")))

    fig.update_layout(height=800, width=1000
                      , title_text="Annualized Volatility - " + ticker1 + " - www.outspokenmarket.com"
                      , font_color="blue"
                      , title_font_color="black"
                      , xaxis_title="Years"
                      , yaxis_title="Volatility (%)"
                      , legend_title="Vol"
                      , font=dict(size=15, color="Black")
                      , xaxis_rangeslider_visible=True
                      , dragmode='zoom'
                      , hovermode='x'
                      )
    
    fig.update_xaxes(                

                 rangeselector=dict(
                     buttons=list([
                         dict(count=1, label="1m", step="month", stepmode="backward"),
                         dict(count=6, label="6m", step="month", stepmode="backward"),
                         dict(count=1, label="YTD", step="year", stepmode="todate"),
                         dict(count=1, label="1y", step="year", stepmode="backward"),
                         dict(step="all")
                                ])         
                                ),
                tickmode="auto",
                rangemode='normal',
                rangeslider=dict(visible=True, thickness=0.10),
                 )
    fig.update_yaxes(rangemode='normal',
                 type="log",
                 tickmode="auto",
                 autorange=True,  # Definido como False para permitir ajuste manual do intervalo
                )

    

    st.plotly_chart(fig)

    # - A volatility of 15 represents a change, with a 68% probability, of a +-15% movement for the asset in 1 year
    #  - This assumes that the returns are normally distributed, which we know is not the case...
    #  - But it's a close enough approximation.

    # In[5]:




    
    df1["year"] = df1.index.year 

    
    year = "2019"


    df1 = df1[df1['year'] == int(year) +1]


    Upper_Band_12m1d = df1["Vol"][-1] * df1["Adj Close"][-1] + df1["Adj Close"][-1]
    Lower_Band_12m1d = df1["Adj Close"][-1] - df1["Vol"][-1] * df1["Adj Close"][-1]

    Upper_Band_12m2d = 2 * df1["Vol"][-1] * df1["Adj Close"][-1] + df1["Adj Close"][-1]
    Lower_Band_12m2d = df1["Adj Close"][-1] - 2 * df1["Vol"][-1] * df1["Adj Close"][-1]

    # Upper_Band_12m3d = 3 * df1["Vol"][-1] * df1[["Adj Close"][-1] + df1["Adj Close"][-1]

    # Lower_Band_12m4d = df1["Adj Close"][-1] - 4 * df1["Vol"][-1] * df1["Adj Close"][-1]

    # Annual S&D Volatility Zones chart

    fig = make_subplots(rows=1, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.3)

    # fig.add_trace(go.Candlestick(x=df1[str(int(year) + 1)].index
    #                               , open=df1["Open"], high=df1["High"]
    #                              , low=df1["Low"], close=df1["Close"]
    #                             , increasing=dict(line=dict(color='black', width=1), fillcolor='green')
    #                             ,  decreasing=dict(line=dict(color='black', width=1), fillcolor='red')
    #                             ,  hoverlabel=dict(font=dict(color='white'))))
    
    
    fig.add_trace(go.Candlestick(x = df1[str(int(year)+1)].index
                             , open = df1[str(int(year)+1)]["Open"], high = df1[str(int(year)+1)]["High"]
                             , low = df1[str(int(year)+1)]["Low"], close = df1[str(int(year)+1)]["Close"]
                             , decreasing=dict(line=dict(color='black', width=1), fillcolor='red')
                             , increasing=dict(line=dict(color='black', width=1), fillcolor='green'))
             )
    
  

    fig.add_hline(y=Upper_Band_12m1d, line_width=1, line_dash="dash", line_color="green")
    fig.add_hline(y=Lower_Band_12m1d, line_width=1, line_dash="dash", line_color="red")

    fig.add_hline(y=Upper_Band_12m2d, line_width=1, line_dash="dash", line_color="green")
    fig.add_hline(y=Lower_Band_12m2d, line_width=1, line_dash="dash", line_color="red")

    # fig.add_hline(y=Upper_Band_12m3d, line_width=2, line_dash="dash", line_color="green")
    # fig.add_hline(y=Lower_Band_12m4d, line_width=2, line_dash="dash", line_color="red")

    fig.update_layout(height=800, width=1000
                      , title_text="Annual S&D Volatility Zones: " + str(int(year) + 1) + " " + ticker1
                      , font_color="blue"
                      , title_font_color="black"
                      , xaxis_title="Years"
                      , yaxis_title="Close"
                      , legend_title="Vol"
                      , font=dict(size=15, color="Black")
                      , xaxis_rangeslider_visible=True
                      )
    
    
    fig.update_layout(xaxis=dict(fixedrange=False), yaxis=dict(fixedrange=False),
                xaxis_title="Data", 
                yaxis_title="Valor", 
                width=1000, height=800,
                dragmode='zoom',
                hovermode='x')

    fig.update_xaxes(                

                 rangeselector=dict(
                     buttons=list([
                         dict(count=1, label="1m", step="month", stepmode="backward"),
                         dict(count=6, label="6m", step="month", stepmode="backward"),
                         dict(count=1, label="YTD", step="year", stepmode="todate"),
                         dict(count=1, label="1y", step="year", stepmode="backward"),
                         dict(step="all")
                                ])         
                                ),
                tickmode="auto",
                rangemode='normal',
                rangeslider=dict(visible=True, thickness=0.10),
                 )
    
    fig.update_yaxes(rangemode='normal',
                 type="log",
                 tickmode="auto",
                 autorange=True,  # Definido como False para permitir ajuste manual do intervalo
                )

    # Code to exclude empty dates from the chart
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

    # # Weekly S&D Volatility Zones

    # In[6]:

    # Identification of the begining of the week
    # and attribuition of the closing volatility from friday to the next week

    df1["Date"] = df1.index
    df1["WeekDay"] = df1["Date"].dt.dayofweek  # Monday is day 0
    df1 = df1.dropna(axis=0)

    WeeklyVol = df1["Vol"] / np.sqrt(52)
    RefPrice = df1["Adj Close"]
    df1["WeeklyVol"] = df1["Vol"] / np.sqrt(52)
    df1["RefPrice"] = df1["Adj Close"]

    for i in range(1, len(df1)):
        if df1["WeekDay"][i] == 0:
            df1["WeeklyVol"][i] = WeeklyVol[i - 1]
            df1["RefPrice"][i] = RefPrice[i - 1]
        else:
            df1["WeeklyVol"][i] = df1["WeeklyVol"][i - 1]
            df1["RefPrice"][i] = df1["RefPrice"][i - 1]

    # In[7]:

    df1.head(20)

    # In[8]:

    df1["Supply_Band_1d"] = np.round(df1["WeeklyVol"] * df1["RefPrice"] + df1["RefPrice"], 2)
    df1["Demand_Band_1d"] = np.round(df1["RefPrice"] - df1["WeeklyVol"] * df1["RefPrice"], 2)
    df1["Supply_Band_2d"] = np.round(2 * df1["WeeklyVol"] * df1["RefPrice"] + df1["RefPrice"], 2)
    df1["Demand_Band_2d"] = np.round(df1["RefPrice"] - 2 * df1["WeeklyVol"] * df1["RefPrice"], 2)

    # Weekly S&D Volatility Zones chart

    fig = make_subplots(rows=1, cols=1,
                        shared_xaxes=True,
                        vertical_spacing=0.08)

    fig.add_trace(go.Candlestick(x=df1.index
                                 , open=df1["Open"], high=df1["High"]
                                 , low=df1["Low"], close=df1["Close"]
                                 , name="Candle"
                                 , increasing_line_color="green", decreasing_line_color="red")
                  , row=1, col=1
                  )
    fig.add_trace(go.Scatter(x=df1.index, y=df1["Supply_Band_1d"]
                             , name="Supply_Band_1d", line=dict(color="Green", width=1))
                  , row=1, col=1)

    fig.add_trace(go.Scatter(x=df1.index, y=df1["Demand_Band_1d"]
                             , name="Demand_Band_1d", line=dict(color="Red", width=1))
                  , row=1, col=1)

    fig.add_trace(go.Scatter(x=df1.index, y=df1["Supply_Band_2d"]
                             , name="Supply_Band_2d", line=dict(color="Green", width=1, dash="dash"))
                  , row=1, col=1)

    fig.add_trace(go.Scatter(x=df1.index, y=df1["Demand_Band_2d"]
                             , name="Demand_Band_2d", line=dict(color="Red", width=1, dash="dash"))
                  , row=1, col=1)

    fig.update_layout(height=800, width=1000
                      , title_text="Weekly S&D Volatility Zones " + ticker1 + " www.outspokenmarket.com"
                      , font_color="blue"
                      , title_font_color="black"
                      , xaxis_title="Years"
                      , yaxis_title="Adj Close"
                      , legend_title="Indexes"
                      , font=dict(size=15, color="Black")
                      , xaxis_rangeslider_visible=True

                      )

    fig.update_layout(xaxis=dict(fixedrange=False), yaxis=dict(fixedrange=False),
                      xaxis_title="Data", yaxis_title="Valor")
    #fig.update_layout(hovermode="x")

    # Code to exclude empty dates from the chart
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
