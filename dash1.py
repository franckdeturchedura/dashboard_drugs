import dash
from dash import *
import dash_core_components as dcc
import dash_html_components as html
#from dash.depedencies import Input,Output
import pandas as pd
import plotly.graph_objs as go
import folium
import plotly
import plotly_express as px
#stylesheet pour avoir un petit style qui mets bien
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#création de l'application
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
#app.scripts.config.serve_locally = False
#app.config.serve_locally = False
#app.css.append_css({'external_url':'https://codepen.io/amyoshino/pen/jzXypZ.css'})

#on lit le fichier xlsx car le csv ne peut pas être lu
file  = pd.read_excel("dataset.xlsx",encoding='utf-8')
#on repasse le fichier en csv
csv = file.to_csv('tempo.csv', encoding='utf-8', index=False)

#on lit la dataframe et on la stocke dans df
df = pd.read_csv("tempo.csv")

print(df)

#utilisation de folium

df_gps = pd.read_csv("countries.csv")
df_gps =df_gps.rename(columns={" 'Andorra')": "Country","            ('AD'":"Init",' 42.546245':"Latitude",' 1.601554':"Longitude"})
df_gps['Country'][0].strip(")")

for i in range(len(df_gps['Country'])):
  #print(i.strip(")"))
  df_gps=df_gps.replace({df_gps['Country'][i]:df_gps['Country'][i].strip(")")})
  df_gps=df_gps.replace({df_gps['Country'][i]:df_gps['Country'][i].strip(" '")})

for i in range(len(df_gps['Init'])):
  #print(i.strip(")"))
  df_gps=df_gps.replace({df_gps['Init'][0]:df_gps['Init'][0].strip("            (")})


countries_gps = df_gps['Country'].unique()
lat_gps = df_gps['Latitude'].unique()
long_gps = df_gps['Longitude'].unique()

dic = {}
for i in df_gps['Country']:
  dic[i]=[df_gps[df_gps['Country']==i]['Longitude'],df_gps[df_gps['Country']==i]['Latitude']]

df_gps_clean = pd.DataFrame()
df_gps_clean['Country'] = df_gps['Country']
df_gps_clean['Longitude'] = df_gps['Longitude']
df_gps_clean['Latitude'] = df_gps['Latitude']
df_gps_clean = df_gps_clean.replace(df_gps_clean[df_gps_clean['Country']=='Vietnam']['Country'],'Viet Nam')
df_gps_clean.loc[234,'Country'] = 'Viet Nam'



df=df.join(df_gps_clean.set_index('Country'), on='Country')

print(df[0:10])

df.to_csv('DataFrame.csv',sep='\t', encoding='utf-8')


for i in df[df['Country']=='United States of America']['Country']:
  df=df.replace({i:'USA'})

for i in df[df['Country']=="Russian Federation"]['Country']:
  df = df.replace({i:'Russia'})

for i in df[df['Country']=="United Kingdom (Northern Ireland)"]['Country']:
  df = df.replace({i:'England'})

df['Best']=df['Best'].apply(lambda x: x.replace(',','.'))

df['Country'] = df['Country'].astype(str)
#type(df['Country'][0])
type(df['Best'][0])

df['Best'] = df['Best'].astype(str)
df['Best'] = df['Best'].astype(float)

df =df.fillna(0)


def map_dash(year,drug):
    data_json = 'world_countries.json'
    dff = df[df['Year']==year]
    dff = dff[dff['Drug Group']==drug]

    map_dash = folium.Map(location=[48.8534 , 2.3488],
        tiles='Stamen Toner',
        zoom_start=2)
    tooltip = 'Click here for more information'
    test_coo = dic.values()
    list_coo = list(test_coo)
    list_coo = list_coo[0:100]

    folium.Choropleth(
    geo_data=data_json,
    name='choropleth',
    data=dff,
    columns=['Country', 'Best'],
    key_on='feature.properties.name',
    fill_color='Reds',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Drugs rate',
    nan_fill_color = 'Black'
).add_to(map_dash)

    """for i in list_coo:
        long = float(i[0])
        #print("Long : ")
        #print(long)
        lat = float(i[1])
        pays = dff[dff['Latitude']==lat]['Country']
        pays = str(pays)
        #print("LAt : ")
        #print(lat)
        #folium.CircleMarker(radius=20,location=[lat,long],popup='Test',color='crimson',fill='False').add_to(map_dash)

        folium.Marker(location=[lat,long], popup=pays, tooltip=tooltip, icon=folium.Icon(color='red', icon='info-sign')).add_to(map_dash)"""
    return map_dash







#map_dash = folium.Map(location=[48.8534 , 2.3488],
#    tiles='Stamen Toner',
#    zoom_start=2)

#map_dash = map_dash(year_slider)

#map_dash.save('test_map1.html')

#DASHBOARD

available_indicators = df['Drug Group'].unique()

app.layout = html.Div([

html.Div([
 html.H1('Test Map')
 ],className="row"),

        html.Div([
        #Permettra de choisir l'axe des abscisses qu'on veut
            dcc.Dropdown(
                id='drugs_choice',
                options=[{'label': i, 'value': i} for i in available_indicators],#prends ses valeurs dans les indcateurs disponibles définis plus haut
                value='Cannabis'
            ),
            #permettra de prendre une échelle linéaire ou log

        ],
        style={'width': '30%', 'display': 'inline-block'}),


html.Div([

                    #TITRE

                       #MAP
                       html.Div(id='map'),
                       #html.Iframe(id='map',srcDoc=open('test_map1.html','r').read(),width='90%',height='600'),

                       html.Div([dcc.Slider(
                       id='year_slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].min(),
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None,
                       )], style = {'width': '90%','margin-left':50, 'align-items': 'center' ,'justify-content':'center'})
],className="row")
])

from dash.dependencies import Input, Output


@app.callback(Output('map','children'),[Input('year_slider','value'),Input('drugs_choice','value')])

def update_iframe(year_value,drugs_choice):
    if year_value and drugs_choice:
        map_dash_callback = map_dash(year_value,drugs_choice)
        map_dash_callback.save('test_map1_callback.html')
        return html.Iframe(srcDoc=open('test_map1_callback.html','r').read(),width='98%',height='600')
    else:
        return [{}]




if __name__ == '__main__':
    app.run_server(debug=True)
