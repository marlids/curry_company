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

st.set_page_config(page_title= 'Visão Empresa', page_icon=None, layout='wide')
# -----------------------------------------------------
# Funções
#======================================================

def order_metric(df1):
    
    """   Mostrar a quantidade de pedidos por dia.
        1 Selecionar as colunas id e order_date.
        2 Agrupar por dia.
        3 Conte os registros.
        4 Imprima seu resultado.
    """
    colunas = ['ID', 'Order_Date']
    df_aux = df1.loc[:,colunas].groupby( 'Order_Date' ).count().reset_index()
    # Desenhar o gráfico de linhas
    fig = px.bar( df_aux, x='Order_Date', y='ID' )
    return fig

def traffic_order_share(df1):
    
    """   Mostrar a distribuição dos pedidos por tipo de tráfego.
        1 Selecionar as colunas id e Road_traffic_density.
        2 Agrupar por tipo de tráfego.
        3 Conte os registros.
        4 Mostre seu resultado em um grafico de pizza.
    """
    
    df_aux = (df1.loc[:, ['ID', 'Road_traffic_density']]
                 .groupby( 'Road_traffic_density' )
                 .count()
                 .reset_index() )
    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()
    ig = px.pie( df_aux, values='entregas_perc', names='Road_traffic_density' ) 
    return fig

def traffic_order_city(df1):
    
    """   Mostrar a comparação do volume de pedidos por cidade e tipo de tráfego.
        1 Selecionar as colunas id , city e Road_traffic_density.
        2 Agrupar por cidade e tipo de tráfego.
        3 Conte os registros.
        4 Imprima seu resultado em um grafico scatter.
    """
    df_aux = (df1.loc[:, ['ID', 'City','Road_traffic_density']]
                 .groupby (['City','Road_traffic_density' ])
                 .count()
                 .reset_index() )
    fig =px.scatter( df_aux, x='City', y='Road_traffic_density',size='ID', color ='City' )
    return fig

def order_by_week(df1):
    
    """   Mostrar a quantidade de pedidos por semana.
        1 Criar a coluna dia das semanas
        2 Selecionar as colunas week_of_year e order_date.
        3 Agrupar por semana.
        4 Conte os registros.
        5 Imprima seu resultado em um grafico de linha.
    """
    
    df1['week_of_year'] = df1['Order_Date'].dt.strftime( "%U" )
    df_aux = (df1.loc[:, ['ID', 'week_of_year']]
                 .groupby( 'week_of_year' )
                 .count()
                 .reset_index() )
    fig = px.line( df_aux, x='week_of_year', y='ID')
    return fig

def order_share_by_week(df1):
    
    """   Mostrar a quantidade de pedidos únicos por entregador por Semana.
        1 Selecionar as colunas id e week_of_year.
        2 Agrupar por semana.
        3 Conte os registros.
        4 Selecione as coluna delivery_person_ID', 'week_of_year.
        5 Agrupar por semana.
        6 identifique os pedidos únicos.
        7 Divida a quantas entregas na semana pelo Numero de entregadores únicos por semana.
        8 Mostre o resultado em um grafico de linha.
    """
    df_aux1 = (df1.loc[:, ['ID', 'week_of_year']]
                  .groupby( 'week_of_year' )
                  .count()
                  .reset_index())
    df_aux2 = (df1.loc[:, ['Delivery_person_ID', 'week_of_year']]  
                  .groupby( 'week_of_year')
                  .nunique()
                  .reset_index() )
    df_aux = pd.merge( df_aux1, df_aux2, how='inner' )
    df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    fig = px.line( df_aux, x='week_of_year', y='order_by_delivery' )        
    return fig

def country_maps(df1):
    
    """   Mostrar a localização central de cada cidade por tipo de tráfego.
        1 Selecionar as colunas city, road_traffic_density, delivery_location_latitude e delivery_location_longitude
        2 Agrupar por cidade por tipo de tráfego.
        3 Calcular a média dos registros.
        4 Mostre o resultado em um mapa.
    """
    df_aux = (df1.loc[:,['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude'] ]
                 .groupby( ['City','Road_traffic_density'])
                 .median()
                 .reset_index() )
    map = folium.Map( )
    for index,location_info in df_aux.iterrows():  
        folium.Marker( [location_info['Delivery_location_latitude'], 
                        location_info['Delivery_location_longitude']],
                        popup= location_info[['City', 'Road_traffic_density']]).add_to( map )
    folium_static( map, width=1024 , height=600)
        
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
st.header('Markeplace - Visão Cliente')

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

tab1, tab2, tab3 = st.tabs( ['Visão Gerencial' , 'Visão Tática', 'Visão Geografica' ] )

with tab1:
   #  1.0 Visão: Empresa
    with st.container():
        # Order Metric
        fig = order_metric(df1)
        st.markdown('### Order by Day' )
        st.plotly_chart( fig, user_container_witdh= True )
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            # Traffic Order Share
            fig = traffic_order_share(df1)
            st.markdown('### Traffic Order Share')
            st.plotly_chart( fig, theme=None, use_container_width=True )

        with col2:
            # Traffic Order City
            fig = traffic_order_city(df1)
            st.markdown('### Traffic Order City')
            st.plotly_chart( fig, theme=None, use_container_width=True )

with tab2:
    with st.container():
        # Order by Week
        fig = order_by_week(df1)
        st.markdown("# Order by Week" )
        st.plotly_chart( fig, user_container_witdh= True) 
      
    with st.container():
        # Order Share by Week
        fig = order_share_by_week(df1)
        st.markdown("# Order Share by Week" )
        st.plotly_chart( fig, user_container_witdh= True )
        
with tab3:
    # Country Maps
    st.markdown("# Country Maps")
    fig = country_maps(df1)

  