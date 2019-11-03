#On importe les librairies utiles


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
import dash_bootstrap_components as dbc
import dash_table as dt

##scrapping of worldometers##
from selenium import webdriver
import os

os.chmod('C:/Users/feld7/OneDrive/Documents/chromedriver/chromedriver.exe', 755)
d = webdriver.Chrome(executable_path='C:/Users/feld7/OneDrive/Documents/chromedriver/chromedriver.exe')

d.get('https://www.worldometers.info/drugs/')

#fonction qui permet de scrapper la donnée dynamique (Spending on illegal drugs)
def get_spending_drug():

    return d.find_element_by_css_selector('[rel="drug_spending/this_year"]').text


#création de l'application
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])


#on lit le fichier xlsx car le csv ne peut pas être lu
file  = pd.read_excel("dataset.xlsx",encoding='utf-8')


#on repasse le fichier en csv
csv = file.to_csv('tempo.csv', encoding='utf-8', index=False)

#on lit la dataframe et on la stocke dans df
df = pd.read_csv("tempo.csv")

#print(df)

#On utilise un autre csv pour avoir les géolocalisations des pays de la premiere database
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


#df sera notre dataset final avec les coordonnées etc
df=df.join(df_gps_clean.set_index('Country'), on='Country')

print(df[0:10])

#on peut retrouver notre nouveau dataset en csv comme ça
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


#on remplace tous les nan par 0
df =df.fillna(0)

#on crée une fonction qui crée une map avec les deux paramètres qui seront au final donnés par les components.

def map_dash(year,drug):
    if year==2002:
        dff = df[df['Drug Group']==drug]
        data_json = 'world_countries.json'

    else:
        data_json = 'world_countries.json'
        dff = df[df['Year']==year]
        dff = dff[dff['Drug Group']==drug]



    map_dash = folium.Map(location=[48.8534 , 2.3488],
        #tiles='Stamen Toner',
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
    legend_name='Drugs rate (% of the population) ',
    nan_fill_color = 'Black'
).add_to(map_dash)

    for i in dff['Country']:
        try:
            lat = dff[dff['Country']==i]['Latitude']
            long = dff[dff['Country']==i]['Longitude']
            country = str(i)
            diam = (dff[dff['Country']==i]['Best']).astype(float)
            #diam = float(diam[0])
            #diam_str = float(diam).astype(str)
            diam = float(diam)
            diam_str = str(diam)
            #print(float(diam))
            folium.CircleMarker(radius=diam*2,location=[lat,long],popup=country +' Rate ' +diam_str+'%',tooltip = 'Click here for more infos',color='crimson',fill='False').add_to(map_dash)
        except:
            pass


        #folium.Marker(location=[lat,long], popup=pays, tooltip=tooltip, icon=folium.Icon(color='red', icon='info-sign')).add_to(map_dash)
    return map_dash



#Pour le slider
a = {str(year): str(year) for year in df['Year'].unique()}
a['2002'] = 'All'


#map_dash = folium.Map(location=[48.8534 , 2.3488],
#    tiles='Stamen Toner',
#    zoom_start=2)

#map_dash = map_dash(year_slider)

#map_dash.save('test_map1.html')

#DASHBOARD
import numpy as np
available_indicators = df['Drug Group'].unique()

#on bootstrap, c'est pour ça qu'il y a des col et des Row



navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Donwload CSV", href="https://drive.google.com/open?id=1wOVP7D9uNAMd0Ks87RpWfvd-iJ1egqxp")),
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            color = "info",
            label="Contact",
            children=[
                dbc.DropdownMenuItem("Franck Deturche-Dura",href='https://www.linkedin.com/in/franck-deturche-dura'),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Yasmine Djemame",href='#'),
            ],
        ),
    ],
    brand="Drugs Uses Around The World",
    brand_href="#",
    sticky="top",
)
#####################################################""""
body = dbc.Container(
    [


        dbc.Row([

        dbc.Col([],md=6),

            dbc.Col([

                dcc.Dropdown(
                    id='drugs_choice',
                    options=[{'label': i, 'value': i} for i in available_indicators],#prends ses valeurs dans les indcateurs disponibles définis plus haut
                    value='Cannabis'
                ),
                ]),

        ]),
        dbc.Row(
            [


                dbc.Col(
                    [
                        html.H2("Description - Analyse"),
                        html.P(
                            """\
Nous constatons que via la Map que les drogues douces (cannabis) sont bien plus présentes que les drogues dures (les autres).... Check ReadMe to see more ."""
                        ),
                        dbc.Button("View git", color="secondary",href='https://git.esiee.fr/djemamey/mini-projet-python'),
                        html.P("\n\n\n\n\n\n"),
                        html.Div([dcc.Dropdown(
                            id='drugs_choice_histo',
                            options=[{'label': i, 'value': i} for i in available_indicators],#prends ses valeurs dans les indcateurs disponibles définis plus haut
                            value='Cannabis'
                        )],style={'width': '50%', 'display': 'inline-block'}),

                        dcc.Graph(
                        id = 'scatter'
                        ),

                    ],
                    md=5,
                ),#col

                dbc.Col(
                    [
                        html.H2("Map"),
                        html.Div(id='map'),
                        html.Div([dcc.Slider(
                        id='year_slider',
         min=2002,
         #min = df['Year'].min(),
         max=int(df['Year'].max()),

         value=2002,
         marks=a,
         step=None,
                        )], style = {'width': '90%','margin-left':30, 'align-items': 'center' ,'justify-content':'center'})

                    ]
                    ),


            ]#row
        ),#row
        dbc.Row([]),
        dbc.Row([

        dbc.Col([
        html.H3(""),
            dcc.Graph(id='histo')
            ]),
        dbc.Col([

        html.Div([
        html.P(""),
        html.H2("Spending on Drugs this year")], style = {'width': '90%','margin-left':30, 'textAlign': 'center' ,'justify-content':'center'}),
        html.Div([
        html.H2(id="spend"),
        #html.H2(str(get_spending_drug() + "$")),
        dbc.Button("Actualiser",id="button_spend", color="secondary"),

        ], style = {'width': '90%','margin-left':30, 'textAlign': 'center' ,'justify-content':'center'}),
        ]),
        ]),
    ],
    className="mt-4",
)




from dash.dependencies import Input, Output
app.layout = html.Div([navbar,body])

@app.callback(Output('map','children'),[Input('year_slider','value'),Input('drugs_choice','value')])

def update_iframe(year_value,drugs_choice):
    if year_value and drugs_choice:
        map_dash_callback = map_dash(year_value,drugs_choice)
        map_dash_callback.save('test_map1_callback.html')
        return html.Iframe(srcDoc=open('test_map1_callback.html','r').read(),width='98%',height='600')
    else:
        return [{}]

@app.callback(Output("spend","children"),[Input("button_spend","n_clicks")])
def on_button_click(n):
    if n !=0:
        return str(get_spending_drug()) + "$"
    else:
        return str(get_spending_drug()) + "$"



@app.callback(Output('histo','figure'),[Input('drugs_choice_histo','value')])

def update_histo(drug_choice):
    if drug_choice:
        return{
            'data': [go.Histogram(
            x=df[df['Drug Group']==drug_choice]['Year'],
            y = df[df['Drug Group']==drug_choice]['Best']

            )],
            #On définit ce qui se passe dans le layout
            'layout': go.Layout(
                xaxis={
                    'title': "Year",#On prends l'axe des abscisses
                },
                yaxis = {'title':'Rate'},

                margin={'l': 0, 'b': 40, 't': 10, 'r': 0},
                hovermode='closest'
            )

        }
    else:
        return [{}]





@app.callback(Output('scatter','figure'),[Input('drugs_choice_histo','value')])

def update_scatter(drug_choice):
    if drug_choice:
        return{
    #On définit la data qui va dans le graphe
        'data': [go.Scatter(
            x=df[df['Drug Group'] == drug_choice]['Best'],
            y = df[df['Drug Group']==drug_choice]['Year'],
            text=df[df['Drug Group'] == drug_choice]['Country'],#quand on passe la souris dessus, affiche le pays
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        #On définit ce qui se passe dans le layout
        'layout': go.Layout(
            xaxis={
                'title': "Drug Rate (% of the population consumming drugs)",#On prends l'axe des abscisses
            },
            yaxis = {'title':'Year'},

            margin={'l': 0, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }
    else:
        return [{}]


if __name__ == '__main__':
    app.run_server(debug=True)
