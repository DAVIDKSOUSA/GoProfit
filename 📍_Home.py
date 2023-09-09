#baixar as bibliotecas
import streamlit as st

#importar paginas
# import pages.prophet as pt
# import pages.relatorio_performance as rp

def hidebar():
    #configuracao de pagina
    st.set_page_config(page_title="GoProfit",
                       page_icon='🛩',
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
hidebar()

#pagina com navegation bar - Transformar o app com Navegation BAr
# from streamlit_option_menu import option_menu
# https://icons.getbootstrap.com - link com icons
# pages = option_menu(menu_title= 'GoProfit',
#                     options=['Prophet', 'Relatório Performance', "iFAt", "S&D"],
#                     icons=['pin', 'graph-up-arrow'],
#                     menu_icon='house',
#                     default_index=0,
#                     orientation='horizontal')