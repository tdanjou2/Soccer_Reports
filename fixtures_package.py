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

# NO need to get intermediary calculations

# OK - No Test
def fixtures_fixture_id(fixture_id):
    fixture_id = str(fixture_id)
    url_fixtures_fixture_id = url + "fixtures/id/" + fixture_id 
    response = requests.request("GET", url_fixtures_fixture_id, headers=headers)
    print("fixtures_fixture_id + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures'])

# OK - No Test
def fixtures_team_id_s(team_id,game_fixture_id):
    start_time = time.time()
    team_id = str(team_id)
    url_fixtures_team = url + "fixtures/team/" + team_id 
    response = requests.request("GET", url_fixtures_team, headers=headers)
    print("fixtures_team_id_s + 1")
    pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures']).to_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_s'+ '_'+ team_id +'.pkl')
    print("fixtures_team_id_s() : {}".format(round(time.time()-start_time,2))) 
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures'])

def fixtures_team_id_modified_s(team_id_1,team_id_2,game_fixture_id):
    team_id_1 , team_id_2 = str(team_id_1),str(team_id_2)
    url_fixtures_team = url + "fixtures/team/" + team_id_2 
    response = requests.request("GET", url_fixtures_team, headers=headers)
    print("fixtures_team_id_modified_s + 1")
    pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures']).to_pickle(link_data+'{}'.format(team_id_1)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_s'+ '_'+ team_id_2 +'.pkl')
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures'])


# OK - No Test 
def fixtures_team_id_last(team_id,last):    
    last,team_id = str(last),str(team_id)
    url_fixtures_team_last = url + "fixtures/team/" + team_id + '/last/' + last
    response = requests.request("GET", url_fixtures_team_last, headers=headers)
    print("fixtures_team_id_last + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures'])

# OK - No Test 
def fixtures_team_id_next(team_id,nex):    
    nex,team_id = str(nex),str(team_id)
    url_fixtures_team_next = url + "fixtures/team/" + team_id + '/next/' + nex
    response = requests.request("GET", url_fixtures_team_next, headers=headers)
    print("fixtures_team_id_next + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures'])

# OK - No Test 
def fixtures_team_id_last_s(team_id,last,game_fixture_id):    
    start_time = time.time()
    last,team_id = str(last),str(team_id)
    url_fixtures_team_last = url + "fixtures/team/" + team_id + '/last/' + last
    response = requests.request("GET", url_fixtures_team_last, headers=headers)
    print("fixtures_team_id_last_s + 1")
    pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures']).to_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_last_s'+ '_'+ team_id +'_'+ last +'.pkl')
    print("fixtures_team_id_last_s() : {}".format(round(time.time()-start_time,2))) 
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures'])

# OK - No Test
def fixtures_team_id_next_s(team_id,nex,game_fixture_id):    
    start_time = time.time()
    nex,team_id = str(nex),str(team_id)
    url_fixtures_team_next = url + "fixtures/team/" + team_id + '/next/' + nex
    response = requests.request("GET", url_fixtures_team_next, headers=headers)  
    print("fixtures_team_id_next_s + 1")
    pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures']).to_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_next_s'+ '_'+ team_id +'_'+ nex +'.pkl')
    print("fixtures_team_id_next_s() : {}".format(round(time.time()-start_time,2))) 
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures'])


# Need to get intermediary calculations

