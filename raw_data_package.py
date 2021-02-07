import requests
import json
import pandas as pd
import numpy as np

from players_package import *
from parameters_package import *


'''
Functions
------------------------------------------------------------------------------------
'''

# OK -
def name_manager(test1,test2):
    test = input("Are you sure you want to reinitialize the name managers ? Every name will be lost. If Yes, enter YES!!")
    if test == 'YES!!' and test1 == "ok" and test2 == "ok" :
        x = pd.DataFrame([i for i in range(100000)],columns=['team_name'])
        x.to_pickle(link_data+central_folder+'/'+'other'+'/' + 'name_manager' + '.pkl')
        x.to_excel(link_data+central_folder+'/'+'other'+'/' + 'name_manager' + '.xlsx')

# OK -
def leagues_function():
    url_leagues_function = url + "leagues/"
    response_leagues = requests.request("GET", url_leagues_function, headers=headers)
    print("leagues_function + 1")
    y_leagues = json.loads(response_leagues.text)
    league_id = pd.DataFrame.from_dict(y_leagues['api']['leagues'])
    league_id.to_excel(link_data+central_folder+'/'+'other'+'/' + 'raw_data_leagues' + '.xlsx')
    league_id.to_pickle(link_data+central_folder+'/'+'other'+'/' + 'raw_data_leagues' + '.pkl')
    return league_id

# OK - 
def leagues_function_to_team():
    url_leagues_function = url + "leagues/"
    response_leagues = requests.request("GET", url_leagues_function, headers=headers)
    print("leagues_function_to_team + 1")
    y_leagues = json.loads(response_leagues.text)
    league_id = pd.DataFrame.from_dict(y_leagues['api']['leagues'])

    ligue_1 = {'2010': None, '2011': None, '2012': None, '2013': None, '2014': None,
               '2015': None, '2016': None, '2017': None, '2018': None, '2019': None, '2020': None}
    ligue_2 = {'2010': None, '2011': None, '2012': None, '2013': None, '2014': None,
               '2015': None, '2016': None, '2017': None, '2018': None, '2019': None, '2020': None}

    liga_1 = {'2010': None, '2011': None, '2012': None, '2013': None, '2014': None,
            '2015': None, '2016': None, '2017': None, '2018': None, '2019': None, '2020': None}
    liga_2 = {'2010': None, '2011': None, '2012': None, '2013': None, '2014': None,
            '2015': None, '2016': None, '2017': None, '2018': None, '2019': None, '2020': None}

    bundesliga_1 = {'2010': None, '2011': None, '2012': None, '2013': None, '2014': None,
                  '2015': None, '2016': None, '2017': None, '2018': None, '2019': None, '2020': None}
    bundesliga_2 = {'2010': None, '2011': None, '2012': None, '2013': None, '2014': None,
                  '2015': None, '2016': None, '2017': None, '2018': None, '2019': None, '2020': None}

    serie_1 = {'2010': None, '2011': None, '2012': None, '2013': None, '2014': None,
               '2015': None, '2016': None, '2017': None, '2018': None, '2019': None, '2020': None}
    serie_2 = {'2010': None, '2011': None, '2012': None, '2013': None, '2014': None,
               '2015': None, '2016': None, '2017': None, '2018': None, '2019': None, '2020': None}
            
    premiere_league_1 = {'2010': None, '2011': None, '2012': None, '2013': None, '2014': None,
                      '2015': None, '2016': None, '2017': None, '2018': None, '2019': None, '2020': None}
    premiere_league_2 = {'2010': None, '2011': None, '2012': None, '2013': None, '2014': None,
                      '2015': None, '2016': None, '2017': None, '2018': None, '2019': None, '2020': None}

    champions_league = {'2010': None, '2011': None, '2012': None, '2013': None, '2014': None,
                        '2015': None, '2016': None, '2017': None, '2018': None, '2019': None, '2020': None}

    global leagues
    leagues = {'ligue_1': ligue_1,'ligue_2': ligue_2, 'liga_1': liga_1,'liga_2': liga_2, 'bundesliga_1': bundesliga_1, 'bundesliga_2': bundesliga_2, 'serie_1': serie_1,
               'serie_2': serie_2,'premiere_league_1': premiere_league_1,'premiere_league_2': premiere_league_2, 'champions_league': champions_league}

    for i in range(len(league_id)):
        if league_id.loc[i, 'country'] == "France" and league_id.loc[i, 'name'] == "Ligue 1":
            ligue_1[str(league_id.loc[i, 'season'])] = league_id.loc[i, 'league_id']
        if league_id.loc[i, 'country'] == "France" and league_id.loc[i, 'name'] == "Ligue 2":
            ligue_2[str(league_id.loc[i, 'season'])] = league_id.loc[i, 'league_id']

        if league_id.loc[i, 'country'] == "Spain" and league_id.loc[i, 'name'] == "Primera Division":
            liga_1[str(league_id.loc[i, 'season'])] = league_id.loc[i, 'league_id']
        if league_id.loc[i, 'country'] == "Spain" and league_id.loc[i, 'name'] == "Segunda Division":
            liga_2[str(league_id.loc[i, 'season'])] = league_id.loc[i, 'league_id']

        if league_id.loc[i, 'country'] == "Germany" and league_id.loc[i, 'name'] == "Bundesliga 1":
            bundesliga_1[str(league_id.loc[i, 'season'])] = league_id.loc[i, 'league_id']
        if league_id.loc[i, 'country'] == "Germany" and league_id.loc[i, 'name'] == "Bundesliga 2":
            bundesliga_2[str(league_id.loc[i, 'season'])] = league_id.loc[i, 'league_id']

        if league_id.loc[i, 'country'] == "England" and league_id.loc[i, 'name'] == "Premier League":
            premiere_league_1[str(league_id.loc[i, 'season'])] = league_id.loc[i, 'league_id']
        if league_id.loc[i, 'country'] == "England" and league_id.loc[i, 'name'] == "Championship":
            premiere_league_2[str(league_id.loc[i, 'season'])] = league_id.loc[i, 'league_id']

        if league_id.loc[i, 'country'] == "Italy" and league_id.loc[i, 'name'] == "Serie A":
            serie_1[str(league_id.loc[i, 'season'])] = league_id.loc[i, 'league_id']
        if league_id.loc[i, 'country'] == "Italy" and league_id.loc[i, 'name'] == "Serie B":
            serie_2[str(league_id.loc[i, 'season'])] = league_id.loc[i, 'league_id']

        if league_id.loc[i, 'country'] == "World" and league_id.loc[i, 'name'] == "UEFA Champions League":
            champions_league[str(league_id.loc[i, 'season'])] = league_id.loc[i, 'league_id']

    leagues = pd.DataFrame.from_dict(leagues)
    leagues = nan_to_zero_all(leagues)
    leagues.to_excel(link_data+central_folder+'/'+'other'+'/' + 'leagues' + '.xlsx')
    leagues.to_pickle(link_data+central_folder+'/'+'other'+'/' + 'leagues' + '.pkl')
    return leagues

