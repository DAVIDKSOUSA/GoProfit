#baixar as bibliotecas
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image

#importar paginas
import pages.prophet as pt
import pages.prophet_dolar as pt_dolar
import pages.relatorio_performance as rp
# import pages.fronteira_eficiente as fe
import pages.home as hm

#configuracao de pagina
#procurar emoji para modificar icone do app page_icon procurara na biblioteca tambem
st.set_page_config(page_title="GoProfit",
                   page_icon='🛩',
                   layout="wide",
                   initial_sidebar_state="auto",
                   menu_items={"Get Help": None, "Report a Bug": None, "About": None,})

#ocultar o menu
# hide_menu_style = """
#     <style>
#     #MainMenu {visibility: hidden; }
#     footer {visibility: hidden;}
#     </style>
#     """
# st.markdown(hide_menu_style, unsafe_allow_html=True)

#pagina com navegation bar
# https://icons.getbootstrap.com - link com icons
pages = option_menu(
    menu_title="GoProfit",
    options=['Home', 'Prophet', 'Relatório Performance', 'Dólar'],
    icons=['pin', 'graph-up-arrow', 'table', 'grip-horizontal','table'],
    menu_icon='house',
    default_index=0,
    orientation='horizontal'
)

#sidebar
# image = Image.open('images/condor guerreiro colorido.png')
# st.sidebar.image(image)
# st.sidebar.write('---')
# st.sidebar.markdown("<h3 style='text-align: center; color:#F63366; font-size:20px;'><b>GoProfit !<b></h3>",
#                 unsafe_allow_html=True)

#chamada de pagina
if pages == "Home":
    hm.home()

if pages == 'Prophet':
    pt.prophet()

if pages == 'Relatório Performance':
    rp.relatorio_performance()

if pages == 'Dólar':
    pt_dolar.prophet_dolar()

# if pages == 'Fronteira Eficiente':
#     fe.fronteira_eficiente()
