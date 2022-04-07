# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import streamlit as st 
import pandas as pd 
import pydeck as pdk 
import plotly.express as px
import plotly.graph_objects as go 
import base64

df = pd.read_csv('bases/NYPD_Shooting_Incident_Data__Historic_.csv')
st.set_page_config(layout='wide') ## codigo para indicar que se desea aprovechar toda la pantalla para visualizar 

st.markdown("<h1 style= 'text-align: center; color:black;'>Historico Disparos en Nueva York 🗽 </h1>", unsafe_allow_html=True) ##  titulo dashboard, el h1 es para el titulo 1
## style tiene varios parametros, el codigo unsafe.... es para que se pueda utilizar los codigos de html, h1 tambien hace referencia el tamañano del titulo 
@st.cache(persist=True)
def load_data(url):
    df = pd.read_csv(url)
    df['OCCUR_DATE']=pd.to_datetime(df['OCCUR_DATE']) ## convertir la columna en formato fecha 
    df['OCCUR_TIME']=pd.to_datetime(df['OCCUR_TIME'],format = '%H:%M:%S') ## convertir columna formato hora, se le debe dar formato para que no se confunda 
    df['YEAR']= df ['OCCUR_DATE'].dt.year ## sacar columna año 
    df['HOUR']= df ['OCCUR_TIME'].dt.hour ## sacar columa hora 
    df['YEARMONTH'] = df['OCCUR_DATE'].dt.strftime('%Y%m') ## para sacar datos mas especificos apartir de las fechas, por ejemplo sacar dia de la semana, en este caso se sacara año,mes
    df.columns=df.columns.map(str.lower)
    
    return df
## funcion para generar un link de descarga del data frame

def get_table_download_link(df):
    csv = df.to_csv(index =False)
    b64 = base64.b64encode(csv.encode()).decode() ## conversion de bite para que se pueda descargar
    href = f'<a href="data:file/csv;base64,{b64}" download="datos.csv">Descargar archivo csv</a>'
    return href
    
df = load_data('bases/NYPD_Shooting_Incident_Data__Historic_.csv')
####--------------------- INDICADORES -----------------------------------------------------------------------------------------------

c1,c2,c3,c4,c5 = st.columns((1,1,1,1,1))
c1.markdown("<h3 style= 'text-align: center; color:#13C9C1;'> Top sexo </h3>", unsafe_allow_html=True)
top_perp_name = df['perp_sex'].value_counts().index[0]
top_perp_num = (round(df['perp_sex'].value_counts()/df['perp_sex'].value_counts().sum(),2)*100)[0]

top_vic_name = df['vic_sex'].value_counts().index[0]
top_vic_num = (round(df['vic_sex'].value_counts()/df['vic_sex'].value_counts().sum(),2)*100)[0]


c1.text('Atacante:'+ str(top_perp_name)+';'+str(top_perp_num)+'%')
c1.text('Victima:'+ str(top_vic_name)+';'+str(top_vic_num)+'%')

                                          #### -

c2.markdown("<h3 style= 'text-align: center; color:#13C9C1;'> Top Raza </h3>", unsafe_allow_html=True)
 
top_perp_name = df['perp_race'].value_counts().index[0]
top_perp_num = (round(df['perp_race'].value_counts()/df['perp_race'].value_counts().sum(),2)*100)[0]

top_vic_name = df['vic_race'].value_counts().index[0]
top_vic_num = (round(df['vic_race'].value_counts()/df['vic_race'].value_counts().sum(),2)*100)[0]
                                
c2.text('Atacante:'+ str(top_perp_name)+';'+str(top_perp_num)+'%')
c2.text('Victima:'+ str(top_vic_name)+';'+str(top_vic_num)+'%')

                                 #############
c3.markdown("<h3 style= 'text-align: center; color:#13C9C1;'> Top Raza </h3>", unsafe_allow_html=True)
        
top_perp_name = df['perp_age_group'].value_counts().index[0]
top_perp_num = (round(df['perp_age_group'].value_counts()/df['perp_race'].value_counts().sum(),2)*100)[0]

top_vic_name = df['vic_age_group'].value_counts().index[0]
top_vic_num = (round(df['vic_age_group'].value_counts()/df['vic_race'].value_counts().sum(),2)*100)[0]
                                       
c3.text('Atacante:'+ str(top_perp_name)+';'+str(top_perp_num)+'%')
c3.text('Victima:'+ str(top_vic_name)+';'+str(top_vic_num)+'%')                          

                                 ###############
c4.markdown("<h3 style= 'text-align: center; color:#13C9C1;'> Top Barrio </h3>", unsafe_allow_html=True)
        
top_perp_name = df['boro'].value_counts().index[0]
top_perp_num = (round(df['boro'].value_counts()/df['perp_race'].value_counts().sum(),2)*100)[0]


c4.text('Nombre:'+ str(top_perp_name)+';'+str(top_perp_num)+'%')
                        
                                                   ########
c5.markdown("<h3 style= 'text-align: center; color:#13C9C1;'> Top Hora </h3>", unsafe_allow_html=True)
        
