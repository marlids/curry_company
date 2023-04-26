# libraries
from streamlit_folium import folium_static
from PIL import Image

# bibliotecas necessárias
import pandas as pd
import numpy   as np 
import plotly.express as px
import streamlit as st

# -----------------------------------------------------
# Funções
#======================================================
def media_prato_para_dois(df1):
    """ Está função mostra a Média de Preço de prato para duas pessoas por País.
    """
    df_aux = df1.loc[:,['Name country','Average Cost for two']
                    ].groupby(['Name country']).agg({'Average Cost for two':['mean']})
    df_aux.columns =['Preço prato para duas Pessoas']
    df_aux = df_aux.sort_values(['Preço prato para duas Pessoas'],ascending=False).reset_index()
    df_aux.rename(columns={'Name country': 'Países'}, inplace = True)

    fig = px.bar( df_aux, x='Países', y='Preço prato para duas Pessoas',text_auto='.4',
                 height=500, title="Média Preço de prato para duas pessoas por País.")
    fig.update_traces(textfont_size=10, textangle=0, textposition="auto", cliponaxis=False, marker_color='rgb(55, 83, 109)')
    return fig

def media_avaliacao(df1):
    """ Está função mostra a Média de Avaliações feita por País.
    """ 
    df_aux = (df1.loc[:,['Name country','Votes']]
              .groupby(['Name country'])
              .agg({'Votes':['mean']}))
    df_aux.columns =['Quantidade Avaliações']
    df_aux = df_aux.sort_values(['Quantidade Avaliações'],ascending=False).reset_index()
    df_aux.rename(columns={'Name country': 'Países'}, inplace = True)

    fig = px.bar( df_aux, x='Países', y='Quantidade Avaliações',text_auto='.2f',
                 height=500, title="Média Avaliações feita por País.")
    fig.update_traces(textfont_size=10, textangle=0, textposition="auto", cliponaxis=False, marker_color='rgb(55, 83, 109)')
    return fig

def quat_cidades_registrados(df1):
    """ Está função mostra a quantidade de cidades registrados por país
        
   """
    df_aux = (df1.loc[:,['Name country','City']]
              .groupby(['Name country'])
              .nunique()
              .sort_values(['City'],ascending=False).reset_index())
    df_aux.rename(columns={'Name country': 'Países','City':'Cidades'}, inplace = True)

    fig = px.bar( df_aux, x='Países', y='Cidades',text_auto='.4',
                 height=500, title="Quantidade de Cidades Registradas por País.")
    fig.update_traces(textfont_size=10, textangle=0, textposition="auto", cliponaxis=False, marker_color='rgb(55, 83, 109)') 
    return fig


def quat_restaurante_registrados(df1):
    """ Está função mostra a quantidade de restaurantes registrados por país
        
   """
    df_aux = df1.loc[:,['Name country','Restaurant ID']
                    ].groupby(['Name country']).agg({'Restaurant ID':['count']})
    df_aux.columns =['Quantidade Restaurantes']
    df_aux = df_aux.sort_values(['Quantidade Restaurantes'],ascending=False).reset_index()
    df_aux.rename(columns={'Name country': 'Países'}, inplace = True)

    fig = px.bar( df_aux, x='Países', y='Quantidade Restaurantes',text_auto='.4',
                 height=500, title="Quantidade de Restaurantes Registrados por País.")
    fig.update_traces(textfont_size=10, textangle=0, textposition="auto", cliponaxis=False, marker_color='rgb(55, 83, 109)')
    return fig

