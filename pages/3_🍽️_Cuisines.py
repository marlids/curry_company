# libraries
from folium.plugins import MarkerCluster
from PIL import Image

# bibliotecas necessárias
import pandas as pd
import numpy   as np 
import folium
import streamlit as st
import plotly.express as px

# -----------------------------------------------------
# Funções
#======================================================
def dez_piores_top_tipo_culinarias(df2,qtde):
    """ Está função mostra os Top 10 Piores Tipos de Culinária.
    """
    df_aux = (df2.loc[: ,['Cuisines','Name country','Aggregate rating']].
                  groupby(['Cuisines']).
                  agg({'Aggregate rating':['mean']}))
    df_aux.columns =['Média Avaliação Média']
    df_aux = df_aux.sort_values(['Média Avaliação Média'],ascending=[True]).reset_index()
    df_aux = df_aux.loc[(df_aux['Média Avaliação Média'] > 0) ,['Cuisines','Média Avaliação Média']]
    df_aux.rename(columns={'Cuisines': 'Tipo Culinária'}, inplace = True)
    df_aux = df_aux.reset_index(drop=True).head(qtde)
    fig = px.bar( df_aux, x='Tipo Culinária', y='Média Avaliação Média',text_auto='.2f',
                 height=500, title="Top 10 Piores Tipos de Culinária.")
    fig.update_traces(textfont_size=10, textangle=0, textposition="auto", cliponaxis=False, marker_color='rgb(55, 83, 109)')
    return fig

def dez_melhores_top_tipo_culinarias(df2,qtde):
    """ Está função mostra os Top 10 Melhores Tipos de Culinária.
    """
    df_aux = (df2.loc[:,['Cuisines','Name country','Aggregate rating']]
            .groupby(['Cuisines'])
            .agg({'Aggregate rating':['mean']}))
    df_aux.columns =['Média Avaliação Média']
    df_aux = df_aux.sort_values(['Média Avaliação Média','Cuisines'],ascending=[False,False]).reset_index()
    df_aux.rename(columns={'Cuisines':'Tipo Culinária'}, inplace = True)
    df_aux = df_aux.reset_index(drop=True).head(qtde)
    fig = px.bar( df_aux, x='Tipo Culinária', y='Média Avaliação Média',text_auto='.2f',
                 height=500, title="Top 10 Melhores Tipos de Culinária.")
    fig.update_traces(textfont_size=10, textangle=0, textposition="auto", cliponaxis=False, marker_color='rgb(55, 83, 109)')
    return fig

