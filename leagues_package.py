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

# OK - No Test
def leagues_team_id_s(team_id,game_fixture_id):
    start_time = time.time()
    team_id = str(team_id)
    url_leagues_team_id = url + "leagues/team/" + team_id  
    response = requests.request("GET", url_leagues_team_id, headers=headers)
    print("leagues_team_id_s + 1")
    pd.DataFrame.from_dict(json.loads(response.text)['api']['leagues']).to_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'leagues_package'+'/'+'leagues_team_id_s'+ '_'+ team_id +'.pkl')
    print("leagues_team_id_s() : {}".format(round(time.time()-start_time,2))) 

# OK - No Test because a new competition can occures
def leagues_team_id_relevant_s(team_id,game_fixture_id):
    start_time = time.time()
    team_id = str(team_id)
    data = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'leagues_package'+'/'+'leagues_team_id_s'+ '_'+ str(team_id) +'.pkl') 
    data1 = data.loc[data['season'] == int(seasons[-1])]
    data3 = data1.loc[data1['type'] == "League"]
    data3.to_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'leagues_package'+'/'+'leagues_team_id_relevant_s'+ '_'+ team_id +'.pkl')
    print("leagues_team_id_relevant_s() : {}".format(round(time.time()-start_time,2))) 

# OK - No Test because a new competition can occures
def leagues_team_id_relevant2_s(team_id,game_fixture_id):
    start_time = time.time()
    team_id = str(team_id)
    array = [2020,2019]
    data = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'leagues_package'+'/'+'leagues_team_id_s'+ '_'+ str(team_id) +'.pkl') 
    data1 = data.loc[data['season'].isin(array)]
    data3 = data1.loc[data1['type'] == "League"]
    data3.to_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'leagues_package'+'/'+'leagues_team_id_relevant2_s'+ '_'+ team_id +'.pkl')
    print("leagues_team_id_relevant2_s() : {}".format(round(time.time()-start_time,2))) 

# OK - No Test because a new competition can occures
def leagues_team_id_relevant3_s(team_id,game_fixture_id):
    start_time = time.time()
    team_id = str(team_id)
    array = []
    for year in range (2020,2009,-1):
        if year>start_date:
            array.append(year)
    data = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'leagues_package'+'/'+'leagues_team_id_s'+ '_'+ str(team_id) +'.pkl') 
    data1 = data.loc[data['season'].isin(array)]
    data3 = data1.loc[data1['type'] == "League"]
    data3.to_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'leagues_package'+'/'+'leagues_team_id_relevant3_s'+ '_'+ team_id +'.pkl')
    print("leagues_team_id_relevant3_s() : {}".format(round(time.time()-start_time,2))) 

# OK - Test
def leagues_season_s(team_id): # Gives all the available seasons in 2019
    start_time = time.time()
    season = str(seasons[-2]) # Only for the 2019 season
    my_file = Path(link_data+ central_folder +'/'+link_data_package_leagues_central+'/'+'leagues_season_s'+ '_'+ season +'.pkl')
    if not my_file.is_file():
        url_leagues_season = url + "leagues/season/" + season  
        response = requests.request("GET", url_leagues_season, headers=headers)   
        print("leagues_season_s + 1")
        pd.DataFrame.from_dict(json.loads(response.text)['api']['leagues']).to_pickle(link_data+ central_folder +'/'+link_data_package_leagues_central+'/'+'leagues_season_s'+ '_'+ season +'.pkl')
    print("leagues_season_s() : {}".format(round(time.time()-start_time,2))) 

# OK - Test
def leagues_league_id_master_s(exc1,exc2,exc3,exc4):
    exc1, exc2, exc3, exc4 = str(exc1), str(exc2), str(exc3), str(exc4)
    start_time = time.time()
    data_leagues = pd.read_pickle(link_data+central_folder+'/'+'other'+'/'+'leagues' +'.pkl') 
    for i in range (len(data_leagues)):
        if int(data_leagues.index[i])>start_date:
            for j in range (len(data_leagues.columns)):
                if data_leagues.columns[j] != exc1 and data_leagues.columns[j] != exc2 and data_leagues.columns[j] != exc3 and data_leagues.columns[j] != exc4:
                    league_id = int(data_leagues.iloc[i,j])
                    my_file = Path(link_data+ central_folder +'/'+link_data_package_leagues_central+'/'+'leagues_league_id_master_s'+ '_'+ str(league_id) +'.pkl')
                    if not my_file.is_file() and league_id != 0:   
                        x = leagues_league_id(league_id)[1]
                        x.to_pickle(link_data+ central_folder +'/'+link_data_package_leagues_central+'/'+'leagues_league_id_master_s'+ '_'+ str(league_id) +'.pkl')
    print("leagues_league_id_master_s() : {}".format(round(time.time()-start_time,2))) 

'''
Additional functions 
------------------------------------------------------------------------------------
'''

# OK -
def leagues_league_id(league_id):
    league_id = str(league_id)
    url_leagues_league_id = url + "leagues/league/" + league_id  
    response = requests.request("GET", url_leagues_league_id, headers=headers)
    print("leagues_league_id + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['leagues']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['leagues'])