top_perp_name = df['hour'].value_counts().index[0]
top_perp_num = (round(df['hour'].value_counts()/df['hour'].value_counts().sum(),2)*100)[0]


c5.text('Hora:'+ str(top_perp_name)+';'+str(top_perp_num)+'%')                                                 
                                                   
                                 
                                 
#-----------------------------------------------------------------------------------------------------------------------
c1, c2 = st.columns((1,1)) ## dividir las partes de la hoja el 1,1 es decir que parta la hoja en dos partes iguales 
c1.markdown("<h3 style= 'text-align: center; color:#13C9C1;'> ¿Donde han ocurrido disparos en Nueva York? </h3>", unsafe_allow_html=True)

## para hacer mapa 
year = c1.slider('Ano en el que ocurrio el suceso ',int(df.year.min()),int(df.year.max())) ## sacar la barrita encima del mapa con el año max y año minimo, filtro dinamico 
c1.map(df[df['year']==year][['latitude','longitude']]) ### mapa

## hacer mapa columna 2 
c2.markdown("<h3 style= 'text-align: center; color:#13C9C1;'> ¿A que hora ocurre disparos en nueva york? </h3>", unsafe_allow_html=True)
hour = c2.slider('Hora en la que ocurrio el suceso',int(df.hour.min()),int(df.hour.max()))  
df2 = df[df['hour']==hour]

c2.write(pdk.Deck( ## permite hacer los mapas


         map_style = 'mapbox://styles/mapbox/light-v9', ## estilo del mapa,es clarito
         
         initial_view_state=  {
             'latitude': df['latitude'].mean(),  
             'longitude':df['longitude'].mean(),
             'zoom':9.5, ## tamaño
             'pitch':50},## que tan ladiado este el mapa   

                          ## estad de la  vista inicial,darla la latitud y longitud del lugar de donde queremos graficar  
        ### ahora vamos a poner las capas que quiero en el mapa,la informacion que quiero que me grafique 
        
       ## rango en el que se va a elevar  
       layers = [pdk.Layer(
       'HexagonLayer',
       data = df2[['latitude','longitude']],
       get_position=['longitude','latitude'],  ## como se llama la latitud y longitud dentro de la data
       radius = 100, ## el puntico (el radio)
       extruded = True, ## cuando grafique se eleven las celdas,elevar barritas exagonales 
       elevation_scale = 4,     ## a que escala puede estar elevado 
       elevation_range =[0,1000])]))   

     ## vamos a poner que la persona seleccione una hora y salga los disparos 
##------------------------
st.markdown("<h3 style= 'text-align: center; color:black;'> ¿Como ha sido la evolucion de disparos por barrio en NY ? </h3>", unsafe_allow_html=True)   
df3=df.groupby(['yearmonth','boro'])[['incident_key']].count().reset_index().rename(columns={'incident_key':'disparos'})        

fig=px.line(df3,x='yearmonth', y='disparos',color='boro', width=1250 , height=450)

fig.update_layout(
    title_x=0.5,template = 'simple_white',
    plot_bgcolor='rgba(0,0,0,0)',  ##para que salga blanco el cuadro donde esta la grafica 
    xaxis_title="<b>Año/mes<b>",
    yaxis_title='<b>Cantidad de incidentes<b>',
    legend_title_text='',
    legend=dict(orientation="h",  ## la leyenda es para poner el color de los nombres y modificarlo como quiero, h= horizontal
                yanchor="bottom",    #abajo 
                y=1.02,
                xanchor="right", ## a la derecha
                x=0.8))
st.plotly_chart(fig)
## la grafica anterior muestra la cantidad de incidentes por mes/año por barrio, se nota que el barrio brooklyn es el barrio con mas disparos 
## a partir del año 2020 aumentaron los casos de disparos 

#--------------------------------
c4,c5,c6,c7 = st.columns((1,1,1,1))

## vamos hacer la columna 4 

c4.markdown("<h3 style= 'text-align: center; color:black;'> ¿Que edad tienen los atacantes? </h3>", unsafe_allow_html=True)

df2 = df.groupby(['perp_age_group'])[['incident_key']].count().reset_index().rename(columns={'incident_key':'disparos'})
## se debe modificar la grafica por que la grafica esta pequeña, las categorias estan muy raras, hay que limpiar los datos incoherentes

## vamos agrupar todos los datos en desconocidos 
df2['perp_age_group']=df2['perp_age_group'].replace({'940':'N/A','224':'N/A',
                                                    '1020':'N/A','UNKNOWN':'N/A'})

# orderar los intervalos de edad por orden logico.
df2['perp_age_group2'] = df2['perp_age_group'].replace({'<18':'1',
                                                       '18-24':'2','25-44':'3',
                                                        '45-64':'4','65+':'5','N/A':'6'})
df2.sort_values('perp_age_group2')