def dez_top_restaurante(df1,qtde):
    """ Está função mostra os melhores Restaurantes 
    """
    df_aux = df1.loc[:,['Restaurant ID','Restaurant Name','Name country','City','Cuisines','Average Cost for two','Aggregate rating','Votes']
                    ].groupby(['Restaurant ID','Restaurant Name','Name country','City','Cuisines','Average Cost for two','Votes']).agg({'Aggregate rating':['max']})
    df_aux.columns =['aggregate_rating']
    df_aux = df_aux.sort_values(['aggregate_rating','Restaurant ID'],ascending=[False,True]).reset_index()
    df_aux.rename(columns={'Restaurant ID': 'restaurant_id','Restaurant Name': 'restaurant_name','Name country': 'country','Average Cost for two': 'average_cost_for_two'}, inplace = True)
    df_aux01 = df_aux.loc[(df_aux['country'] =='Brazil'), :].sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True]).head(qtde)
    df_aux02 = df_aux.loc[(df_aux['country'] =='England'), :].sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True]).head(qtde)
    df_aux03 = df_aux.loc[(df_aux['country'] =='Qatar'), :].sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True]).head(qtde)
    df_aux04 = df_aux.loc[(df_aux['country'] =='South Africa'), :].sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True]).head(qtde)
    df_aux05 = df_aux.loc[(df_aux['country'] =='Canada'), :].sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True]).head(qtde)
    df_aux06 = df_aux.loc[(df_aux['country'] =='Australia'), :].sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True]).head(qtde)
    df_aux07 = df_aux.loc[(df_aux['country'] =='India') , :].sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True]).head(qtde)
    df_aux08 = df_aux.loc[(df_aux['country'] =='Indonesia'), :].sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True]).head(qtde)
    df_aux09 = df_aux.loc[(df_aux['country'] =='New Zeland'), :].sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True]).head(qtde)
    df_aux10 = df_aux.loc[(df_aux['country'] =='Philippines'), :].sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True]).head(qtde)
    df_aux11 = df_aux.loc[(df_aux['country'] =='Singapure'), :].sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True]).head(qtde)
    df_aux12 = df_aux.loc[(df_aux['country'] =='Sri Lanka'), :].sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True]).head(qtde)
    df_aux13 = df_aux.loc[(df_aux['country'] =='Turkey'), :].sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True]).head(qtde)
    df_aux14 = df_aux.loc[(df_aux['country'] =='United Arab Emirates'), :].sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True]).head(qtde)
    df_aux15 = df_aux.loc[(df_aux['country'] =='United States of America'), :].sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True]).head(qtde)
    df_aux16 = pd.concat([df_aux01, df_aux02, df_aux03, df_aux04, df_aux05, df_aux06, df_aux07, df_aux08, df_aux09, df_aux10, df_aux11, df_aux12, df_aux13, df_aux14, df_aux15]).reset_index(drop=True)
    df_aux16 = df_aux16.sort_values(['aggregate_rating','restaurant_id'],ascending=[False,True]).head(qtde)
    return df_aux16.head(qtde)

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
df2 = df.copy()
# -----------------------------------------------------
# Limpando dados
#======================================================
df1 = clean_code(df)
df2 = clean_code(df)
df4 = clean_code(df)
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
        
st.sidebar.markdown('# Filtros')

country_options = st.sidebar.multiselect(
    'Escolha os Paises que Deseja visualizar os Restaurantes',
    ['India','Australia','Brazil','Canada','Indonesia',
     'New Zeland','Philippines','Qatar','Singapure','South Africa',
     'Sri Lanka','Turkey','United Arab Emirates','England','United States of America',],
    
    default=['Brazil', 'England', 'Qatar', 'South Africa','Canada','Australia',
            ] )

# Filtro de quantidde de Restaurante que deseja visualizar.
qtde = st.sidebar.slider('Selecione a quantidde de Restaurante que deseja visualizar.', 0, 20, 10)

