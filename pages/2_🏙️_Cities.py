# bibliotecas necessárias
import pandas as pd
import numpy   as np
import plotly.express as px
import streamlit as st

# libraries
from PIL import Image

# -----------------------------------------------------
# Funções
#======================================================
def dez_cidades_culinarias_top(df1):
    """ Função para mostrar Top 10 Cidades mais Restaurantes com tipos culinários distintos.
    """
    df_aux = df1.loc[:,['Name country','City','Restaurant ID','Cuisines']
                    ].groupby(['Name country','City']).agg({'Cuisines':['nunique']})
    df_aux.columns =['Quantidade Tipo Culinaria Unicos']
    df_aux = df_aux.sort_values(['Quantidade Tipo Culinaria Unicos'],ascending=False).reset_index()
    df_aux.rename(columns={'Name country': 'Paises','City':'Cidade'}, inplace = True)
    df_aux1 = df_aux.sort_values(['Quantidade Tipo Culinaria Unicos','Cidade'],ascending=[False,True]).reset_index(drop=True).head(10)
    #df_aux1.head(10)
    fig = px.bar( df_aux1, x='Cidade', y='Quantidade Tipo Culinaria Unicos' ,text_auto='.', color ="Paises",width=800,
                 height=500, title="Top 10 Cidades com mais Restaurantes com tipos culinários distintos.")
    return fig

def sete_cidades_abaixo_top(df1):
    """ Função para mostrar Top 7 Cidades com Restaurantes com média de avaliação abaixo de 2.5
    """
    df_aux = (df1.loc[(df1['Aggregate rating']<2.5),['Name country','City','Restaurant ID']]
              .groupby(['Name country','City'])
              .agg({'Restaurant ID':['count','min']}))
    df_aux.columns =['Quantidade Restaurantes','Menor ID']
    df_aux = df_aux.sort_values(['Quantidade Restaurantes'],ascending=False).reset_index()
    df_aux.rename(columns={'Name country': 'Paises','City':'Cidade'}, inplace = True)
    df_aux = df_aux.loc[:,['Paises','Cidade','Quantidade Restaurantes','Menor ID']
                       ].sort_values(['Quantidade Restaurantes'],ascending=False).reset_index()
    df_aux1 = df_aux.sort_values(['Quantidade Restaurantes','Cidade','Paises'],ascending=[False,True,True]).reset_index(drop=True).head(7)
    df_aux1.head(7)
    fig = px.bar( df_aux1, x='Cidade', y='Quantidade Restaurantes' ,text_auto='.2f', color ="Paises", width=800, height=500, 
                 title="7 Top Cidades com Restaurantes com média de avaliação abaixo de 2.5")
    return fig

def sete_cidades_acima_tops(df1):
    """ Função que mostrar as Top 7 Cidades com Restaurantes com média de avaliação acima de 4
    """
    df_aux = df1.loc[(df1['Aggregate rating']>=4),['Name country','City','Restaurant ID']
                    ].groupby(['Name country','City']).agg({'Restaurant ID':['count','min']})

    df_aux.columns =['Quantidade Restaurantes','Menor ID']
    df_aux = df_aux.sort_values(['Quantidade Restaurantes'],ascending=False).reset_index()
    df_aux.rename(columns={'Name country': 'Paises','City':'Cidade'}, inplace = True)
    df_aux = df_aux.loc[:,['Paises','Cidade','Quantidade Restaurantes','Menor ID']
                       ].sort_values(['Quantidade Restaurantes'],ascending=False).reset_index()

    df_aux1 = df_aux.sort_values(['Quantidade Restaurantes','Cidade'],ascending=[False,True]).reset_index(drop=True).head(7)
    fig = px.bar( df_aux1, x='Cidade', y='Quantidade Restaurantes' ,text_auto='.2f', color ="Paises", width=800, height=500, 
                title="7 Top Cidades com Restaurantes com média de avaliação acima de 4")
    return fig

