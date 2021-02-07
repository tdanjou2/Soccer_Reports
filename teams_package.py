# Imports
import requests
import json
import pandas as pd  
import numpy as np
from pathlib import Path
import time
import os
import os.path

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
def teams_team_id(team_id):
    team_id= str(team_id)
    url_teams_team_id = url + "teams/team/" + team_id 
    response = requests.request("GET", url_teams_team_id, headers=headers)
    print("teams_team_id + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['teams']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['teams'])

# OK 
def teams_league_id(league_id):
    league_id= str(league_id)
    url_teams_league_id = url + "teams/league/" + league_id 
    response = requests.request("GET", url_teams_league_id, headers=headers)
    print("teams_league_id + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['teams']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['teams'])

# OK - Test
def teams_league_id_s(team_id,k,game_fixture_id):
    start_time = time.time()
    data = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'leagues_package'+'/'+'leagues_team_id_relevant_s'+ '_'+ str(team_id) +'.pkl') 
    for i in range (len(data)):
        try:
            league_id = data.iloc[i,data.columns.get_loc('league_id')]
            my_file = Path(link_data+central_folder+'/'+link_data_package_teams_central+'/'+'teams_league_id_s'+ '_'+ str(league_id) + '.pkl')
            if not my_file.is_file():   
                x = teams_league_id(league_id)[1]                
                x.to_pickle(link_data+central_folder+'/'+link_data_package_teams_central+'/'+'teams_league_id_s'+ '_'+ str(league_id) + '.pkl')
        except Exception as e:
            print(e)
    
    if k ==1:
        # This is for option 2
        next_id = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_next_s'+ '_'+ str(team_id) + '_'+ str(nex) + '.pkl')
        if int(next_id.iloc[0,next_id.columns.get_loc("homeTeam")]['team_id']) == team_id:
            next_id = int(next_id.iloc[0,next_id.columns.get_loc("awayTeam")]['team_id'])
        else:
            next_id = int(next_id.iloc[0,next_id.columns.get_loc("homeTeam")]['team_id'])
        
        data2 = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_h2h_team_id_team_id_next_s'+ '_'+ str(team_id) + '_'+ str(next_id) + '.pkl') 
        for i in range (len(data2)):
            try:
                league_id = data2.iloc[i,data2.columns.get_loc('league_id')]
                data_league = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'leagues_package'+'/'+'leagues_team_id_relevant3_s'+ '_'+ str(team_id) +'.pkl') 
                if len(data_league.loc[data_league['league_id'] == league_id])>0:
                    my_file = Path(link_data+central_folder+'/'+link_data_package_teams_central+'/'+'teams_league_id_s'+ '_'+ str(league_id) + '.pkl')
                    if not my_file.is_file():   
                        x = teams_league_id(league_id)[1]
                        x.to_pickle(link_data+central_folder+'/'+link_data_package_teams_central+'/'+'teams_league_id_s'+ '_'+ str(league_id) + '.pkl')
            except:
                print("Error with {}".format(i))

        # This is for option 3
        data3 = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_identical_season_s'+ '_'+ str(seasons[-2]) + '.pkl')
        for i in range (len(data3)):
            try:
                league_id = data3.iloc[i,data3.columns.get_loc('league_id')]
                data_league = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'leagues_package'+'/'+'leagues_team_id_relevant3_s'+ '_'+ str(team_id) +'.pkl') 
                if len(data_league.loc[data_league['league_id'] == league_id])>0:
                    my_file = Path(link_data+central_folder+'/'+link_data_package_teams_central+'/'+'teams_league_id_s'+ '_'+ str(league_id) + '.pkl')
                    if not my_file.is_file():   
                        x = teams_league_id(league_id)[1]
                        x.to_pickle(link_data+central_folder+'/'+link_data_package_teams_central+'/'+'teams_league_id_s'+ '_'+ str(league_id) + '.pkl')
            except:
                print("Error with {}".format(i))
    print("teams_league_id_s() : {}".format(round(time.time()-start_time,2))) 

# OK - Test
def teams_league_id_master_s(exc1,exc2,exc3,exc4):
    exc1, exc2, exc3, exc4 = str(exc1), str(exc2), str(exc3), str(exc4)
    start_time = time.time()
    data_leagues = pd.read_pickle(link_data+central_folder+'/'+'other'+'/'+'leagues' +'.pkl') 
    for i in range (len(data_leagues)):
        if int(data_leagues.index[i])>start_date:
            for j in range (len(data_leagues.columns)):
                if data_leagues.columns[j] != exc1 and data_leagues.columns[j] != exc2 and data_leagues.columns[j] != exc3 and data_leagues.columns[j] != exc4:
                    league_id = int(data_leagues.iloc[i,j])
                    my_file = Path(link_data+central_folder+'/'+link_data_package_teams_central+'/'+'teams_league_id_s'+ '_'+ str(league_id) + '.pkl')
                    if not my_file.is_file():   
                        x = teams_league_id(league_id)[1]
                        x.to_pickle(link_data+central_folder+'/'+link_data_package_teams_central+'/'+'teams_league_id_s'+ '_'+ str(league_id) + '.pkl')
    print("teams_league_id_master_s() : {}".format(round(time.time()-start_time,2))) 


# OK - Test
def teams_logo_team_id_s(team_id):
    for teams in list(pd.read_pickle(link_data+central_folder+'/'+'other'+'/'+'leagues' +'.pkl')[:][-1:].iloc[0]):
        try:    
            link = link_data + str(central_folder) +'/'+ "teams_package"+'/'+"teams_league_id_s_" + str(int(teams))+ '.pkl'
            for i in range(len(pd.read_pickle(link))):
                team_id = int(pd.read_pickle(link).iloc[i,pd.read_pickle(link).columns.get_loc('team_id')])
                logo_id = str(pd.read_pickle(link).iloc[i,pd.read_pickle(link).columns.get_loc('logo')])
                if not os.path.exists(link_reports + str(central_folder) +'/'+ "other"+'/'+'logo_'+str(team_id)+'.png'):
                    response = requests.get(logo_id)
                    file = open(link_reports + str(central_folder) +'/'+ "other"+'/'+'logo_'+str(team_id)+'.png', "wb")
                    file.write(response.content)
                    file.close()
        except:
            print(teams)

# OK - Test
def logo_team_id_s(team_id):
    logo_id = str(teams_team_id(team_id)[1].iloc[0,teams_team_id(team_id)[1].columns.get_loc(("logo"))])
    if not os.path.exists(link_reports + str(central_folder) +'/'+ "other"+'/'+'logo_'+str(team_id)+'.png'):
        response = requests.get(logo_id)
        file = open(link_reports + str(central_folder) +'/'+ "other"+'/'+'logo_'+str(team_id)+'.png', "wb")
        file.write(response.content)
        file.close()
    print(team_id)

'''
Additional functions 
------------------------------------------------------------------------------------
'''

# OK - Test 
def output_name(team_id):
    return teams_team_id(team_id)[1]['name'][0]
