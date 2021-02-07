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

# OK -
def transfers_player_id(player_id):
    player_id = str(player_id)
    url_players_transfers_player_id = url + "transfers/player/" + player_id 
    response = requests.request("GET", url_players_transfers_player_id, headers=headers)
    print("transfers_player_id + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['transfers']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['transfers'])

# OK - Test
def transfers_player_id_s(team_id,game_fixture_id):
    start_time = time.time()
    for i in range (-1,0):
        try:
            data = pd.read_pickle(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' + 'players_package'+'/'+'players_squad_team_id_season_s'+'_'+ str(team_id)+'_'+ str(seasons_diff[i])+'.pkl')
            for j in range (len(data)):
                player_id = data.iloc[j,data.columns.get_loc('player_id')]
                try:
                    my_file = Path(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' +'transfers_package'+'/'+'transfers_player_id_s'+'_'+ str(player_id) +'.pkl')
                    if not my_file.is_file():   
                        x = transfers_player_id(player_id)[1]
                        x.to_pickle(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' +'transfers_package'+'/'+'transfers_player_id_s'+'_'+ str(player_id) +'.pkl')
                except:
                    print("Error with {},{}".format(i,j))
        except: 
            data = pd.read_pickle(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' + 'players_package'+'/'+'players_squad_team_id_season_s'+'_'+ str(team_id)+'_'+ str(seasons[i])+'.pkl')
            for j in range (len(data)):
                player_id = data.iloc[j,data.columns.get_loc('player_id')]
                try:
                    my_file = Path(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' +'transfers_package'+'/'+'transfers_player_id_s'+'_'+ str(player_id) +'.pkl')
                    if not my_file.is_file():   
                        x = transfers_player_id(player_id)[1]
                        x.to_pickle(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' +'transfers_package'+'/'+'transfers_player_id_s'+'_'+ str(player_id) +'.pkl')
                except:
                    print("Error with {},{}".format(i,j))    
    print("transfers_player_id_s() : {}".format(round(time.time()-start_time,2)))  

'''
Additional functions
------------------------------------------------------------------------------------
'''