# OK -
def fixtures_league_id(league_id):   
    league_id = str(league_id)
    url_fixtures_league = url + "fixtures/league/" + league_id
    response = requests.request("GET", url_fixtures_league, headers=headers)
    print("fixtures_league_id + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures'])

# OK - Test light
def fixtures_league_id_s(team_id,game_fixture_id):  
    start_time = time.time()
    data = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'leagues_package'+'/'+'leagues_team_id_relevant2_s'+ '_'+ str(team_id) +'.pkl') 
    for i in range (len(data)):
        try:
            league_id = data.iloc[i,data.columns.get_loc('league_id')]
            season = data.iloc[i,data.columns.get_loc('season')]
            my_file = Path(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_league_id_last_s'+ '_'+ str(league_id) + '_'+ str(last) + '.pkl')
            if not my_file.is_file() or int(season) == int(seasons[-1]):   
                x = fixtures_league_id(league_id)[1]
                x.to_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_league_id_s'+ '_'+ str(league_id) + '.pkl')
        except Exception as e:
            print(i,e)
    print("fixtures_league_id_s() : {}".format(round(time.time()-start_time,2))) 

# OK -
def fixtures_league_id_last(league_id,last):    
    last,league_id = str(last),str(league_id)
    url_fixtures_league_last = url + "fixtures/league/" + league_id + '/last/' + last
    response = requests.request("GET", url_fixtures_league_last, headers=headers)
    print("fixtures_league_id_last + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures'])

# OK - No Test
def fixtures_league_id_last_s(team_id,last,game_fixture_id):  
    start_time = time.time()
    data = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'leagues_package'+'/'+'leagues_team_id_relevant_s'+ '_'+ str(team_id) +'.pkl') 
    for i in range (len(data)):
        try:
            league_id = data.iloc[i,data.columns.get_loc('league_id')]   
            x = fixtures_league_id_last(league_id,last)[1]
            x.to_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_league_id_last_s'+ '_'+ str(league_id) + '_'+ str(last) + '.pkl')
        except Exception as e:
            print(i,e)
    print("fixtures_league_id_last_s() : {}".format(round(time.time()-start_time,2))) 

# OK -
def fixtures_league_id_next(league_id,nex):    
    nex,league_id = str(nex),str(league_id)
    url_fixtures_league_next = url + "fixtures/league/" + league_id + '/next/' + nex
    response = requests.request("GET", url_fixtures_league_next, headers=headers)
    print("fixtures_league_id_next + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures'])

# OK - No Test
def fixtures_league_id_next_s(team_id,nex,game_fixture_id):  
    start_time = time.time()
    data = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'leagues_package'+'/'+'leagues_team_id_relevant_s'+ '_'+ str(team_id) +'.pkl') 
    for i in range (len(data)):
        try:
            league_id = data.iloc[i,data.columns.get_loc('league_id')]
            x = fixtures_league_id_next(league_id,nex)[1]
            x.to_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_league_id_next_s'+ '_'+ str(league_id) + '_'+ str(nex) + '.pkl')
        except Exception as e:
            print(i,e)
    print("fixtures_league_id_next_s() : {}".format(round(time.time()-start_time,2))) 

# OK -
def fixtures_h2h_team_id_team_id(team_id_1,team_id_2):   
    team_id_1,team_id_2 = str(team_id_1),str(team_id_2)
    url_fixtures_h2h_team_id_team_id= url + "fixtures/h2h/" + team_id_1 + "/" + team_id_2
    response = requests.request("GET", url_fixtures_h2h_team_id_team_id, headers=headers)
    print("fixtures_h2h_team_id_team_id + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures'])

# OK - No Test
def fixtures_h2h_team_id_team_id_s(team_id,last,nex,game_fixture_id):   
    start_time = time.time()
    data_last = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_last_s'+ '_'+ str(team_id) +'_' + str(last) +'.pkl') 
    data_next = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_next_s'+ '_'+ str(team_id) +'_' + str(nex) +'.pkl') 
    for i in range (len(data_last)):
        try:
            team_id_1 = data_last.iloc[i,data_last.columns.get_loc('homeTeam')]['team_id']
            team_id_2 = data_last.iloc[i,data_last.columns.get_loc('awayTeam')]['team_id']
            x = fixtures_h2h_team_id_team_id(team_id_1,team_id_2)[1]
            x.to_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_h2h_team_id_team_id_s'+ '_'+ str(team_id_1) + '_'+ str(team_id_2) + '.pkl')
        except Exception as e:
            print(i,e)

    for i in range (len(data_next)):
        try:
            team_id_1 = data_next.iloc[i,data_next.columns.get_loc('homeTeam')]['team_id']
            team_id_2 = data_next.iloc[i,data_next.columns.get_loc('awayTeam')]['team_id']
            x = fixtures_h2h_team_id_team_id(team_id_1,team_id_2)[1]
            x.to_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_h2h_team_id_team_id_s'+ '_'+ str(team_id_1) + '_'+ str(team_id_2) + '.pkl')
        except Exception as e:
            print(i,e)
    print("fixtures_h2h_team_id_team_id_s() : {}".format(round(time.time()-start_time,2))) 

# OK - No Test
def fixtures_h2h_team_id_team_id_next_s(team_id,nex,k,game_fixture_id):   
    if k == 1:
        start_time = time.time()
        data_next = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_next_s'+ '_'+ str(team_id) +'_' + str(nex) +'.pkl') 
        try:
            team_id_1 = data_next.iloc[0,data_next.columns.get_loc('homeTeam')]['team_id']
            team_id_2 = data_next.iloc[0,data_next.columns.get_loc('awayTeam')]['team_id']
            x = fixtures_h2h_team_id_team_id(team_id_1,team_id_2)[1]
            x = x.sort_index(ascending=False)
            x = x.set_index(pd.Index([i for i in range (len(x))]))
            if int(team_id_1) == team_id:
                x.to_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_h2h_team_id_team_id_next_s'+ '_'+ str(team_id_1) + '_'+ str(team_id_2) + '.pkl')
            else:
                x.to_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_h2h_team_id_team_id_next_s'+ '_'+ str(team_id_2) + '_'+ str(team_id_1) + '.pkl')
        except:
            pass
        print("fixtures_h2h_team_id_team_id_next_s() : {}".format(round(time.time()-start_time,2))) 

# OK -
def fixturesrounds_league_id(league_id):
    league_id = str(league_id)
    url_fixturesrounds_league_id = url + "fixtures/rounds/" + league_id 
    response = requests.request("GET", url_fixturesrounds_league_id, headers=headers)
    print("fixturesrounds_league_id + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures'])

# OK - Test
def fixturesrounds_league_id_s(team_id,k,game_fixture_id):
    start_time = time.time()
    
    if k == 1:
        data = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'leagues_package'+'/'+'leagues_team_id_relevant2_s'+ '_'+ str(team_id) +'.pkl') 

    elif k == 0:
        data = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'leagues_package'+'/'+'leagues_team_id_relevant_s'+ '_'+ str(team_id) +'.pkl') 
    else:
        print("Error with k")

    for i in range (len(data)):
        try:
            league_id = data.iloc[i,data.columns.get_loc('league_id')]
            my_file = Path(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixturesrounds_league_id_s'+ '_'+ str(league_id) +'.pkl')
            if not my_file.is_file() :   
                x = fixturesrounds_league_id(league_id)[1]
                x.to_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixturesrounds_league_id_s'+ '_'+ str(league_id) +'.pkl')
        except Exception as e:
            print(i,e)
    
    # This is for option 2
    if k ==1:
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
                    my_file = Path(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixturesrounds_league_id_s'+ '_'+ str(league_id) +'.pkl')
                    if not my_file.is_file():   
                        x = fixturesrounds_league_id(league_id)[1]
                        x.to_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixturesrounds_league_id_s'+ '_'+ str(league_id) +'.pkl')
            except Exception as e:
                print(i,e)
    print("fixturesrounds_league_id_s() : {}".format(round(time.time()-start_time,2))) 

# OK - Test
def fixturesrounds_league_id_master_s(exc1,exc2,exc3,exc4):
    exc1, exc2, exc3, exc4 = str(exc1), str(exc2), str(exc3), str(exc4)
    start_time = time.time()
    data_leagues = pd.read_pickle(link_data+central_folder+'/'+'other'+'/'+'leagues' +'.pkl') 
    for i in range (len(data_leagues)):
        if int(data_leagues.index[i])>start_date:
            for j in range (len(data_leagues.columns)):
                if data_leagues.columns[j] != exc1 and data_leagues.columns[j] != exc2 and data_leagues.columns[j] != exc3 and data_leagues.columns[j] != exc4:
                    league_id = int(data_leagues.iloc[i,j])
                    my_file = Path(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixturesrounds_league_id_s'+ '_'+ str(league_id) + '.pkl')
                    if not my_file.is_file():   
                        x = fixturesrounds_league_id(league_id)[1]
                        x.to_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixturesrounds_league_id_s'+ '_'+ str(league_id) + '.pkl')
    print("fixturesrounds_league_id_master_s() : {}".format(round(time.time()-start_time,2))) 

# OK - 
def fixtures_league_id_round(league_id,rounds):
    league_id,rounds = str(league_id),str(rounds)
    url_fixtures_league_id_round = url + "fixtures/league/" + league_id + '/' + rounds
    response = requests.request("GET", url_fixtures_league_id_round, headers=headers)
    print("fixtures_league_id_round + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures'])

# OK - Test light
def fixtures_league_id_round_s(team_id,k,game_fixture_id):
    start_time = time.time()
    if k == 1:
        data_league = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'leagues_package'+'/'+'leagues_team_id_relevant2_s'+ '_'+ str(team_id) +'.pkl') 
    elif k == 0:
        data_league = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'leagues_package'+'/'+'leagues_team_id_relevant_s'+ '_'+ str(team_id) +'.pkl') 
    else:
        print("Error with k")
    
    for i in range (len(data_league)):
        try:
            league_id = data_league.iloc[i,data_league.columns.get_loc('league_id')]
            season = data_league.iloc[i,data_league.columns.get_loc('season')]
            data_rounds = pd.read_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixturesrounds_league_id_s'+ '_'+ str(league_id) +'.pkl')
            try:
                current_rounds = pd.read_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixturesrounds_league_id_current_round_s'+ '_'+ str(league_id) +'.pkl') 
            except:
                fixturesrounds_league_id_current_round_s(league_id)
                current_rounds = pd.read_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixturesrounds_league_id_current_round_s'+ '_'+ str(league_id) +'.pkl') 
            for j in range (len(data_rounds)):
                rounds = data_rounds.iloc[j,0]
                variable_path = link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixtures_league_id_round_s'+ '_'+ str(league_id) +'_' +str(rounds)+'.pkl'
                my_file = Path(variable_path)
                if not my_file.is_file():
                    x = fixtures_league_id_round(league_id,rounds)[1]
                    x.to_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixtures_league_id_round_s'+ '_'+ str(league_id) +'_' +str(rounds)+'.pkl')
                elif my_file.is_file() and not match_item_list(int(league_id),list(pd.read_pickle(link_data+central_folder+'/'+'other'+'/'+'leagues' +'.pkl')[:][-1:].iloc[0])) and int(season) == int(seasons[-1]) and j<int(data_rounds.loc[data_rounds[0] == current_rounds[0][0]].index[0])+1:
                    time_variable = os.path.getmtime(variable_path)
                    if time_variable<(datetime.timestamp(datetime.now()-timedelta(seconds=detla_seconds_update))):
                        x = fixtures_league_id_round(league_id,rounds)[1]
                        x.to_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixtures_league_id_round_s'+ '_'+ str(league_id) +'_' +str(rounds)+'.pkl')
        except Exception as e:
            print(i,e)
            
    if k==1:
        next_id = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_next_s'+ '_'+ str(team_id) + '_'+ str(nex) + '.pkl')
        if int(next_id.iloc[0,next_id.columns.get_loc("homeTeam")]['team_id']) == team_id:
            next_id = int(next_id.iloc[0,next_id.columns.get_loc("awayTeam")]['team_id'])
        else:
            next_id = int(next_id.iloc[0,next_id.columns.get_loc("homeTeam")]['team_id'])

        data2 = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_h2h_team_id_team_id_next_s'+ '_'+ str(team_id) + '_'+ str(next_id) + '.pkl')    
        for i in range (len(data2)):
            try:
                league_id = data2.iloc[i,data2.columns.get_loc('league_id')] # No need to test on the season because the current season has already been captured by the rest of the formula
                data_league = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'leagues_package'+'/'+'leagues_team_id_relevant3_s'+ '_'+ str(team_id) +'.pkl') 
                if len(data_league.loc[data_league['league_id'] == league_id])>0:
                    data_rounds = pd.read_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixturesrounds_league_id_s'+ '_'+ str(league_id) +'.pkl')
                    for j in range (len(data_rounds)):
                        rounds = data_rounds.iloc[j,0] 
                        my_file = Path(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixtures_league_id_round_s'+ '_'+ str(league_id) +'_' +str(rounds)+'.pkl')
                        if not my_file.is_file():   
                            x = fixtures_league_id_round(league_id,rounds)[1]
                            x.to_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixtures_league_id_round_s'+ '_'+ str(league_id) +'_' +str(rounds)+'.pkl')
            except Exception as e:
                print(i,e)
    print("fixtures_league_id_round_s() : {}".format(round(time.time()-start_time,2))) 

# OK - Test
def fixtures_league_id_round_master_s(exc1,exc2,exc3,exc4):
    exc1, exc2, exc3, exc4 = str(exc1), str(exc2), str(exc3), str(exc4)
    start_time = time.time()
    data_leagues = pd.read_pickle(link_data+central_folder+'/'+'other'+'/'+'leagues' +'.pkl') 
    for i in range (len(data_leagues)):
        if int(data_leagues.index[i])>start_date:
            for j in range (len(data_leagues.columns)):
                if data_leagues.columns[j] != exc1 and data_leagues.columns[j] != exc2 and data_leagues.columns[j] != exc3 and data_leagues.columns[j] != exc4:
                    league_id = int(data_leagues.iloc[i,j])
                    if league_id != 0:
                        data_league_id = pd.read_pickle(link_data+central_folder+'/'+link_data_package_leagues_central+'/'+'leagues_league_id_master_s'+ '_'+ str(league_id) +'.pkl') 
                        season = data_league_id.iloc[0,data_league_id.columns.get_loc('season')]
                        current_rounds = pd.read_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixturesrounds_league_id_current_round_s'+ '_'+ str(league_id) +'.pkl') 
                        data_rounds = pd.read_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixturesrounds_league_id_s'+ '_'+ str(league_id) +'.pkl') 
                        for k in range (len(data_rounds)):
                            rounds = data_rounds.iloc[k,0]
                            my_file = Path(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixtures_league_id_round_s'+ '_'+ str(league_id) +'_'+ str(rounds) + '.pkl')
                            if not my_file.is_file(): 
                                x = fixtures_league_id_round(league_id,rounds)[1]
                                x.to_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixtures_league_id_round_s'+ '_'+ str(league_id) +'_'+ str(rounds) + '.pkl')
                            elif my_file.is_file() and (int(season) == int(seasons[-1]) and k<int(data_rounds.loc[data_rounds[0] == current_rounds[0][0]].index[0])+1):
                                test = 0
                                data = pd.read_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixtures_league_id_round_s'+ '_'+ str(league_id) +'_'+ str(rounds) + '.pkl')
                                for cpt_3 in data['elapsed']:
                                    if int(cpt_3) != 90: # A completed game
                                        test = 1
                                if test == 1 :
                                    x = fixtures_league_id_round(league_id,rounds)[1]
                                    x.to_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixtures_league_id_round_s'+ '_'+ str(league_id) +'_'+ str(rounds) + '.pkl')
    print("fixtures_league_id_round_master_s() : {}".format(round(time.time()-start_time,2))) 

# OK -
def fixtures_list_opp_id(team_id,game_fixture_id):
    opp_list = []
    x = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_last_s'+ '_'+ str(team_id) + '_' + str(last) + '.pkl')
    for i in range (last_fixtures_lineups_duration):
        opp_id = int(x.iloc[i,x.columns.get_loc('homeTeam')]['team_id'])
        if opp_id == int(team_id):
            opp_list.append(int(x.iloc[i,x.columns.get_loc('awayTeam')]['team_id']))
        else:
            opp_list.append(int(x.iloc[i,x.columns.get_loc('homeTeam')]['team_id']))
    return opp_list

# OK - No Test
def fixtures_identical_season_s(team_id,k,game_fixture_id): 

    if k == 1:    
        start_time = time.time()
        
        next_id = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_next_s'+ '_'+ str(team_id) + '_'+ str(nex) + '.pkl')
        leagues = pd.read_pickle(link_data+central_folder+'/'+'other'+'/' + 'leagues' + '.pkl')
        leagues_list = list(leagues.iloc[-1,:-1])
        
        cpt_2 = 0
        while cpt_2<nex and not match_item_list(int(next_id.iloc[cpt_2,next_id.columns.get_loc("league_id")]),leagues_list):
            cpt_2 += 1
        q = position(int(next_id.iloc[cpt_2,next_id.columns.get_loc("league_id")]),leagues_list)
        next_round = str(next_id.iloc[cpt_2,next_id.columns.get_loc("round")])
        next_league_country = str(next_id.iloc[cpt_2,next_id.columns.get_loc("league")]['country'])
        next_league_name = str(next_id.iloc[cpt_2,next_id.columns.get_loc("league")]['name'])

        x = pd.read_pickle(link_data+ central_folder +'/'+link_data_package_leagues_central+'/'+'leagues_season_s'+ '_'+ str(seasons[-2]) + '.pkl')
        x = x.loc[x['country'] == next_league_country]
        x = x.loc[x['name'] == next_league_name]
        x = int(x.iloc[0,x.columns.get_loc('league_id')])
        
        identical_rank = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_s'+ '_'+ str(team_id) + '.pkl')

        try:
            identical_rank = identical_rank.loc[identical_rank['round'] == next_round]
            identical_rank = identical_rank.loc[identical_rank['league_id'] == x]
            identical_rank = int(identical_rank.index[0])

        except:
            if leagues.columns[q][-1] == "2" :
                x = leagues.iloc[-2,q-1]
            else:
                x = leagues.iloc[-2,q+1]
            
            identical_rank = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_s'+ '_'+ str(team_id) + '.pkl')
            identical_rank = identical_rank.loc[identical_rank['round'] == next_round]
            identical_rank = identical_rank.loc[identical_rank['league_id'] == x]
            identical_rank = int(identical_rank.index[0])

        data3 = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_s'+ '_'+ str(team_id) + '.pkl').truncate(before=identical_rank-size_extract_identical,after=identical_rank).sort_index(ascending=False)
        data3 = data3.set_index(pd.Index([i for i in range (len(data3))]))
        data3.to_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_identical_season_s'+ '_'+ str(seasons[-2]) + '.pkl')
        print("fixtures_identical_season_s() : {}".format(round(time.time()-start_time,2))) 

# OK -
def fixturesrounds_league_id_current_round_master_s(team_id,exc1,exc2,exc3,exc4):
    data_leagues = pd.read_pickle(link_data+central_folder+'/'+'other'+'/'+'leagues' +'.pkl') 
    for i in range (len(data_leagues)):
        if int(data_leagues.index[i])>start_date:    
            for j in range (len(data_leagues.columns)):
                if data_leagues.columns[j] != exc1 and data_leagues.columns[j] != exc2 and data_leagues.columns[j] != exc3 and data_leagues.columns[j] != exc4:
                    league_id = int(data_leagues.iloc[i,j])
                    my_file = Path(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixturesrounds_league_id_current_round_s'+ '_'+ str(league_id) +'.pkl')
                    if not my_file.is_file() or int(data_leagues.index[i])>2019: 
                        fixturesrounds_league_id_current_round_s(league_id)

# OK -
def fixturesrounds_league_id_current_round_s(league_id):
    league_id = int(league_id)
    url_fixturesrounds_league_id_current_round_s = url + "fixtures/rounds/" + str(league_id) + '/current'
    response = requests.request("GET", url_fixturesrounds_league_id_current_round_s, headers=headers)
    print("fixturesrounds_league_id_current_round_s + 1")
    x = pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures'])
    x.to_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixturesrounds_league_id_current_round_s'+ '_'+ str(league_id) +'.pkl')


'''
Ouput functions
------------------------------------------------------------------------------------
'''

# OK -
def output_rank_fixtures(team_id,fixture_id,game_fixture_id):
    fixture_id = int(fixture_id)
    df = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_s'+ '_'+ str(team_id) +'.pkl')
    x = df[df['fixture_id'] == fixture_id].index.values
    return int(x)

# OK -
def output_rank_fixtures_modified(team_id_1,team_id_2,fixture_id,game_fixture_id):
    fixture_id = int(fixture_id)
    df = pd.read_pickle(link_data+'{}'.format(team_id_1)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_s'+ '_'+ str(team_id_2) +'.pkl')
    x = df[df['fixture_id'] == fixture_id].index.values
    return int(x)
