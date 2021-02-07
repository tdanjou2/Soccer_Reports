# Imports
import requests
import json
import pandas as pd
import numpy as np
from pathlib import Path
import time

from parameters_package import *
from core_functions import *  # For nan_to_zero function

'''
Package parameters
------------------------------------------------------------------------------------
'''


'''
Functions 
------------------------------------------------------------------------------------
'''

# Need to get intermediary calculations

# Fixtures statistics

# OK -
def statistics_fixture_id(fixture_id):
    fixture_id = str(fixture_id)
    url_statistics = url + "statistics/fixture/" + fixture_id
    response = requests.request("GET", url_statistics, headers=headers)
    print("statistics_fixture_id + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['statistics']).columns), pd.DataFrame.from_dict(json.loads(response.text)['api']['statistics'])

# OK - Test
def statistics_fixture_id_s(team_id,k,game_fixture_id):
    start_time = time.time()
    data = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package' +'/'+'fixtures_team_id_last_s' + '_' + str(team_id)+'_' + str(last)+'.pkl')
    next_id = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_next_s'+ '_'+ str(team_id) + '_'+ str(nex) + '.pkl')
    
    for i in range(len(data)):
        try:
            fixture_id = data.iloc[i, data.columns.get_loc('fixture_id')]
            my_file = Path(link_data+central_folder+'/'+link_data_package_statitics_central+'/'+'statistics_fixture_id_s'+'_' + str(fixture_id)+'.pkl')
            if not my_file.is_file() or (my_file.is_file() and int(data.iloc[i,data.columns.get_loc('event_timestamp')])>int(start_time_update) and int(data.iloc[i,data.columns.get_loc('event_timestamp')])<int(now_time) and len(pd.read_pickle(link_data+central_folder+'/'+link_data_package_statitics_central+'/'+'statistics_fixture_id_s'+'_' + str(fixture_id)+'.pkl')) == 0):
                x = statistics_fixture_id(fixture_id)[1]
                x.to_pickle(link_data+central_folder+'/'+link_data_package_statitics_central+'/'+'statistics_fixture_id_s'+'_' + str(fixture_id)+'.pkl')
        except:
            print("Error with {}".format(i))

    if k==1:
        if int(next_id.iloc[0,next_id.columns.get_loc("homeTeam")]['team_id']) == team_id:
            next_id = int(next_id.iloc[0,next_id.columns.get_loc("awayTeam")]['team_id'])
        else:
            next_id = int(next_id.iloc[0,next_id.columns.get_loc("homeTeam")]['team_id'])
        data2 = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_h2h_team_id_team_id_next_s'+ '_'+ str(team_id) + '_'+ str(next_id) + '.pkl') 

        for i in range(len(data2)):
            if i<last+5:    
                try:
                    fixture_id = data2.iloc[i,data2.columns.get_loc('fixture_id')]
                    my_file = Path(link_data+central_folder+'/'+link_data_package_statitics_central+'/'+'statistics_fixture_id_s'+'_' + str(fixture_id)+'.pkl')
                    if not my_file.is_file() or (my_file.is_file() and int(data2.iloc[i,data2.columns.get_loc('event_timestamp')])>int(start_time_update) and int(data2.iloc[i,data2.columns.get_loc('event_timestamp')])<int(now_time) and  len(pd.read_pickle(link_data+central_folder+'/'+link_data_package_statitics_central+'/'+'statistics_fixture_id_s'+'_' + str(fixture_id)+'.pkl')) == 0):
                        x = statistics_fixture_id(fixture_id)[1]
                        x.to_pickle(link_data+central_folder+'/'+link_data_package_statitics_central+'/'+'statistics_fixture_id_s'+'_' + str(fixture_id)+'.pkl')
                except:
                    print("Error with {}".format(i))

        data3 = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_identical_season_s'+ '_'+ str(seasons[-2]) + '.pkl')
        for i in range (len(data3)):
            try:
                fixture_id = data3.iloc[i,data3.columns.get_loc('fixture_id')]
                my_file = Path(link_data+central_folder+'/'+link_data_package_statitics_central+'/'+'statistics_fixture_id_s'+'_' + str(fixture_id)+'.pkl')
                if not my_file.is_file() or (my_file.is_file() and int(data3.iloc[i,data3.columns.get_loc('event_timestamp')])>int(start_time_update) and int(data3.iloc[i,data3.columns.get_loc('event_timestamp')])<int(now_time) and len(pd.read_pickle(link_data+central_folder+'/'+link_data_package_statitics_central+'/'+'statistics_fixture_id_s'+'_' + str(fixture_id)+'.pkl')) == 0):   
                    x = statistics_fixture_id(fixture_id)[1]
                    x.to_pickle(link_data+central_folder+'/'+link_data_package_statitics_central+'/'+'statistics_fixture_id_s'+'_' + str(fixture_id)+'.pkl')
            except:
                print("Error with {}".format(i))

    print("statistics_fixture_id_s() : {}".format(round(time.time()-start_time, 2)))


# Teams statistics

# OK -
def statistics_team_id_league_id(team_id, league_id):
    league_id, team_id = str(league_id), str(team_id)
    url_statistics_team_id_league_id = url + "statistics/" + league_id + "/" + team_id
    response = requests.request("GET", url_statistics_team_id_league_id, headers=headers)
    print("statistics_team_id_league_id + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['statistics']).columns), pd.DataFrame.from_dict(json.loads(response.text)['api']['statistics'])

# OK - No Test 
def statistics_team_id_league_id_s(team_id,game_fixture_id):
    start_time = time.time()
    data = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'leagues_package' +'/' +'leagues_team_id_relevant_s' + '_' + str(team_id) + '.pkl')
    for i in range(len(data)):
        league_id = data.iloc[i, data.columns.get_loc('league_id')]
        data_2 = pd.read_pickle(link_data+central_folder+'/'+link_data_package_teams_central+'/'+'teams_league_id_s'+ '_'+ str(league_id) + '.pkl')
        for j in range (len(data_2)):
            team_id_2 = data_2.iloc[j,data_2.columns.get_loc('team_id')]    
            try:
                x = statistics_team_id_league_id(team_id_2, league_id)[1]
                x.to_pickle(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' +'statistics_package'+ '/' +'statistics_team_id_league_id_s' + '_' + str(team_id_2) + '_' + str(league_id)+'.pkl')
            except:
                print("Error with {},{}".format(i,j))
    print("statistics_team_id_league_id_s() : {}".format(
        round(time.time()-start_time, 2)))

