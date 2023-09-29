#importar bibliotecas
import quantstats as qs
import streamlit as st
from streamlit_option_menu import option_menu
import datetime
import pandas as pd

def relatorioperformance():
#     #configuracao de pagina
#     st.set_page_config(page_title="Relatório de Performance",
#                        page_icon="📝",
#                        layout="wide",
#                        initial_sidebar_state="expanded",
#                        menu_items={"Get Help": None, "Report a Bug": None, "About": None})

#     # ocultar o menu
#     hide_menu_style = """
#         <style>
#         #MainMenu {visibility: hidden; }
#         footer {visibility: hidden;}
#         </style>
#         """
#     st.markdown(hide_menu_style, unsafe_allow_html=True)
# hidebar()



    qs.extend_pandas()
    st.markdown(f'<h3 style="text-align: center; color:#F63366; font-size:28px;">Relatório de Performance</h3>',
                        unsafe_allow_html=True)
    form = st.form(key="annotation")
    form.write('Código da Ação')
    ticker = form.text_input('Insira o código de acordo com o site Yahoo Finance.', value='VALE')
    form.write('Benchmark')
    benchmark = form.text_input('Insira o código de acordo com o site Yahoo Finance.', value='^BVSP')
    form.write('Período da Análise')
    period = form.text_input('Escreva: '
                                   '5y, para 5 anos.',
                                   value='10y'
                                   )
    submit = form.form_submit_button("Gerar Dados")
    if submit:
        returns = qs.utils.download_returns(ticker, period=period)
        # tentativa de plotagem dos gráficos
        # fig, ax = plt.subplots()
        # sns.heatmap(returns.monthly_returns(), linewidths=1.9, center=0, square=True, annot=True,  vmax=.3, cmap='RdYlGn', fmt='.1f')
        # st.pyplot(fig)
        # gerar as imagens


        returns.plot_monthly_heatmap(savefig='output/monthly_heatmap.png')
        st.image('output/monthly_heatmap.png')
        returns.plot_snapshot(savefig='output/snapshot.png')
        st.image('output/snapshot.png')

        returns.plot_daily_returns(savefig='output/daily_returns.png', benchmark=benchmark)
        st.image('output/daily_returns.png')
        returns.plot_drawdowns_periods(savefig='output/drawdowns_periods.png')
        st.image('output/drawdowns_periods.png')
        # colocar quantia em dinheiro
        returns.plot_earnings(savefig='output/earnings.png')
        st.image('output/earnings.png')
        returns.plot_rolling_volatility(savefig='output/rolling_volatility.png')
        st.image('output/rolling_volatility.png')
        # colocar escolher benchmark
        # returns.plot_rolling_beta(savefig='output/rolling_beta.png', benchmark=benchmark)
        # st.image('output/rolling_beta.png')

        returns.plot_histogram(savefig='output/histogram.png')
        st.image('output/histogram.png')
    
        returns.plot_yearly_returns(savefig='output/yearly_returns.png')
        st.image('output/yearly_returns.png')
        returns.plot_rolling_sharpe(savefig='output/rolling_sharpe.png')
        st.image('output/rolling_sharpe.png')
        returns.plot_rolling_sortino(savefig='output/rolling_sortino.png')
        st.image('output/rolling_sortino.png')
        # Verificar na biblioteca o que é mais conveniente inserir
        # há algumas possibilidades como os plots mode=full ou o relatório HTML gera dados escritos que não há no plot
        # -- https://github.com/ranaroussi/quantstats
        # -- returns.reports.plots(mode='full', benchmark='QQQ', repo)
