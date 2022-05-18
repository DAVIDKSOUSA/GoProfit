#baixar as bibliotecas
import streamlit as st
from streamlit_option_menu import option_menu

#importar paginas
import pages.prophet as pt
import pages.relatorio_performance as rp
import pages.fronteira_eficiente as fe




#configuracao icone
#colocar outra imagem de icone

#configuracao de pagina
#procurar emoji para modificar icone do app page_icon procurara na biblioteca tambem
st.set_page_config(page_title="GoProfit",
                   page_icon='randon',
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={'Get help': None,
                               "Report a Bug": None,
                               "About": None
                                }
                   )
#ocultar o menu
# hide_menu_style = """
#     <style>
#     #MainMenu {visibility: hidden; }
#     footer {visibility: hidden;}
#     </style>
#     """
# st.markdown(hide_menu_style, unsafe_allow_html=True)

#paginas
st.sidebar.write('---')
st.sidebar.markdown("<h3 style='text-align: center; color:#F63366; font-size:20px;'><b>Bem Vindo ao GoProfit !<b></h3>",
                unsafe_allow_html=True)
# pages = ['Prophet']
# pagina = st.sidebar.selectbox("Selecione uma funcionalidade:", pagina)

#pagina com navegation bar
pages = option_menu(
    menu_title="GoProfit",
    options=['Prophet', 'Relatório Performance', 'Fronteira Eficiente'],
    menu_icon='cast',
    default_index=0,
    orientation='horizontal'
)
if pages == 'Prophet':
    pt.prophet()

if pages == 'Relatório Performance':
    rp.relatorio_performance()

if pages == 'Fronteira Eficiente':
    fe.fronteira_eficiente()