def cidades_top(df1):
    """ Fução que mostrar as 10 Cidades com mais Restaurantes na Base de Dados
    """
    df_aux = df1.loc[:,['Name country','City','Restaurant ID']
                    ].groupby(['Name country','City']).agg({'Restaurant ID':['count']})
    df_aux.columns =['Quantidade Restaurantes']
    df_aux = df_aux.sort_values(['Quantidade Restaurantes'],ascending=False).reset_index()
    df_aux.rename(columns={'Name country': 'Paises','City':'Cidade'}, inplace = True)

    df_aux = df_aux.loc[:,['Paises','Cidade','Quantidade Restaurantes']
                       ].sort_values(['Quantidade Restaurantes'],ascending=False).reset_index()

    df_aux01 = df_aux.loc[(df_aux['Paises'] =='India') & (df_aux['Quantidade Restaurantes'] ==80), :].head(10)
    df_aux02 = df_aux.loc[(df_aux['Paises'] =='Australia'), :].head(10)
    df_aux03 = df_aux.loc[(df_aux['Paises'] =='Brazil'), :].head(10)
    df_aux04 = df_aux.loc[(df_aux['Paises'] =='Canada'), :].sort_values(['Cidade'],ascending=True).head(10)
    df_aux05 = df_aux.loc[(df_aux['Paises'] =='Indonesia'), :].head(10)
    df_aux06 = df_aux.loc[(df_aux['Paises'] =='New Zeland'), :].head(10)
    df_aux07 = df_aux.loc[(df_aux['Paises'] =='Philippines'), :].head(10)
    df_aux08 = df_aux.loc[(df_aux['Paises'] =='Singapure'), :].head(10)
    df_aux09 = df_aux.loc[(df_aux['Paises'] =='South Africa'), :].head(10)
    df_aux10 = df_aux.loc[(df_aux['Paises'] =='Sri Lanka'), :].head(10)
    df_aux11 = df_aux.loc[(df_aux['Paises'] =='Turkey'), :].head(10)
    df_aux12 = df_aux.loc[(df_aux['Paises'] =='United Arab Emirates'), :].head(10)
    df_aux13 = df_aux.loc[(df_aux['Paises'] =='England'), :].head(10)
    df_aux14 = df_aux.loc[(df_aux['Paises'] =='United States of America'), :].head(10)
    df_aux15 = df_aux.loc[(df_aux['Paises'] =='Qatar'), :].head(10)
    df_aux16 = pd.concat([df_aux01, df_aux02, df_aux03, df_aux04, df_aux05, df_aux06, df_aux07, df_aux08, df_aux09, df_aux10, df_aux11, df_aux12, df_aux13, df_aux14, df_aux15]).reset_index(drop=True)
    df_aux17 = df_aux16.sort_values(['Quantidade Restaurantes','Cidade'],ascending=[False,True]).reset_index(drop=True).head(10)

    fig = px.bar( df_aux17, x='Cidade', y='Quantidade Restaurantes' ,text_auto='.2f', color ="Paises",width=800,
                 height=500, title="10 Cidades com mais Restaurantes na Base de Dados")
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

   # linhas_selecionadas = df1['Restaurant ID'] != 18516213
   # df1 = df1.loc[linhas_selecionadas, :]
    
   # linhas_selecionadas = df1['Restaurant ID'] != 16547518
   # df1 = df1.loc[linhas_selecionadas, :]
    
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

st.header("🏙️ Visão Cidades")

# As 10 Cidades com mais Restaurantes na Base de Dados
fig = cidades_top(df1)
st.plotly_chart( fig, user_container_witdh= True )

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        # Top 7 Cidades com Restaurantes com média de avaliação acima de 4'
        fig = sete_cidades_acima_tops(df1)
        st.plotly_chart( fig, use_container_width=True )
    with col2:
        # Top 7 Cidades com Restaurantes com média de avaliação abaixo de 2.5'
        fig = sete_cidades_abaixo_top(df1)
        st.plotly_chart( fig, use_container_width=True )

# As Top 10 Cidades mais Restaurantes com tipos culinários distintos.
fig = dez_cidades_culinarias_top(df1)
st.plotly_chart( fig, user_container_witdh= True )