# OK -          
def teams_function():
    url_teams_function = url + "teams/league/"
    global teams
    teams = {'ligue_1': {'2010': None, '2011': None, '2012': None, '2013': None, '2014': None, '2015': None, '2016': None, '2017': None, '2018': None, '2019': None, '2020': None},
             'liga_1': {'2010': None, '2011': None, '2012': None, '2013': None, '2014': None, '2015': None, '2016': None, '2017': None, '2018': None, '2019': None, '2020': None},
             'bundesliga_1': {'2010': None, '2011': None, '2012': None, '2013': None, '2014': None, '2015': None, '2016': None, '2017': None, '2018': None, '2019': None, '2020': None},
             'serie_1': {'2010': None, '2011': None, '2012': None, '2013': None, '2014': None, '2015': None, '2016': None, '2017': None, '2018': None, '2019': None, '2020': None},
             'premiere_league_1': {'2010': None, '2011': None, '2012': None, '2013': None, '2014': None, '2015': None, '2016': None, '2017': None, '2018': None, '2019': None, '2020': None},
             'champions_league': {'2010': None, '2011': None, '2012': None, '2013': None, '2014': None, '2015': None, '2016': None, '2017': None, '2018': None, '2019': None, '2020': None}}
    cmpt = 0
    for i in leagues.keys():
        print(i)
        if i[-1] == "1" :
            print(2)
            for j in leagues[i].keys():
                url_teams_function = url + "teams/league/"
                try:
                    a = str(int(leagues[i][j]))
                except:
                    a = str(leagues[i][j])
                if a != 'None' and a != 'nan':
                    url_teams_function += a
                    response_leagues = requests.request("GET", url_teams_function, headers=headers)
                    print("teams_function + 1")
                    request_cpt += 1
                    y_teams = json.loads(response_leagues.text)
                    team_id = pd.DataFrame.from_dict(y_teams['api']['teams'])
                    cmpt += 1
                    l = []
                    k = 0
                    for k in range(len(team_id['team_id'])):
                        l.append([team_id.iloc[k, team_id.columns.get_loc('team_id')], team_id.iloc[k, team_id.columns.get_loc('name')]])
                    teams[i][j] = l
                    print(cmpt)
    teams = pd.DataFrame.from_dict(teams)
    
    teams.to_excel(link_data+central_folder+'/'+'other'+'/' + 'teams' + '.xlsx')
    teams.to_pickle(link_data+central_folder+'/'+'other'+'/' + 'teams' + '.pkl')

    return teams

'''
Other functions
------------------------------------------------------------------------------------
'''


# OK -
def leagues_league_id(league_id):
    league_id = str(league_id)
    url_leagues_league_id = url + "leagues/league/" + league_id
    response = requests.request("GET", url_leagues_league_id, headers=headers)
    print("leagues_league_id + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['leagues']).columns), pd.DataFrame.from_dict(json.loads(response.text)['api']['leagues'])

# OK-
def leagues_team_id(team_id):
    team_id = str(team_id)
    url_leagues_team_id = url + "leagues/team/" + team_id
    response = requests.request("GET", url_leagues_team_id, headers=headers)
    print("leagues_team_id + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['leagues']).columns), pd.DataFrame.from_dict(json.loads(response.text)['api']['leagues'])

# OK -
def rounds_league_id(league_id):
    league_id = str(league_id)
    url_rounds_league_id = url + "fixtures/rounds/" + league_id
    response = requests.request("GET", url_rounds_league_id, headers=headers)
    print("rounds_league_id + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures']).columns), pd.DataFrame.from_dict(json.loads(response.text)['api']['fixtures'])