def clean_code(df1):
    """ Está função tem a responsábilidade de limpar o dataframe
        
        Tipos de limpeza:
        1. Remoçao dos dados Nam.
        2. Removendo linhas duplicadas.
        3. Criando a coluna Index
        4. Convertendo objet/string e removendo da coluna "cuisines" os demais tipos de culinária
        5. Descartando coluna com 1 valor único em todas as linhas.
        6. Criando os nomes dos países 
        7. Criando a coluna do Tipo de Categoria de Comida 'Type of Food Category'
        8. Criando a coluna nomes das cores 'Name color'
        
        Imput: Dataframe
        Output: dataframe 
 
    """
    # 1. Remoçao dos dados Nan.
    df1 = df1[df1['Cuisines'].notnull()]

    # 1.1 Apaga todos os Nan do dataframe
    #df1 = sort.drop()

    # 2. Removendo linhas duplicadas
    df1 = df1.drop_duplicates( keep ='first')

    # 3. Criando a coluna Index 
    df1 = df1.reset_index()
    df1 = df1.rename(columns={'index': 'ID'})

    # 4. Convertendo objet/string e removendo da coluna "cuisines" os demais tipos de culinária
    df1["Cuisines"] = df1.loc[:, "Cuisines"].astype(str).apply(lambda x: x.split(',')[0])
    
    # 6. Criando os nomes dos países    
    df1["Name country"] = df1["Country Code"].apply(lambda x:country_name(x))

    # 5. Descartando coluna com 1 valor único em todas as linhas-
    df1 = df1.drop(columns=['Switch to order menu'])

    # 7. Criando a coluna do Tipo de Categoria de Comida 'Type of Food Category'
    df1["Type of Food Category"] = df1["Price range"].apply(lambda x:create_price_tye(x))

    # 8. Criando a coluna nomes das cores 'Name color'
    df1["Name color"] = df1["Rating color"].apply(lambda x:color_name(x))
    return df1

# 6. Criando os nomes dos países
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}
def country_name(country_id):
    """ Está função tem a responsábilidade contém todos os nomes dos países. """
    return COUNTRIES[country_id]

# 7. Criando a coluna do Tipo de Categoria de Comida 'Type of Food Category'
def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

# 8. Criando a coluna nomes das cores 'Name color'
COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}
def color_name(color_code):
    """ Está função tem a responsábilidade contém todos os nomes das cores. """
    return COLORS[color_code]

# 9. Função para renomear colunas'
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df
   
#======================================================
# Início da Estrutura Lógica do código
# -----------------------------------------------------

# lendo o arquivo importado
#======================================================
# lendo o arquivo importado
df = pd.read_csv( 'dataset/zomato.csv' ) 
# -----------------------------------------------------

# Fazendo uma copia do Dataframe
#======================================================
df1 = df.copy()

# -----------------------------------------------------
# Limpando dados
#======================================================
df1 = clean_code(df)
#======================================================
#barrra Lateral
#======================================================
with st.sidebar.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        image_path = 'logo.png'
        image = Image.open( image_path )
        st.image( image, width= 40)
    with col2:
        st.markdown('## Fome Zero')
    with col3:
        st.header('')
        
country_options = st.sidebar.multiselect(
    'Escolha os Paises que Deseja visualizar os Restaurantes',
    ['India','Australia','Brazil','Canada','Indonesia',
     'New Zeland','Philippines','Qatar','Singapure','South Africa',
     'Sri Lanka','Turkey','United Arab Emirates','England','United States of America',],
    
    default=['Brazil', 'England', 'Qatar', 'South Africa','Canada','Australia',
            ] )

# Filtro de paises
linhas_selecionadas = df1['Name country'].isin(country_options)
df1 = df1.loc[linhas_selecionadas,:]

#======================================================
# Layout no Streamlit
#======================================================

st.header("🌎 Visão Países")

# Quantidade de Restaurantes Registrados por País.
fig = quat_restaurante_registrados(df1)
st.plotly_chart( fig, user_container_witdh= True )

# Quantidade de Cidades Registrados por País.
fig = quat_cidades_registrados(df1)
st.plotly_chart( fig, user_container_witdh= True )

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        # Média de Avaliações feita por País.
        fig = media_avaliacao(df1)
        #st.markdown('### Traffic Order Share')
        st.plotly_chart( fig, use_container_width=True )    
    with col2:
        # Média de Preço de prato para duas pessoas por País.
        fig = media_prato_para_dois(df1)
        #st.markdown('### Traffic Order Share')
        st.plotly_chart( fig, use_container_width=True )    
    

