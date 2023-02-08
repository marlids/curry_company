 # Libraries
import plotly.express as px
import plotly.graph_objects as go
from haversine import haversine

# bibliotecas necessárias
import folium
import pandas as pd
import numpy  as np
import streamlit as st
from PIL import Image
import re
from streamlit_folium import folium_static

st.set_page_config(page_title= 'Visão Restaurantes', page_icon=None, layout='wide')
# -----------------------------------------------------
# Funções
#======================================================

def distance(df1, fig):
    if fig== False:
        cols = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
        df1['distance'] = (df1.loc[:, cols].apply( lambda x: 
                           haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']), 
                                      ( x['Delivery_location_latitude'], x['Delivery_location_longitude'])), axis=1))
        avg_distance = np.round( df1['distance'].mean(), 2 )
        return avg_distance
    else:
        cols = ['Restaurant_latitude','Restaurant_longitude','Delivery_location_latitude', 'Delivery_location_longitude']
        df1['Distance'] = (df1.loc[:,cols].apply(lambda x : 
                           haversine( (x['Restaurant_latitude'], x['Restaurant_longitude']),
                                      (x['Delivery_location_latitude'], x['Delivery_location_longitude'])),axis = 1 ))
        avg_distance = df1.loc[:,['City','Distance']].groupby('City').mean().reset_index()
        fig = go.Figure( data=[go.Pie(labels=avg_distance['City'],values=avg_distance['Distance'], pull=[0,0.1,0])] )
        return fig

def avg_std_delvery(df1, festival, op):
    """
        Está função calcula o empo médio e o desvio padrão do tempo de entrega.
        Parâmetros:
            Input:
                - df: Dataframe com os dados necessários para o calculo.
                - op: ipo de operação que precisa ser calculado.
                        'avg_time': Calcular o Tempo Médio.
                        'std_time': Calcular o Desvio Padrão do Tempo
                - OutPut:
                    - Dataframe com 2 colunas e uma linha.       
    """
    df_aux = ( df1.loc[:, ['Time_taken(min)', 'Festival']]
                  .groupby( ['Festival'] )
                  .agg( {'Time_taken(min)': ['mean', 'std']} ) )
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    df_aux = np.round( df_aux.loc[df_aux['Festival'] == festival, op], 2 )
    return df_aux

def avg_std_time_grafic(df1):
    df_aux = df1.loc[:,['City', 'Time_taken(min)']].groupby('City').agg( {'Time_taken(min)': ['mean', 'std']} )
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    fig = go.Figure() 
    fig.add_trace( go.Bar( name='Control', x=df_aux['City'], y=df_aux['avg_time'], error_y=dict(type='data', array=df_aux['std_time']))) 
    fig.update_layout(barmode='group') 
    return fig

def avg_std_time_on_traffic(df1):
    df_aux = (df1.loc[:,['City','Road_traffic_density','Time_taken(min)']                ]
                 .groupby(['City','Road_traffic_density'])
                 .agg({'Time_taken(min)':['mean','std']}))
    df_aux.columns =['Time_mean','Time_std']
    df_aux =df_aux.reset_index()
    fig = px.sunburst(df_aux, path=['City', 'Road_traffic_density'], values='Time_mean', color='Time_std',
                  color_continuous_scale='RdBu', color_continuous_midpoint=np.average(df_aux['Time_std']) )
    return fig
            
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
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    
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
st.header( 'Marketplace - Visão Restaurantes' )

image_path = 'Logo.png'
image = Image.open( image_path )
st.sidebar.image( image, width=120 )

st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( """---""" )

st.sidebar.markdown( '## Selecione uma data limite' )

date_slider = st.sidebar.slider( 
    'Até qual valor?',
    value=pd.datetime( 2022, 4, 13 ),
    min_value=pd.datetime(2022, 2, 11 ),
    max_value=pd.datetime( 2022, 4, 6 ),
    format='DD-MM-YYYY' )

st.sidebar.markdown( """---""" )

traffic_options = st.sidebar.multiselect( 
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'], 
    default=['Low', 'Medium', 'High', 'Jam'] )

st.sidebar.markdown( """---""" )
st.sidebar.markdown( '### Powered by Comunidade DS' )

# Filtro de data
linhas_selecionadas = df1['Order_Date'] <  date_slider 
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de transito
linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[linhas_selecionadas, :]

# =======================================
# Layout no Streamlit
# =======================================
tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', '_', '_'] )

with tab1:
    with st.container():
        st.title( "Overal Metrics" )
        
        col1, col2, col3, col4, col5, col6 = st.columns( 6 )
        with col1:
            delivery_unique = len( df1.loc[:, 'Delivery_person_ID'].unique() )
            col1.metric( 'Couriers.', delivery_unique )
                
        with col2:
            # Top Entregadores mais rapidos
            avg_distance = distance(df1, fig=False)
            col2.metric( 'Average distance.', avg_distance )
           
        with col3:
            # Tempo Médio c/Festival
            df_aux = avg_std_delvery(df1, 'Yes','avg_time')
            col3.metric( 'Average Time w/Fest.', df_aux )           

        with col4:
            # STD Entrega c/ Festival
            df_aux = avg_std_delvery(df1, 'Yes','std_time')
            col4.metric( 'STD Delivery w/Fest.', df_aux ) 
     
        with col5:
             # AVG Entrega s/Festival
            df_aux = avg_std_delvery(df1, 'No','avg_time')
            col5.metric( 'Average Time w/o Fest', df_aux )
            
        with col6:
            # STD Entrega s/Festival
            df_aux = avg_std_delvery(df1, 'No','std_time')
            col6.metric( 'STD Delivery w/o Fest.', df_aux )
    
    with st.container():
        st.markdown( """---""" )
        col1, col2 = st.columns( 2 )
        
        with col1:
            #  O tempo médio e o desvio padrão de entrega por cidade
            fig = avg_std_time_grafic(df1)
            st.markdown( "###### Average Delivery Time and STD by City. " )
            st.plotly_chart(fig, theme=None, use_container_width=True)
           
        with col2:
            # Distribuição da Distância
            st.markdown("###### Distance Distribution." )
            df_aux = ( df1.loc[:, ['City', 'Time_taken(min)', 'Type_of_order']]
                          .groupby( ['City', 'Type_of_order'] )
                          .agg( {'Time_taken(min)': ['mean', 'std']} ) )
            df_aux.columns = ['avg_time', 'std_time']
            df_aux = df_aux.reset_index()
            st.dataframe( df_aux )
        
    with st.container():
        st.markdown( """---""" )
        st.title( "Time Distribution." )
        
        col1, col2 = st.columns(2)
        with col1:
            # Distância AVG por Cidade
            fig = distance(df1, fig=True)
            st.markdown('###### Average Distance by City.')
            st.plotly_chart( fig ,theme=None, use_container_width=True)

        with col2:
            # Distância AVG e STD por cidade e Tráfego
            fig = avg_std_time_on_traffic(df1)
            st.markdown('###### Average Distance and STD by City and Traffic.')
            st.plotly_chart( fig ,theme=None, use_container_width=True)
