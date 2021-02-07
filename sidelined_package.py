# Imports
import requests
import json
import pandas as pd  
import numpy as np
from pathlib import Path
import time

from parameters_package import *
from core_functions import * # For nan_to_zero function

'''
Package parameters
------------------------------------------------------------------------------------
'''

'''
Functions
------------------------------------------------------------------------------------
'''
# Need to get intermediary calculations

# OK -
def sidelined_coach_id(coach_id):    
    coach_id = str(coach_id)
    sidelined_coach_id = url + "sidelined/coach/" + coach_id 
    response = requests.request("GET", sidelined_coach_id, headers=headers)
    print("sidelined_coach_id + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['sidelined']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['sidelined'])

# OK - No Test
def sidelined_coach_id_s(team_id,game_fixture_id):    
    start_time = time.time()
    data = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' + 'coachs_package'+'/'+'coachs_team_id_s'+ '_'+ str(team_id) +'.pkl') 
    for i in range (len(data)):
        try:
            coach_id = data.iloc[i,data.columns.get_loc('coach_id')]
            x = sidelined_coach_id(coach_id)[1]
            x.to_pickle(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' +'sidelined_package'+'/'+'sidelined_coach_id_s'+'_'+ str(coach_id)+'.pkl')
        except:
            print("Error with {}".format(i))
    print("sidelined_coach_id_s() : {}".format(round(time.time()-start_time,2)))    

# OK - 
def sidelined_player_id(player_id):
    player_id = str(player_id)
    sidelined_player_id = url + "sidelined/player/" + player_id 
    response = requests.request("GET", sidelined_player_id, headers=headers)
    print("sidelined_player_id + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['sidelined']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['sidelined'])

# OK - No Test
def sidelined_player_id_s(team_id,game_fixture_id):    
    start_time = time.time()
    for i in range (-1,0):
        try:
            data = pd.read_pickle(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' + 'players_package'+'/'+'players_squad_team_id_season_s'+'_'+ str(team_id)+'_'+ str(seasons_diff[i])+'.pkl')
            for j in range (len(data)):
                player_id = data.iloc[j,data.columns.get_loc('player_id')]
                try: 
                    x = sidelined_player_id(player_id)[1]
                    x.to_pickle(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' +'sidelined_package'+'/'+'sidelined_player_id_s'+'_'+ str(player_id) +'.pkl')
                except:
                    print("Error with {},{}".format(i,j))
        except: 
            data = pd.read_pickle(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' + 'players_package'+'/'+'players_squad_team_id_season_s'+'_'+ str(team_id)+'_'+ str(seasons[i])+'.pkl')
            for j in range (len(data)):
                player_id = data.iloc[j,data.columns.get_loc('player_id')]
                try:  
                    x = sidelined_player_id(player_id)[1]
                    x.to_pickle(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' +'sidelined_package'+'/'+'sidelined_player_id_s'+'_'+ str(player_id) +'.pkl')
                except:
                    print("Error with {},{}".format(i,j)) 
    print("sidelined_player_id_s() : {}".format(round(time.time()-start_time,2)))  