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
def lineups_fixture_id(fixture_id): 
    fixture_id = str(fixture_id)
    url_lineups = url + "lineups/" + fixture_id 
    response = requests.request("GET", url_lineups, headers=headers)
    print("lineups_fixture_id + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['lineUps']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['lineUps'])

# OK - Test
def lineups_fixture_id_s(team_id,k,game_fixture_id): 
    start_time = time.time()
    data = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_last_s'+ '_'+ str(team_id) + '_'+ str(last) +'.pkl') 

    for i in range (len(data)):
        try:
            fixture_id = data.iloc[i,data.columns.get_loc('fixture_id')]
            my_file = Path(link_data+central_folder+'/'+link_data_package_lineups_central+'/'+'lineups_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
            if not my_file.is_file() or (my_file.is_file() and int(data.iloc[i,data.columns.get_loc('event_timestamp')])>int(start_time_update) and int(data.iloc[i,data.columns.get_loc('event_timestamp')])<int(now_time) and len(pd.read_pickle(link_data+central_folder+'/'+link_data_package_lineups_central+'/'+'lineups_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')) == 0):     
                x = lineups_fixture_id(fixture_id)[1]
                x.to_pickle(link_data+central_folder+'/'+link_data_package_lineups_central+'/'+'lineups_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
        except:
            print("Error with {}".format(i))

    if k == 1:
        next_id = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_next_s'+ '_'+ str(team_id) + '_'+ str(nex) + '.pkl')
        if int(next_id.iloc[0,next_id.columns.get_loc("homeTeam")]['team_id']) == team_id:
            next_id = int(next_id.iloc[0,next_id.columns.get_loc("awayTeam")]['team_id'])
        else:
            next_id = int(next_id.iloc[0,next_id.columns.get_loc("homeTeam")]['team_id'])
        data2 = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_h2h_team_id_team_id_next_s'+ '_'+ str(team_id) + '_'+ str(next_id) + '.pkl') 

        for i in range (len(data2)):
            if i<last+5:    
                try:
                    fixture_id = data2.iloc[i,data2.columns.get_loc('fixture_id')]
                    my_file = Path(link_data+central_folder+'/'+link_data_package_lineups_central+'/'+'lineups_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
                    if not my_file.is_file() or (my_file.is_file() and int(data2.iloc[i,data2.columns.get_loc('event_timestamp')])>int(start_time_update) and int(data2.iloc[i,data2.columns.get_loc('event_timestamp')])<int(now_time) and len(pd.read_pickle(link_data+central_folder+'/'+link_data_package_lineups_central+'/'+'lineups_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')) == 0):     
                        x = lineups_fixture_id(fixture_id)[1]
                        x.to_pickle(link_data+central_folder+'/'+link_data_package_lineups_central+'/'+'lineups_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
                except:
                    print("Error with {}".format(i))

        data3 = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_identical_season_s'+ '_'+ str(seasons[-2]) + '.pkl')
        for i in range (len(data3)):
            try:
                fixture_id = data3.iloc[i,data3.columns.get_loc('fixture_id')]
                my_file = Path(link_data+central_folder+'/'+link_data_package_lineups_central+'/'+'lineups_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
                if not my_file.is_file() or (my_file.is_file() and int(data3.iloc[i,data3.columns.get_loc('event_timestamp')])>int(start_time_update) and int(data3.iloc[i,data3.columns.get_loc('event_timestamp')])<int(now_time) and len(pd.read_pickle(link_data+central_folder+'/'+link_data_package_lineups_central+'/'+'lineups_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')) == 0):     
                    x = lineups_fixture_id(fixture_id)[1]
                    x.to_pickle(link_data+central_folder+'/'+link_data_package_lineups_central+'/'+'lineups_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
            except:
                print("Error with {}".format(i))

    print("lineups_fixture_id_s() : {}".format(round(time.time()-start_time,2))) 