culinaria_options = st.sidebar.multiselect(
    'Escolha os Tipos de Culinárias',
    ['Italian', 'European', 'Filipino', 'American', 'Korean', 'Pizza',
       'Taiwanese', 'Japanese', 'Coffee', 'Chinese', 'Seafood',
       'Singaporean', 'Vietnamese', 'Latin American', 'Healthy Food',
       'Cafe', 'Fast Food', 'Brazilian', 'Argentine', 'Arabian', 'Bakery',
       'Tex-Mex', 'Bar Food', 'International', 'French', 'Steak',
       'German', 'Sushi', 'Grill', 'Peruvian', 'North Eastern',
       'Ice Cream', 'Burger', 'Mexican', 'Vegetarian', 'Contemporary',
       'Desserts', 'Juices', 'Beverages', 'Spanish', 'Thai', 'Indian',
       'Mineira', 'BBQ', 'Mongolian', 'Portuguese', 'Greek', 'Asian',
       'Author', 'Gourmet Fast Food', 'Lebanese', 'Modern Australian',
       'African', 'Coffee and Tea', 'Australian', 'Middle Eastern',
       'Malaysian', 'Tapas', 'New American', 'Pub Food', 'Southern',
       'Diner', 'Donuts', 'Southwestern', 'Sandwich', 'Irish',
       'Mediterranean', 'Cafe Food', 'Korean BBQ', 'Fusion', 'Canadian',
       'Breakfast', 'Cajun', 'New Mexican', 'Belgian', 'Cuban', 'Taco',
       'Caribbean', 'Polish', 'Deli', 'British', 'California', 'Others',
       'Eastern European', 'Creole', 'Ramen', 'Ukrainian', 'Hawaiian',
       'Patisserie', 'Yum Cha', 'Pacific Northwest', 'Tea', 'Moroccan',
       'Burmese', 'Dim Sum', 'Crepes', 'Fish and Chips', 'Russian',
       'Continental', 'South Indian', 'North Indian', 'Salad',
       'Finger Food', 'Mandi', 'Turkish', 'Kerala', 'Pakistani',
       'Biryani', 'Street Food', 'Nepalese', 'Goan', 'Iranian', 'Mughlai',
       'Rajasthani', 'Mithai', 'Maharashtrian', 'Gujarati', 'Rolls',
       'Momos', 'Parsi', 'Modern Indian', 'Andhra', 'Tibetan', 'Kebab',
       'Chettinad', 'Bengali', 'Assamese', 'Naga', 'Hyderabadi', 'Awadhi',
       'Afghan', 'Lucknowi', 'Charcoal Chicken', 'Mangalorean',
       'Egyptian', 'Malwani', 'Armenian', 'Roast Chicken', 'Indonesian',
       'Western', 'Dimsum', 'Sunda', 'Kiwi', 'Asian Fusion', 'Pan Asian',
       'Balti', 'Scottish', 'Cantonese', 'Sri Lankan', 'Khaleeji',
       'South African', 'Drinks Only', 'Durban', 'World Cuisine',
       'Izgara', 'Home-made', 'Giblets', 'Fresh Fish', 'Restaurant Cafe',
       'Kumpir', 'Döner', 'Turkish Pizza', 'Ottoman', 'Old Turkish Bars',
       'Kokoreç'],
    
    default=['Home-made', 'BBQ', 'Japanese', 'Brazilian', 'Arabian', 'American', 'Italian',
            ] )

# Filtro de paises
linhas_selecionadas = df1['Name country'].isin(country_options)
df1 = df1.loc[linhas_selecionadas,:]

linhas_selecionadas = df2['Name country'].isin(country_options)
df2 = df2.loc[linhas_selecionadas,:]

# Filtro de Tipos Culinárias
linhas_selecionadas = df1['Cuisines'].isin(culinaria_options)
df1 = df1.loc[linhas_selecionadas,:]

