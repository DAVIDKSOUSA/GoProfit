#baixar as bibliotecas
import streamlit as st
from streamlit_option_menu import option_menu

#importar paginas
import paginas.prophet as ph
import paginas.regression as rg
# import paginas.iFat as ifat
import paginas.relatorioperformance as rp
import paginas.suporteresistencia as sr


st.set_page_config(page_title="GoProfit",
                   page_icon='bar-chart',
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={'Get help': None,
                               "Report a Bug": None,
                               "About": None,
                                }
                   )

#navegation bar
pagina = option_menu(
        "GoProfit", ["Prophet", 'Suporte & Resistência', 'Regression'],
        icons=['pin-map', 'cast', 'table'],
    menu_icon="house",
    default_index=0,
    orientation='horizontal'
    # site com icones: https://icons.getbootstrap.com
)

# if pagina == "Relatório Performance":
#     rp.relatorioperformance()
if pagina == "Prophet":
    ph.prophet()
if pagina == 'Suporte & Resistência':
    sr.suporteresistencia()
if pagina == 'Regression':
    rg.regression()