fig = px.bar(df2, x ='disparos', y ='perp_age_group', orientation='h', width=340,height=310)
fig.update_layout(
    xaxis_title="<b>Atacante<b>",
    yaxis_title="<b>Edades<b>",
    template = 'simple_white',
   plot_bgcolor='rgba(0,0,0,0)')

c4.plotly_chart(fig)

###------------------------

c5.markdown("<h3 style= 'text-align: center; color:black;'> ¿Que edad tiene las victimas? </h3>", unsafe_allow_html=True)

df2 = df.groupby(['vic_age_group'])[['incident_key']].count().reset_index().rename(columns={'incident_key':'disparos'})
## se debe modificar la grafica por que la grafica esta pequeña, las categorias estan muy raras, hay que limpiar los datos incoherentes

## vamos agrupar todos los datos en desconocidos 
df2['vic_age_group']=df2['vic_age_group'].replace({'940':'N/A','224':'N/A',
                                                    '1020':'N/A','UNKNOWN':'N/A'})

# orderar los intervalos de edad por orden logico.
df2['vic_age_group2'] = df2['vic_age_group'].replace({'<18':'1',
                                                       '18-24':'2','25-44':'3',
                                                        '45-64':'4','65+':'5','N/A':'6'})
df2.sort_values('vic_age_group2')

fig = px.bar(df2, x ='disparos', y ='vic_age_group', orientation='h', width=340,height=310)
fig.update_layout(
    xaxis_title="<b>Atacante<b>",
   yaxis_title="<b>Edades<b>",
    template = 'simple_white',
   plot_bgcolor='rgba(0,0,0,0)')
c5.plotly_chart(fig)

##--------------

c6.markdown("<h3 style= 'text-align: center; color:black;'> ¿Cual es el sexo del atacante ? </h3>", unsafe_allow_html=True)

df2 = df.groupby(['perp_sex'])[['incident_key']].count().reset_index().sort_values('incident_key')


fig = px.pie(df2,values='incident_key',names='perp_sex', width=300, height=300)

## Editar grafica 
fig.update_layout(
    title_x=0.5,
    plot_bgcolor='rgba(0,0,0,0)',##para que salga blanco el cuadro donde esta la grafica 
    template = 'simple_white',
    legend_title_text='',
    
    legend=dict(orientation="h",  ## la leyenda es para poner el color de los nombres y modificarlo como quiero, h= horizontal
                yanchor="bottom",    #abajo 
                y=-0.4,
                xanchor="center", ## a la derecha
                x=0.5))
c6.plotly_chart(fig)

####----------------------------------
c7.markdown("<h3 style= 'text-align: center; color:black;'> ¿Cual es el sexo del victima ? </h3>", unsafe_allow_html=True)

df2 = df.groupby(['vic_sex'])[['incident_key']].count().reset_index().sort_values('incident_key')


fig = px.pie(df2,values='incident_key',names='vic_sex', width=300, height=300)

## Editar grafica 
fig.update_layout(
    title_x=0.5,
    plot_bgcolor='rgba(0,0,0,0)',##para que salga blanco el cuadro donde esta la grafica 
    template = 'simple_white',
    legend_title_text='',
    
    legend=dict(orientation="h",  ## la leyenda es para poner el color de los nombres y modificarlo como quiero, h= horizontal
                yanchor="bottom",    #abajo 
                y=-0.4,
                xanchor="center", ## a la derecha
                x=0.5))
c7.plotly_chart(fig)

####----------------------------------
st.markdown("<h3 style= 'text-align: center; color:black;'> ¿Evolucion de disparos por año ? </h3>", unsafe_allow_html=True)
df2 = df[df['hour'].isin([23,9])].groupby(['year','hour'])[['incident_key']].count().reset_index()
df2['hour']=df2['hour'].astype('category')
fig = px.bar(df2, x ='year', y ='incident_key', color ='hour', barmode='group', width =1150, height=450)

fig.update_layout(
    title_x=0.5,
    plot_bgcolor='rgba(0,0,0,0)',##para que salga blanco el cuadro donde esta la grafica 
    xaxis_title="<b>Año<b>",
    yaxis_title="<b>Cantidad de disparos<b>",
    template = 'simple_white',
    legend_title_text='<b> Hora<b>')
    
st.plotly_chart(fig)

if st.checkbox('Obtener datos por fecha y barrio', False):
    df2=df.groupby(['occur_date','boro'])[['incident_key']].count().reset_index().rename(columns={'boro':'Barrio','occur_date':'Fecha','incident_key':'Disparos'})
    df2['Fecha'] = pd.to_datetime(df2['Fecha']).dt.date
    
    fig = go.Figure(data=[go.Table(
        header =dict(values=list(df2.columns),
                     fill_color ='lightgrey',
                     line_color ='darkslategray'),
        cells =dict(values=[df2.Fecha, df2.Barrio, df2.Disparos],
                    fill_color ='white',
                    line_color ='lightgrey'))])
    
    fig.update_layout(width =500, height = 450)
    st.write(fig)
    
    ## se manda el link 
    st.markdown(get_table_download_link(df2),unsafe_allow_html=True)
    















