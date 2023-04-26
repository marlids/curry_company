# libraries
#from haversine import haversine
from streamlit_folium import folium_static
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px

# bibliotecas necessárias
import pandas as pd
import numpy   as np
import streamlit as st
import folium
import haversine
import re

st.set_page_config(page_title= 'Visão Entregadores', page_icon=None, layout='wide')
# -----------------------------------------------------
# Funções
#======================================================

def top_delivery(df1, top_asc):
    """  Está função vai buscar os 10 entregadores mais rápidos ou menos rápidos por cidade.
        top_asc -> True (mas rápido) ou False(menos rápido).
        1. Mostrar os 10 entregadore ['Delivery_person_ID','City','Time_taken(min)']. 
        2. Agrupado por ('City').
        3. Pegar ['Time_taken'] de menor velocidade das cidades ('Metropolitian' ,'Urban' e 'Semi-Urban').
    """         
    
    df2 = (df1.loc[:,['Delivery_person_ID','City','Time_taken(min)'] ]
              .groupby(['City','Delivery_person_ID'] )
              .mean()
              .sort_values(['City','Time_taken(min)'],ascending=top_asc).reset_index())
    df_aux01 = df2.loc[df2['City'] =='Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City'] =='Urban', :].head(10)
    df_aux03 = df2.loc[df2['City'] =='Semi-Urban', :].head(10)
    df3 = pd.concat([df_aux01, df_aux02,df_aux03]).reset_index(drop=True)
    return df3

def clean_code(df1):
    """ Está função tem a responsábilidade de limpar o dataframe
        
        Tipos de limpeza:
        1. Remoçao dos dados Nam.
        2. Mudança de tipos de colunas de dados.
        3. Remoçao de espacos das variaveis de texto
        4. Formatação da colunas de dadta. 
        5. Limpeza da coluna de tempo (remoção do texto da variavel numérica.
        
        Imput: Dataframe
        Output: dataframe 
 
    """
    # 1. Remoçao dos dados Nam.
    linhas_selecionadas = df1['Delivery_person_Age'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = df1['Road_traffic_density'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = df1['Time_taken(min)'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = df1['City'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_selecionadas = df1['Festival'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, :].copy()

    linhas_vazias = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :].copy()

    linhas_vazias = df1['Road_traffic_density'] != 'NaN '
    df1 = df1.loc[linhas_vazias, :].copy()

    # 2. Limpando a coluna Time_taken(min)
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split('(min)') [1])

    # 3. Conversao de texto/categoria/data/string para numeros inteiros
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int ) 
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( int )
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )
    df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format='%d-%m-%Y' ) 

    df1.loc[: , 'ID'] = df1.loc[: , 'ID'].str.strip()
    df1.loc[: , 'Road_traffic_density'] = df1.loc[: , 'Road_traffic_density'].str.strip()
    df1.loc[: , 'Type_of_order'] = df1.loc[: , 'Type_of_order'].str.strip()
    df1.loc[: , 'Type_of_vehicle'] = df1.loc[: , 'Type_of_vehicle'].str.strip()
    df1.loc[: , 'City'] = df1.loc[: , 'City'].str.strip()

    # 4. Adicionando a coluna 'week_of_year' -. Dias da semana
    df1['week_of_year'] = df1['Order_Date'].dt.strftime( "%U" )
    return df1

#======================================================
# Início da Estrutura Lógica do código

# -----------------------------------------------------
# lendo o arquivo importado
#======================================================
df = pd.read_csv( 'dataset/train.csv' )

# -----------------------------------------------------
# Fazendo uma copia do Dataframe
#======================================================
df1 = df.copy()

# -----------------------------------------------------
# Limpando dados
#======================================================
df1 = clean_code(df)

#======================================================
# Barra Lateral
#======================================================
st.header('Markeplace - Visão Entregadores')

image_path = 'Logo.png'
image = Image.open( image_path )
st.sidebar.image( image, width=120 )

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('### Fastest Delivery in Town')
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma data limite')

