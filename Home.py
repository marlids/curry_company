#Librare
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",page_icon=None,
)
#image_path=\Users\Morena\repos_cds\ftc_programacao_phyton\Ciclo07_conceito_etl\aula_53_modularizacao
image_path = 'Logo.png'
image = Image.open( image_path )
st.sidebar.image( image, width=120 )

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('### Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.write("# Cury Company Growth dashboard")
st.markdown(
    """
    Growth dashboard foi contruído para acompanha a métrica de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth dashboard?
    - Visão da Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de géolocalização.
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento.
    - Visão Restaurante:
        - Indicadores semanais de crescimento do restaurante.
    ### Ask for help:
    - Time Data Science no Dicoverd:
        - @megarom
""" )
        
    
    