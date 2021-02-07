# Imports 
import requests
import json
import pandas as pd  
import numpy as np
from pathlib import Path
import time

from parameters_package import *
from core_functions import * # For nan_to_zero function
from teams_package import * # For nan_to_zero function

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
def events_fixture_id(fixture_id): 
    fixture_id = str(fixture_id)
    url_events = url + "events/" + fixture_id 
    response = requests.request("GET", url_events, headers=headers)
    print("events_fixture_id + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['events']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['events'])

# OK - Test
def events_fixture_id_s(team_id,k,game_fixture_id): 
    start_time = time.time()
    data = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_last_s'+ '_'+ str(team_id) + '_'+ str(last) +'.pkl') 

    for i in range (len(data)):
        try :
            fixture_id = data.iloc[i,data.columns.get_loc('fixture_id')]
            my_file = Path(link_data+central_folder+'/'+link_data_package_events_central+'/'+'events_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
            if not my_file.is_file() or (my_file.is_file() and int(data.iloc[i,data.columns.get_loc('event_timestamp')])>int(start_time_update) and int(data.iloc[i,data.columns.get_loc('event_timestamp')])<int(now_time) and len(pd.read_pickle(link_data+central_folder+'/'+link_data_package_events_central+'/'+'events_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')) == 0):   
                x = events_fixture_id(fixture_id)[1]
                x.to_pickle(link_data+central_folder+'/'+link_data_package_events_central+'/'+'events_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
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
            if i<last+5: # 5 is a buffer
                try :
                    fixture_id = data2.iloc[i,data2.columns.get_loc('fixture_id')]
                    my_file = Path(link_data+central_folder+'/'+link_data_package_events_central+'/'+'events_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
                    if not my_file.is_file() or (my_file.is_file() and int(data2.iloc[i,data2.columns.get_loc('event_timestamp')])>int(start_time_update) and int(data2.iloc[i,data2.columns.get_loc('event_timestamp')])<int(now_time) and len(pd.read_pickle(link_data+central_folder+'/'+link_data_package_events_central+'/'+'events_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')) == 0):   
                        x = events_fixture_id(fixture_id)[1]
                        x.to_pickle(link_data+central_folder+'/'+link_data_package_events_central+'/'+'events_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
                except:
                    print("Error with {}".format(i))   

        data3 = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_identical_season_s'+ '_'+ str(seasons[-2]) + '.pkl')
        for i in range (len(data3)):
            try:
                fixture_id = data3.iloc[i,data3.columns.get_loc('fixture_id')]
                my_file = Path(link_data+central_folder+'/'+link_data_package_events_central+'/'+'events_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
                if not my_file.is_file() or (my_file.is_file() and int(data3.iloc[i,data3.columns.get_loc('event_timestamp')])>int(start_time_update) and int(data3.iloc[i,data3.columns.get_loc('event_timestamp')])<int(now_time) and len(pd.read_pickle(link_data+central_folder+'/'+link_data_package_events_central+'/'+'events_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')) == 0):   
                    x = events_fixture_id(fixture_id)[1]
                    x.to_pickle(link_data+central_folder+'/'+link_data_package_events_central+'/'+'events_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
            except:
                print("Error with {}".format(i)) 

    print("events_fixture_id_s() : {}".format(round(time.time()-start_time,2))) 

'''
Output Functions 
------------------------------------------------------------------------------------
'''



# OK -
def output_number_event_pre_event_strict_3_events(team_id,fixture_id,team_id_A,event_type_A,detail_event_type_A,team_id_B,event_type_B,detail_event_type_B,team_id_C,event_type_C,detail_event_type_C,team_id_D,event_type_D,detail_event_type_D):
    df = pd.read_pickle(link_data+central_folder+'/'+link_data_package_events_central+'/'+'events_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
    a = nan_to_zero(df,'elapsed_plus')
    elapsed_event_type_B = []
    number_event_type_A = 0
    
    for i in a.index:
        if (a.iloc[i,a.columns.get_loc('type')] == event_type_B \
            and a.iloc[i,a.columns.get_loc('detail')] == detail_event_type_B and a.iloc[i,a.columns.get_loc('team_id')] == team_id_B) or (a.iloc[i,a.columns.get_loc('type')] == event_type_C \
            and a.iloc[i,a.columns.get_loc('detail')] == detail_event_type_C and a.iloc[i,a.columns.get_loc('team_id')] == team_id_C) or ((a.iloc[i,a.columns.get_loc('type')] == event_type_D \
            and a.iloc[i,a.columns.get_loc('detail')] == detail_event_type_D and a.iloc[i,a.columns.get_loc('team_id')] == team_id_D)):

            elapsed_event_type_B.append(int(a.iloc[i,a.columns.get_loc('elapsed')])+int(a.iloc[i,a.columns.get_loc('elapsed_plus')]))
  
    if elapsed_event_type_B == []:
        elapsed_event_type_B.append(1000)

    for j in a.index:
        if a.iloc[j,a.columns.get_loc('type')] == event_type_A \
            and a.iloc[j,a.columns.get_loc('detail')] == detail_event_type_A \
            and (int(a.iloc[j,a.columns.get_loc('elapsed')])+int(a.iloc[j,a.columns.get_loc('elapsed_plus')]))<int(elapsed_event_type_B[0]) and a.iloc[j,a.columns.get_loc('team_id')] == team_id_A and a.iloc[j,a.columns.get_loc('detail')] != 'Missed Penalty':
            number_event_type_A += 1
    return number_event_type_A

# OK -
def output_number_event_pre_event_strict(team_id,fixture_id,team_id_A,event_type_A,detail_event_type_A,team_id_B,event_type_B,detail_event_type_B):
    df = pd.read_pickle(link_data+central_folder+'/'+link_data_package_events_central+'/'+'events_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
    a = nan_to_zero(df,'elapsed_plus')
    elapsed_event_type_B = []
    number_event_type_A = 0
    
    for i in a.index:
        if a.iloc[i,a.columns.get_loc('type')] == event_type_B \
            and a.iloc[i,a.columns.get_loc('detail')] == detail_event_type_B and a.iloc[i,a.columns.get_loc('team_id')] == team_id_B:
            elapsed_event_type_B.append(int(a.iloc[i,a.columns.get_loc('elapsed')])+int(a.iloc[i,a.columns.get_loc('elapsed_plus')]))
  
    if elapsed_event_type_B == []:
        elapsed_event_type_B.append(1000)

    for j in a.index:
        if a.iloc[j,a.columns.get_loc('type')] == event_type_A \
            and a.iloc[j,a.columns.get_loc('detail')] == detail_event_type_A \
            and (int(a.iloc[j,a.columns.get_loc('elapsed')])+int(a.iloc[j,a.columns.get_loc('elapsed_plus')]))<int(elapsed_event_type_B[0]) and a.iloc[j,a.columns.get_loc('team_id')] == team_id_A and a.iloc[j,a.columns.get_loc('detail')] != 'Missed Penalty':
            number_event_type_A += 1
    return number_event_type_A

# OK -
def output_number_event_pre_event_soft(team_id,fixture_id,team_id_A,event_type_A,team_id_B,event_type_B,detail_event_type_B):
    df = pd.read_pickle(link_data+central_folder+'/'+link_data_package_events_central+'/'+'events_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
    a = nan_to_zero(df,'elapsed_plus')
    elapsed_event_type_B = []
    number_event_type_A = 0
    
    for i in a.index:
        if a.iloc[i,a.columns.get_loc('type')] == event_type_B \
            and a.iloc[i,a.columns.get_loc('detail')] == detail_event_type_B and a.iloc[i,a.columns.get_loc('team_id')] == team_id_B:
            
            elapsed_event_type_B.append(int(a.iloc[i,a.columns.get_loc('elapsed')])+int(a.iloc[i,a.columns.get_loc('elapsed_plus')]))
  
    if elapsed_event_type_B == []:
        elapsed_event_type_B.append(1000)

    for j in a.index:
        if a.iloc[j,a.columns.get_loc('type')] == event_type_A \
            and (int(a.iloc[j,a.columns.get_loc('elapsed')])+int(a.iloc[j,a.columns.get_loc('elapsed_plus')]))<int(elapsed_event_type_B[0]) and a.iloc[j,a.columns.get_loc('team_id')] == team_id_A and a.iloc[j,a.columns.get_loc('detail')] != 'Missed Penalty':
            number_event_type_A += 1
    return number_event_type_A

# OK - 
def output_number_goals_subs(team_id,team_id_var,fixture_id,league_id,team_name,opp_name):
    #try: 
        #variable_teams = pd.read_pickle(link_data+central_folder+'/'+link_data_package_teams_central+'/' +'teams_league_id_s'+ '_'+ str(league_id)+'.pkl') # The list of teams within a given legue
        #team_name = str(variable_teams.loc[variable_teams['team_id'] == team_id_var].iloc[0,variable_teams.loc[variable_teams['team_id'] == team_id_var].columns.get_loc('name')])
    #except:
        #team_name = output_name(team_id_var) 
    team_name = str(team_name)
    player = 0
    df = pd.read_pickle(link_data+central_folder+'/'+link_data_package_events_central+'/'+'events_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
    a = nan_to_zero(df,'elapsed_plus')
    subs = pd.read_pickle(link_data+central_folder+'/'+link_data_package_lineups_central+'/'+'lineups_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')[team_name]['substitutes']
    number = 0
    condition = 0
    for i in a.index:  
        condition = 0 
        if a.iloc[i,a.columns.get_loc('type')] == "Goal" and a.iloc[i,a.columns.get_loc('team_id')] == team_id_var and a.iloc[i,a.columns.get_loc('detail')] != 'Missed Penalty':
            player = int(a.iloc[i,a.columns.get_loc('player_id')] )
            for p in subs:
                if int(p['player_id']) == player:
                    condition = 1
        number += condition
    return number

# OK -
def output_number_assists_subs(team_id,team_id_var,fixture_id,league_id,team_name,opp_name):
    #try:
        #variable_teams = pd.read_pickle(link_data+central_folder+'/'+link_data_package_teams_central+'/' +'teams_league_id_s'+ '_'+ str(league_id)+'.pkl') # The list of teams within a given legue
        #team_name = str(variable_teams.loc[variable_teams['team_id'] == team_id_var].iloc[0,variable_teams.loc[variable_teams['team_id'] == team_id_var].columns.get_loc('name')])
    #except:
        #team_name = output_name(team_id_var) 
    team_name = str(team_name)
    player = 0
    df = pd.read_pickle(link_data+central_folder+'/'+link_data_package_events_central+'/'+'events_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
    a = nan_to_zero(df,'elapsed_plus')
    subs = pd.read_pickle(link_data+central_folder+'/'+link_data_package_lineups_central+'/'+'lineups_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')[team_name]['substitutes']
    number = 0
    condition = 0

    for i in a.index:  
        condition = 0 
        if a.iloc[i,a.columns.get_loc('type')] == "Goal" and a.iloc[i,a.columns.get_loc('team_id')] == team_id_var and a.iloc[i,a.columns.get_loc('detail')] != 'Missed Penalty':
            try:
                player = int(a.iloc[i,a.columns.get_loc('assist_id')] )
                for p in subs:
                    if int(p['player_id']) == player:
                        condition = 1
                number += condition
            except: 
                condition = 0
    return number

# OK - 
def output_number_goals_X_Y_mins(team_id,team_id_var,X,Y,fixture_id):
    df = pd.read_pickle(link_data+central_folder+'/'+link_data_package_events_central+'/'+'events_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
    a = nan_to_zero(df,'elapsed_plus')
    X,Y = int(X), int(Y)
    number = 0
    for i in a.index:  
        if a.iloc[i,a.columns.get_loc('type')] == "Goal" and a.iloc[i,a.columns.get_loc('team_id')] == team_id_var and a.iloc[i,a.columns.get_loc('detail')] != 'Missed Penalty' and int(a.iloc[i,a.columns.get_loc('elapsed')])+int(a.iloc[i,a.columns.get_loc('elapsed_plus')]) > X and int(a.iloc[i,a.columns.get_loc('elapsed')])+int(a.iloc[i,a.columns.get_loc('elapsed_plus')]) < Y :
            number += 1
    return number

# OK - 
def output_first_goal(team_id,fixture_id): # Returns id of first team scoring + time of first goal
    df = pd.read_pickle(link_data+central_folder+'/'+link_data_package_events_central+'/'+'events_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
    a = nan_to_zero(df,'elapsed_plus')
    i = 0
    while i<len(a) and a.iloc[i,a.columns.get_loc('type')] != 'Goal' and a.iloc[i,a.columns.get_loc('detail')] != 'Missed Penalty':
        i += 1
    if i == len(a):
        return 0,0
    else:
        return a.iloc[i,a.columns.get_loc('team_id')],int(a.iloc[i,a.columns.get_loc('elapsed')]+a.iloc[i,a.columns.get_loc('elapsed_plus')])
# OK -
def output_direct_goals(team_id,team_id_var,fixture_id): # Returns the number of direct goasl by a team in a game
    df = pd.read_pickle(link_data+central_folder+'/'+link_data_package_events_central+'/'+'events_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
    a = nan_to_zero(df,'elapsed_plus')
    goals = 0
    for i in range (len(a)) :
        if a.iloc[i,a.columns.get_loc('type')] == 'Goal' and a.iloc[i,a.columns.get_loc('detail')] != 'Missed Penalty' and type(a.iloc[i,a.columns.get_loc('assist')]) == type(None) and a.iloc[i,a.columns.get_loc('team_id')] == team_id_var:
            goals += 1
    return goals

# OK -
def output_csc(team_id,team_id_var,fixture_id,player_id): # Returns the number own goals in favor of team_id 
    df = pd.read_pickle(link_data+central_folder+'/'+link_data_package_events_central+'/'+'events_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
    a = nan_to_zero(df,'elapsed_plus')
    player_id = int(player_id)
    goals, goals_player = 0,0
    for i in range (len(a)) :
        if a.iloc[i,a.columns.get_loc('type')] == 'Goal' and a.iloc[i,a.columns.get_loc('detail')] == 'Own Goal'  and a.iloc[i,a.columns.get_loc('team_id')] == team_id_var :
            goals += 1
    for i in range (len(a)) :
        if a.iloc[i,a.columns.get_loc('type')] == 'Goal' and a.iloc[i,a.columns.get_loc('detail')] == 'Own Goal'  and a.iloc[i,a.columns.get_loc('player_id')] == player_id :
            goals_player += 1
    return goals, goals_player

# OK - 
def output_red_cards_commited(team_id,team_id_var,fixture_id,player_id): # Returns the number of red cards for a player in a game
    df = pd.read_pickle(link_data+central_folder+'/'+link_data_package_events_central+'/'+'events_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
    a = nan_to_zero(df,'elapsed_plus')
    cards = 0
    for i in range (len(a)) :
        try:
            if a.iloc[i,a.columns.get_loc('type')] == 'Card' and a.iloc[i,a.columns.get_loc('detail')] == 'Red Card'  and a.iloc[i,a.columns.get_loc('team_id')] == team_id_var and int(a.iloc[i,a.columns.get_loc('player_id')]) == player_id:
                cards += 1
        except: 
            print("Error in player_id for fixture_id :{}, player_id {}, comments: {}".format(fixture_id,a.iloc[i,a.columns.get_loc('comments')],a.iloc[i,a.columns.get_loc('player')]))
    return cards

# OK -
def output_yellow_cards_commited(team_id,team_id_var,fixture_id,player_id): # Returns the number of yellow cards for a player in a game 
    df = pd.read_pickle(link_data+central_folder+'/'+link_data_package_events_central+'/'+'events_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
    a = nan_to_zero(df,'elapsed_plus')
    cards = 0
    for i in range (len(a)) :
        try :
            if a.iloc[i,a.columns.get_loc('type')] == 'Card' and a.iloc[i,a.columns.get_loc('detail')] == 'Yellow Card'  and a.iloc[i,a.columns.get_loc('team_id')] == team_id_var and int(a.iloc[i,a.columns.get_loc('player_id')]) == player_id:
                cards += 1
        except:
            print("Error in player_id for fixture_id :{}, player_id {}, comments: {}".format(fixture_id,a.iloc[i,a.columns.get_loc('comments')],a.iloc[i,a.columns.get_loc('player')]))
    return cards

# OK - 
def output_penalty_commited(team_id,team_id_var,fixture_id): # Returns the number of red cards for a player in a game
    df = pd.read_pickle(link_data+central_folder+'/'+link_data_package_events_central+'/'+'events_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
    a = nan_to_zero(df,'elapsed_plus')
    penalty = 0
    for i in range (len(a)) :
        try:
            if a.iloc[i,a.columns.get_loc('type')] == 'Goal' and (a.iloc[i,a.columns.get_loc('detail')] == 'Penalty' or a.iloc[i,a.columns.get_loc('detail')] == 'Missed Penalty') and a.iloc[i,a.columns.get_loc('team_id')] != team_id_var :
                penalty += 1
        except: 
            print("Error in player_id for fixture_id :{}".format(fixture_id))
    return penalty