#======================================================
# Layout no Streamlit
#======================================================
st.header("🍽️ Visão Tipos de Cusinhas")
st.markdown('### Melhores Restaurantes dos Principais tipos Culinários')
with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        df_aux = (df4.loc[(df4['Cuisines']=='Italian'),
           ['Restaurant ID','Name country','City','Cuisines','Restaurant Name','Currency','Average Cost for two','Aggregate rating']]) 
        df_aux = df_aux.sort_values(['Aggregate rating','Restaurant ID'],ascending=[False,True]).reset_index(drop=True)
        prato_dois = f'{df_aux.loc[0, "Average Cost for two"]}'
        culinaria = f'{df_aux.loc[0, "Currency"]}'
        help = f'''
        País: {df_aux.loc[0, "Name country"]}\n
        Cidade: {df_aux.loc[0, "City"]}\n
        Média Prato para dois: {prato_dois} {culinaria}
        ''' 
        col1.metric(label=f'{df_aux.loc[0, "Cuisines"]}:\n {df_aux.loc[0, "Restaurant Name"]}', 
                    value=f'{df_aux.loc[0, "Aggregate rating"]}/5.0', help=help)
    
    with col2:
        df_aux = (df4.loc[(df4['Cuisines']=='American'),
            ['Restaurant ID','Name country','City','Cuisines','Restaurant Name','Currency','Average Cost for two','Aggregate rating']]) 
        df_aux = df_aux.sort_values(['Aggregate rating','Restaurant ID'],ascending=[False,True]).reset_index(drop=True)
        prato_dois = f'{df_aux.loc[0, "Average Cost for two"]}'
        culinaria = f'{df_aux.loc[0, "Currency"]}'
        help = f'''
        País: {df_aux.loc[0, "Name country"]}\n
        Cidade: {df_aux.loc[0, "City"]}\n
        Média Prato para dois: {prato_dois} {culinaria}
        '''
        col2.metric(label=f'{df_aux.loc[0, "Cuisines"]}:\n{df_aux.loc[0, "Restaurant Name"]}', 
                    value=f'{df_aux.loc[0, "Aggregate rating"]}/5.0', help=help)
        
    with col3:
        df_aux = (df4.loc[(df4['Cuisines']=='Arabian'),
            ['Restaurant ID','Name country','City','Cuisines','Restaurant Name','Currency','Average Cost for two','Aggregate rating']])
        df_aux = df_aux.sort_values(['Aggregate rating','Restaurant ID'],ascending=[False,True]).reset_index(drop=True)
        prato_dois = f'{df_aux.loc[0, "Average Cost for two"]}'
        culinaria = f'{df_aux.loc[0, "Currency"]}'
        help = f'''
        País: {df_aux.loc[0, "Name country"]}\n
        Cidade: {df_aux.loc[0, "City"]}\n
        Média Prato para dois: {prato_dois} {culinaria}
        '''
        col3.metric(label=f'{df_aux.loc[0, "Cuisines"]}:\n{df_aux.loc[0, "Restaurant Name"]}', 
                    value=f'{df_aux.loc[0, "Aggregate rating"]}/5.0\n', help=help)
  
    with col4:
        df_aux = (df4.loc[(df4['Cuisines']=='Japanese'),
            ['Restaurant ID','Name country','City','Cuisines','Restaurant Name','Currency','Average Cost for two','Aggregate rating']])
        df_aux = df_aux.sort_values(['Aggregate rating','Restaurant ID'],ascending=[False,True]).reset_index(drop=True)
        prato_dois = f'{df_aux.loc[0, "Average Cost for two"]}'
        culinaria = f'{df_aux.loc[0, "Currency"]}'
        help = f'''
        País: {df_aux.loc[0, "Name country"]}\n
        Cidade: {df_aux.loc[0, "City"]}\n
        Média Prato para dois: {prato_dois} {culinaria}
        '''
        col4.metric(label=f'{df_aux.loc[0, "Cuisines"]}:\n{df_aux.loc[0, "Restaurant Name"]}', 
                    value=f'{df_aux.loc[0, "Aggregate rating"]}/5.0\n', help=help)

    with col5:
        df_aux = (df4.loc[(df4['Cuisines']=='Brazilian'),
            ['Restaurant ID','Name country','City','Cuisines','Restaurant Name','Currency','Average Cost for two','Aggregate rating']])
        df_aux = df_aux.sort_values(['Aggregate rating','Restaurant ID'],ascending=[False,True]).reset_index(drop=True)
        prato_dois = f'{df_aux.loc[0, "Average Cost for two"]}'
        culinaria = f'{df_aux.loc[0, "Currency"]}'
        help = f'''
        País: {df_aux.loc[0, "Name country"]}\n
        Cidade: {df_aux.loc[0, "City"]}\n
        Média Prato para dois: {prato_dois} {culinaria}
        '''
        col5.metric(label=f'{df_aux.loc[0, "Cuisines"]}:\n{df_aux.loc[0, "Restaurant Name"]}', 
                    value=f'{df_aux.loc[0, "Aggregate rating"]}/5.0\n', help=help)

        
st.markdown("# Top 10 Restaurantes" )        
df3 = dez_top_restaurante(df1,qtde)
st.dataframe(df3.head(qtde).style.format(thousands=" "), use_container_width=True)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        #  Top 10 Melhores Tipos de Culinária.
        fig = dez_melhores_top_tipo_culinarias(df2,qtde)
        st.plotly_chart( fig, use_container_width=True )       
    with col2:
        #  Top 10 Piores Tipos de Culinária. 
        fig = dez_piores_top_tipo_culinarias(df2,qtde)
        st.plotly_chart( fig, use_container_width=True ) 