date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=pd.datetime(2022, 4, 13),
    min_value=pd.datetime(2022, 2, 11),
    max_value=pd.datetime(2022, 4, 6),
    format='DD-MM-YYYY')
    
st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições de transitos',
    ['Low', 'Medium', 'High', 'Jam'],
    default=['Low', 'Medium', 'High', 'Jam'] )
    
st.sidebar.markdown("""---""")    
st.sidebar.markdown('### Powered by comunidade DS')

# Filtro de datas
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas,:]

# Filtro de Transito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas,:]

#======================================================
# Layout no Streamlit
#======================================================

tab1, tab2, tab3 = st.tabs( ['Visão Gerencial' , '_', '_' ] )

with tab1:
    with st.container():    
        st.title(' Overal Metrics' )
        col1, col2,col3,col4 = st.columns(4, gap='Large')
        with col1:
            # Maior idade do entregadores
            maior_idade = df1.loc[ :, 'Delivery_person_Age'].max()
            col1.metric('Major age.', maior_idade)

        with col2:
            # Menor idade do entregadores
            menor_idade = df1.loc[ :, 'Delivery_person_Age'].min()
            col2.metric('Minor age.', menor_idade)
            
        with col3:
            #  Melhor condiçao de veículo
            melhor_condicao = df1.loc[ :, 'Vehicle_condition'].max()
            col3.metric('Best condition.', melhor_condicao)
            
        with col4:
            # Pior condição de veículo
            pior_condicao = df1.loc[ :, 'Vehicle_condition'].min()
            col4.metric('Worst condition.', pior_condicao)
            
    with st.container(): 
        st.markdown("""---""") 
        st.title('Evaluations' )
        col1, col2 = st.columns(2)
        with col1:
            # Avaliações média por Entregador
            st.markdown('###### Average ratings by courier.' )
            avg_retinge_por_delivery = (df1.loc[ :,['Delivery_person_ID','Delivery_person_Age']]
                                    .groupby(['Delivery_person_ID'])
                                     .mean()
                                     .reset_index())
            st.dataframe(avg_retinge_por_delivery)

        with col2:
            st.markdown('###### Average ratings per transit.' )
            dt_avg_std_retinge_by_traffic = (df1.loc[:,['Delivery_person_Ratings','Road_traffic_density']]
                                                .groupby(['Road_traffic_density'])
                                                .agg({'Delivery_person_Ratings':['mean' , 'std']}))
            
            # Mudança do nome da coluna
            dt_avg_std_retinge_by_traffic.columns =['Delivery_mean','Delivery_std']

            # resete index
            dt_avg_std_retinge_by_traffic = dt_avg_std_retinge_by_traffic.reset_index()
            st.dataframe(dt_avg_std_retinge_by_traffic)
   
            st.markdown('###### Average ratings by climate.' )
            dt_avg_retinge_by_weather = (df1.loc[:, ['Delivery_person_Ratings','Weatherconditions']]
                                            .groupby(['Weatherconditions'])
                                            .agg({'Delivery_person_Ratings':['mean' , 'std']}))
            dt_avg_retinge_by_weather.columns =['climate_mean','climate_std']
            dt_avg_retinge_by_weather = dt_avg_retinge_by_weather.reset_index()
            st.dataframe(dt_avg_retinge_by_weather)
    
    with st.container():
        st.markdown("""---""") 
        st.title('Delivery speed.' )
        col1, col2 = st.columns(2)
        
        with col1:
            # Top Entregadores mais lentos
            df3 = top_delivery(df1, top_asc=True)
            st.markdown('###### Top Fastest Deliverers.' )
            st.dataframe(df3)
           
        with col2:
            # Top Entregadores mais lentos
            df3 = top_delivery(df1, top_asc=False)
            st.markdown('###### Top Slowest Deliverers.' )
            st.dataframe(df3)
        