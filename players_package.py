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
def players_squad_team_id_season(team_id,season):
    team_id,season = str(team_id),str(season)
    url_players_squad_team_id_season = url + "players/squad/" + team_id + "/" + season
    response = requests.request("GET", url_players_squad_team_id_season, headers=headers)
    print("players_squad_team_id_season + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['players']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['players'])

# OK - Test light
def players_squad_team_id_season_s(team_id,game_fixture_id):    
    start_time = time.time()
    try: 
        for i in range (len(seasons_diff)):
            try:
                my_file = Path(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' + 'players_package'+'/'+'players_squad_team_id_season_s'+'_'+ str(team_id)+'_'+ str(seasons_diff[i])+'.pkl')
                if not my_file.is_file() or seasons_diff[i] == seasons_diff[-1] :   
                    x = players_squad_team_id_season(team_id,seasons_diff[i])[1]
                    x.to_pickle(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' + 'players_package'+'/'+'players_squad_team_id_season_s'+'_'+ str(team_id)+'_'+ str(seasons_diff[i])+'.pkl')
            except:
                print("Error with {}".format(i))
    except: 
        for i in range (len(seasons)):
            try:
                my_file = Path(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' + 'players_package'+'/'+'players_squad_team_id_season_s'+'_'+ str(team_id)+'_'+ str(seasons[i])+'.pkl')
                if not my_file.is_file() or seasons[i] == seasons[-1]:   
                    x = players_squad_team_id_season(team_id,seasons[i])[1]
                    x.to_pickle(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' + 'players_package'+'/'+'players_squad_team_id_season_s'+'_'+ str(team_id)+'_'+ str(seasons[i])+'.pkl')
            except:
                print("Error with {}".format(i))
    print("players_squad_team_id_season_s() : {}".format(round(time.time()-start_time,2)))    

# OK -
def players_statistics_team_id_season(team_id,season):
    team_id,season = str(team_id),str(season)
    url_statistics_players_team_id_season = url + "players/team/" + team_id + "/" + season
    response = requests.request("GET", url_statistics_players_team_id_season, headers=headers)  
    print("players_statistics_team_id_season + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['players']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['players'])

# OK - Test
def players_statistics_team_id_season_s(team_id,game_fixture_id):
    start_time = time.time()
    try: 
        for i in range (len(seasons_diff)):
            try:
                my_file = Path(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' + 'players_package'+'/'+'players_statistics_team_id_season_s'+'_'+ str(team_id)+'_'+ str(seasons_diff[i])+'.pkl')
                if not my_file.is_file() or seasons_diff[i] == seasons_diff[-1]:    
                    x = players_statistics_team_id_season(team_id,seasons_diff[i])[1]
                    x.to_pickle(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' + 'players_package'+'/'+'players_statistics_team_id_season_s'+'_'+ str(team_id)+'_'+ str(seasons_diff[i])+'.pkl')
            except:
                print("Error with {}".format(i))
    except: 
        for i in range (len(seasons)):
            try:
                my_file = Path(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' + 'players_package'+'/'+'players_statistics_team_id_season_s'+'_'+ str(team_id)+'_'+ str(seasons[i])+'.pkl')
                if not my_file.is_file() or seasons[i] == seasons[-1]:   
                    x = players_statistics_team_id_season(team_id,seasons[i])[1]
                    x.to_pickle(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' + 'players_package'+'/'+'players_statistics_team_id_season_s'+'_'+ str(team_id)+'_'+ str(seasons[i])+'.pkl')
            except:
                print("Error with {}".format(i))
    print("players_statistics_team_id_season_s() : {}".format(round(time.time()-start_time,2)))    


# OK -
def players_statistics_player_id_season(player_id,season):
    player_id,season = str(player_id),str(season)
    url_statistics_players_player_id_season = url + "players/player/" + player_id + "/" + season
    response = requests.request("GET", url_statistics_players_player_id_season, headers=headers)
    print("players_statistics_player_id_season + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['players']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['players'])

# OK - Test
def players_statistics_player_id_season_s(team_id,game_fixture_id):
    start_time = time.time()
    try: 
        for i in range (len(seasons_diff)):
            df = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' + 'players_package'+'/'+'players_squad_team_id_season_s'+ '_'+ str(team_id) + '_'+ str(seasons_diff[i]) +'.pkl') 
            for j in range (len(df)):
                player_id = df.iloc[j,df.columns.get_loc('player_id')]
                try:
                    my_file = Path(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' + 'players_package'+'/'+'players_statistics_player_id_season_s'+'_'+ str(player_id)+'_'+ str(seasons_diff[i])+'.pkl')
                    if not my_file.is_file() or seasons_diff[i] == seasons_diff[-1]:     
                        x = players_statistics_player_id_season(player_id,seasons_diff[i])[1]
                        x.to_pickle(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' + 'players_package'+'/'+'players_statistics_player_id_season_s'+'_'+ str(player_id)+'_'+ str(seasons_diff[i])+'.pkl')
                except:
                    print("Error with {}".format(i))
    except: 
        for i in range (len(seasons)):
            df = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' + 'players_package'+'/'+'players_squad_team_id_season_s'+ '_'+ str(team_id) + '_'+ str(seasons[i]) +'.pkl') 
            for j in range (len(df)):
                player_id = df.iloc[j,df.columns.get_loc('player_id')]
                my_file = Path(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' + 'players_package'+'/'+'players_statistics_player_id_season_s'+'_'+ str(player_id)+'_'+ str(seasons[i])+'.pkl')
                if not my_file.is_file() or seasons[i] == seasons[-1]:   
                    y = players_statistics_player_id_season(player_id,seasons[i])[1]
                    y.to_pickle(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' + 'players_package'+'/'+'players_statistics_player_id_season_s'+'_'+ str(player_id)+'_'+ str(seasons[i])+'.pkl')
    print("players_statistics_player_id_season_s() : {}".format(round(time.time()-start_time,2)))    

# OK - 
def players_statistics_fixture_id(fixture_id):
    fixture_id = str(fixture_id)
    url_statistics_players_fixture_id = url + "players/fixture/" + fixture_id 
    response = requests.request("GET", url_statistics_players_fixture_id, headers=headers) 
    print("players_statistics_fixture_id + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['players']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['players'])

# OK - Test
def players_statistics_fixture_id_s(team_id,k,game_fixture_id):
    start_time = time.time()
    data = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_last_s'+ '_'+ str(team_id) + '_'+ str(last) +'.pkl') 
    for i in range (len(data)):
        try:
            fixture_id = data.iloc[i,data.columns.get_loc('fixture_id')]
            my_file = Path(link_data+central_folder+'/'+link_data_package_players_central+'/'+'players_statistics_fixture_id_s'+'_'+ str(fixture_id)+'.pkl')
            if not my_file.is_file():
                x = players_statistics_fixture_id(fixture_id)[1]
                x.to_pickle(link_data+central_folder+'/'+link_data_package_players_central+'/'+'players_statistics_fixture_id_s'+'_'+ str(fixture_id)+'.pkl')
            elif my_file.is_file() and int(data.iloc[i,data.columns.get_loc('event_timestamp')])>int(start_time_update) and int(data.iloc[i,data.columns.get_loc('event_timestamp')])<int(now_time) and len(pd.read_pickle(link_data+central_folder+'/'+link_data_package_players_central+'/'+'players_statistics_fixture_id_s'+'_' + str(fixture_id)+'.pkl')) == 0:   
                time_variable = os.path.getmtime(link_data+central_folder+'/'+link_data_package_players_central+'/'+'players_statistics_fixture_id_s'+'_'+ str(fixture_id)+'.pkl')
                if time_variable<(datetime.timestamp(datetime.now()-timedelta(seconds=detla_seconds_update))):
                    x = players_statistics_fixture_id(fixture_id)[1]
                    x.to_pickle(link_data+central_folder+'/'+link_data_package_players_central+'/'+'players_statistics_fixture_id_s'+'_'+ str(fixture_id)+'.pkl')
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
            if i<last+5: # A buffer because the first fixtures are not taken into account 
                try:
                    fixture_id = data2.iloc[i,data2.columns.get_loc('fixture_id')]
                    my_file = Path(link_data+central_folder+'/'+link_data_package_players_central+'/'+'players_statistics_fixture_id_s'+'_'+ str(fixture_id)+'.pkl')
                    if not my_file.is_file() or (my_file.is_file() and int(data2.iloc[i,data2.columns.get_loc('event_timestamp')])>int(start_time_update) and int(data2.iloc[i,data2.columns.get_loc('event_timestamp')])<int(now_time) and len(pd.read_pickle(link_data+central_folder+'/'+link_data_package_players_central+'/'+'players_statistics_fixture_id_s'+'_' + str(fixture_id)+'.pkl')) == 0):
                        x = players_statistics_fixture_id(fixture_id)[1]
                        x.to_pickle(link_data+central_folder+'/'+link_data_package_players_central+'/'+'players_statistics_fixture_id_s'+'_'+ str(fixture_id)+'.pkl')
                except:
                    print("Error with {}".format(i))
        
        data3 = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_identical_season_s'+ '_'+ str(seasons[-2]) + '.pkl')
        for i in range (len(data3)):
            try:
                fixture_id = data3.iloc[i,data3.columns.get_loc('fixture_id')]
                my_file = Path(link_data+central_folder+'/'+link_data_package_players_central+'/'+'players_statistics_fixture_id_s'+'_'+ str(fixture_id)+'.pkl')
                if not my_file.is_file() or (my_file.is_file() and int(data3.iloc[i,data3.columns.get_loc('event_timestamp')])>int(start_time_update) and int(data3.iloc[i,data3.columns.get_loc('event_timestamp')])<int(now_time) and len(pd.read_pickle(link_data+central_folder+'/'+link_data_package_players_central+'/'+'players_statistics_fixture_id_s'+'_' + str(fixture_id)+'.pkl')) == 0):
                    x = players_statistics_fixture_id(fixture_id)[1]
                    x.to_pickle(link_data+central_folder+'/'+link_data_package_players_central+'/'+'players_statistics_fixture_id_s'+'_'+ str(fixture_id)+'.pkl')
            except:
                print("Error with {}".format(i))

    print("players_statistics_fixture_id_s() : {}".format(round(time.time()-start_time,2))) 
'''
Additional functions
------------------------------------------------------------------------------------
'''

# OK - 
def output_players_name (player_id):
    player_id = str(player_id)
    url_statistics_players_fixture_id = url + "players/player/" + player_id 
    response = requests.request("GET", url_statistics_players_fixture_id, headers=headers) 
    print("output_players_name + 1")
    x = list(pd.DataFrame.from_dict(json.loads(response.text)['api']['players']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['players'])
    return x[1]['lastname'][0],x[1]['firstname'][0]
