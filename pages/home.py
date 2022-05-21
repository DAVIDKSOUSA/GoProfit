#importar bibliotecas
import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image
import requests

##animacao
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()
lottie_coding = load_lottieurl('https://assets4.lottiefiles.com/packages/lf20_z6scuqaw.json')

#sidebar
# image = Image.open('images/condor guerreiro colorido.png')
# st.sidebar.image(image)
#esse comando abaixo causo um erro relacioado com a initial page config
# st.sidebar.markdown("<h3 style='text-align: center; color:#F63366; font-size:20px;'><b>GoProfit<b></h3>",
#                     unsafe_allow_html=True)

#chamada da pagina
def home():
    def p_title(title):
        st.markdown(f'<h3 style="text-align: left; color:#F63366; font-size:28px;">{title}</h3>',
                    unsafe_allow_html=True)
    # coluns = st.columns(2)
    # image = Image.open('images/bolacha.png')
    # coluns[0].image(image, width=300)
    # coluns[1].markdown("<h1 style='text-align:center ; color:grey; font-size:20px;'><b>1º/2º GT - Primeiro Esquadrão do Segundo Grupo de Transporte<b></h1>",
    #             unsafe_allow_html=True)
    # coluns[1].markdown("<h1 style='text-align:center ; color:grey; font-size:18px;'><b>Missão<b></h1>",
    #             unsafe_allow_html=True)
    # coluns[1].write('Manter o efetivo preparado para empregar seus meios aéreos com SEGURANÇA, EFICIENCIA e EFICÁCIA.')
    # st.write('---')

    # p_title('AVISOS:')
    # st.text('')
    # st.write(' - Reuniãoto e CONREC - 12/05/22 às 13h30.')

    # image = Image.open('qts/IMG_4341.jpg')
    # st.image(image)

    # st.write('---')

    #st.text('')
    #st.markdown("<h1 style='text-align: center; color:grey; font-size:23px;'><b>Faça uma análise completa da sua "
    #            "carteira de investimentos de forma<b></h1>",
    #            unsafe_allow_html=True)
    #st.markdown("<h3 style='text-align: center; color:grey; font-size:30px;'><b>SIMPLES, OBJETIVA e RÁPIDA!<b></h3>",
    #            unsafe_allow_html=True)
    #st.text('')
    #st.write(
    #    'ALTIVO E GLORIOSO\n'
    #    'VOAMOS COM LOUVOR\n'
    #    'SEGURO E EFICIENTE\n'
    #    'NAS ASAS DO CONDOR.'
    #)
    #st.write('---')
    #st.write(':point_left: Use o menu ao lado e selecione uma funcionalidade.')
    #st.write('---')
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            def p_title(title):
                st.markdown(f'<h3 style="text-align: center; color:#F63366; font-size:28px;">{title}</h3>',
                            unsafe_allow_html=True)
            p_title('GoProfit')
            st.text('')
            st.write('- As informações contidas neste Webapp não constituem\
            recomendação de investimento.\n '
                     '- Qualquer e toda decisão de investimento será de única e exclusiva\
            responsabilidade do usuário.\n'
            '- Os algoritmos coletam os dados da API do Yahoo Finance para a análise e previsão das Séries Temporais.')

            # image = Image.open('qts/IMG_4341.jpg')
            # st.image(image)
            #
            # with open("qts/IMG_4341.jpg", "rb") as pdf_file:
            #     PDFbyte = pdf_file.read()
            #
            # st.download_button(label='Visualizar Documento',
            #                    data=PDFbyte,
            #                    file_name="IMG_4341.jpg",
            #                    mime='application/octet-stream')

            # p_title('AVISOS:')
            # st.write('##')

            st.write('Mídias Sociais:')
            # link para modificação dos logos
            st.markdown(
                """
                [![YouTube Channel Condor](https://img.shields.io/youtube/channel/subscribers/UCHi_qOCcC_KeMu18cOyHtQg?label=GoProfit&style=social)](https://www.youtube.com/channel/UCHi_qOCcC_KeMu18cOyHtQg)
                """
            )
            st.markdown(
                """
                [![Instagram](https://img.shields.io/badge/DAVIDKSOUSA-E4405F?logo=instagram&style=social)](https://www.instagram.com/davidksousa/)
                """
            )
        with right_column:
            st_lottie(lottie_coding, quality='high', height=300, key='coding')

