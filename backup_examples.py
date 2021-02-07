# Imports
import requests
import json
import pandas as pd  
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.ticker import StrMethodFormatter
from pathlib import Path
import time
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches
import plotly
import plotly.graph_objects as go
from math import pi

from parameters_package import *
from core_functions import * # For nan_to_zero function
from output_v2 import *
from summarize import *

import seaborn as sns
import warnings; warnings.filterwarnings(action='once')

game_fixture_id = "592295 Everton-Manchester City"
team_id = 212

start_time = time.time()
data = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_last_s'+ '_'+ str(team_id) + '_'+ str(last) +'.pkl') 
for i in range (len(data)):
    try:
        fixture_id = data.iloc[i,data.columns.get_loc('fixture_id')]
        my_file = Path(link_data+central_folder+'/'+link_data_package_players_central+'/'+'players_statistics_fixture_id_s'+'_'+ str(fixture_id)+'.pkl')
        if not my_file.is_file() or (my_file.is_file() and int(data.iloc[i,data.columns.get_loc('event_timestamp')])>int(start_time_update) and int(data.iloc[i,data.columns.get_loc('event_timestamp')])<int(now_time) and len(pd.read_pickle(link_data+central_folder+'/'+link_data_package_players_central+'/'+'players_statistics_fixture_id_s'+'_' + str(fixture_id)+'.pkl')) == 0):
            time_variable = os.path.getmtime(link_data+central_folder+'/'+link_data_package_players_central+'/'+'players_statistics_fixture_id_s'+'_'+ str(fixture_id)+'.pkl')
            if time_variable<(datetime.timestamp(datetime.now()-timedelta(seconds=detla_seconds_update))):
                print(fixture_id)
    except:
        print("Error with {}".format(i))


    '''

# Normal bar chart

x = ['Nuclear', 'Hydro', 'Gas', 'Oil', 'Coal', 'Biofuel']
energy = [5, 6, 15, 22, 24, 8]

x_pos = [i for i, _ in enumerate(x)]

plt.bar(x_pos, energy, color='green')
plt.xlabel("Energy Source")
plt.ylabel("Energy Output (GJ)")
plt.title("Energy output from various fuel sources")

plt.xticks(x_pos, x)

plt.show()


# Multiple X's bar chart

N = 5
men_means = (20, 35, 30, 35, 27)
women_means = (25, 32, 34, 20, 25)

ind = np.arange(N) 
width = 0.35       
plt.bar(ind, men_means, width, label='Men')
plt.bar(ind + width, women_means, width,
    label='Women')

plt.ylabel('Scores')
plt.title('Scores by group and gender')

plt.xticks(ind + width / 2, ('G1', 'G2', 'G3', 'G4', 'G5'))
plt.legend(loc='best')
plt.show()

# Stacked bar chart

countries = ['USA', 'GB', 'China', 'Russia', 'Germany']
bronzes = np.array([38, 17, 26, 19, 15])
silvers = np.array([37, 23, 18, 18, 10])
golds = np.array([46, 27, 26, 19, 17])
ind = [x for x, _ in enumerate(countries)]

plt.bar(ind, golds, width=0.8, label='golds', color='gold', bottom=silvers+bronzes)
plt.bar(ind, silvers, width=0.8, label='silvers', color='silver', bottom=bronzes)
plt.bar(ind, bronzes, width=0.8, label='bronzes', color='#CD853F')

plt.xticks(ind, countries)
plt.ylabel("Medals")
plt.xlabel("Countries")
plt.legend(loc="upper right")
plt.title("2012 Olympics Top Scorers")

plt.show()



    Plotly radar chart

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[1, 5, 2, 2, 3],
        theta=categories,
        fill='toself',
        name='Product A'
    ))
    fig.add_trace(go.Scatterpolar(
        r=[4, 3, 2.5, 1, 2],
        theta=categories,
        fill='toself',
        name='Product B'
    ))

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0, 5]
        )),
    showlegend=False
    )

    fig.show()

'''

