#importar bibliotecas
import streamlit as st
import quantstats as qs

def relatorio_performance():

    qs.extend_pandas()
    st.sidebar.markdown(f'<h3 style="text-align: center; color:#F63366; font-size:28px;">GoProfit</h3>',
                        unsafe_allow_html=True)
    form = st.sidebar.form(key="annotation")
    form.write('Código da Ação')
    ticker = form.text_input('Insira o código de acordo com o site Yahoo Finance.', value='USDBRL=X')
    form.write('Benchmark')
    benchmark = form.text_input('Insira o código de acordo com o site Yahoo Finance.', value='QQQ')
    form.write('Período da Análise')
    period = form.text_input('Escreva: '
                                   '5y, para 5 anos.',
                                   value='10y')
    submit = form.form_submit_button("Gerar Dados")

    if submit:
        returns = qs.utils.download_returns(ticker, period=period)
        returns.plot_monthly_heatmap(savefig='output/monthly_heatmap.png')
        st.image('output/monthly_heatmap.png')
        returns.plot_daily_returns(savefig='output/daily_returns.png')
        st.image('output/daily_returns.png')
        returns.plot_drawdowns_periods(savefig='output/drawdowns_periods.png')
        st.image('output/drawdowns_periods.png')
        returns.plot_earnings(savefig='output/earnings.png')
        st.image('output/earnings.png')
        returns.plot_rolling_volatility(savefig='output/rolling_volatility.png')
        st.image('output/rolling_volatility.png')

        # colocar escolher benchmark
        returns.plot_rolling_beta(savefig='output/rolling_beta.png', benchmark=benchmark)
        st.image('output/rolling_beta.png')
        returns.plot_returns(savefig='output/returns.png', benchmark=benchmark)
        st.image('output/returns.png')
        returns.plot_histogram(savefig='output/histogram.png')
        st.image('output/histogram.png')
        returns.plot_snapshot(savefig='output/snapshot.png')
        st.image('output/snapshot.png')
        returns.plot_yearly_returns(savefig='output/yearly_returns.png')
        st.image('output/yearly_returns.png')
        returns.plot_rolling_sharpe(savefig='output/rolling_sharpe.png')
        st.image('output/rolling_sharpe.png')
        returns.plot_rolling_sortino(savefig='output/rolling_sortino.png')
        st.image('output/rolling_sortino.png')


