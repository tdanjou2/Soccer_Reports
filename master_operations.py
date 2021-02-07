# Imports 
import requests
import json
import pandas as pd  
import numpy as np
from pathlib import Path
import time
import os
import os.path
import shutil  
from shutil import copyfile

from parameters_package import *
from core_functions import * # For nan_to_zero function

from coachs_package import * 
from events_package import *
from fixtures_package import *
from leagues_package import *
from lineups_package import *
from odds_package import *
from players_package import *
from sidelined_package import * 
from statistics_package import * 
from teams_package import * 
from trophies_package import *
from transfers_package import *
from summarize import *
from introduction_reports import *
from composition_reports import *
from pressure_reports import *
from typology_reports import *
from h2h_reports import *
from download_data import *

'''
Package parameters
------------------------------------------------------------------------------------
'''



global team_id 
global opp_id  
global team_name 
global opp_name  
global game_fixture_id  


team_id = 79
opp_id = 89
team_name = "Lille"
opp_name = "Dijon"
game_fixture_id = "571683 Lille-Dijon"
pres_path = link_reports + game_fixture_id + '/' + 'report' +'/'+'report' + '.pptx'  
homeTeam_id = 79
awayTeam_id = 89
homeTeam_name = "Lille"
awayTeam_name = "Dijon"
df_raw_home_1 = pd.read_pickle(link_data+'{}'.format(homeTeam_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'new_matrix' +'_{}_{}'.format(homeTeam_id,1) + '.pkl')
df_raw_home_2 = pd.read_pickle(link_data+'{}'.format(homeTeam_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'new_matrix' +'_{}_{}'.format(homeTeam_id,2) + '.pkl')
df_raw_home_3 = pd.read_pickle(link_data+'{}'.format(homeTeam_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'new_matrix' +'_{}_{}'.format(homeTeam_id,3) + '.pkl')
df_raw_away_1 = pd.read_pickle(link_data+'{}'.format(awayTeam_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'new_matrix' +'_{}_{}'.format(awayTeam_id,1) + '.pkl')
df_raw_away_2 = pd.read_pickle(link_data+'{}'.format(awayTeam_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'new_matrix' +'_{}_{}'.format(awayTeam_id,2) + '.pkl')
df_raw_away_3 = pd.read_pickle(link_data+'{}'.format(awayTeam_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'new_matrix' +'_{}_{}'.format(awayTeam_id,3) + '.pkl')




'''
Central function to quick off a batch of reports
------------------------------------------------------------------------------------
'''

# OK -
def master_function_batch(need,all):
    val = input("Are you sure to launch the master_function_batch() ? If yes, enter YES!!")
    #all = 1
    cpt = 0
    game_fixture_id_list = []
    if val == "YES!!":
        for i in input_dic.keys(): # This is a parameter
            team_id = int(input_dic[i]['team_id'])
            opp_id = int(input_dic[i]['opp_id'])
            if team_id != 0 and opp_id != 0:                
                x = fixtures_team_id_next(team_id,1)[1]
                
                homeTeam_name = x.iloc[0,x.columns.get_loc('homeTeam')]['team_name']
                awayTeam_name = x.iloc[0,x.columns.get_loc('awayTeam')]['team_name']
                
                if x.iloc[0,x.columns.get_loc('homeTeam')]['team_id'] == team_id:
                    team_name = x.iloc[0,x.columns.get_loc('homeTeam')]['team_name']
                    opp_name = x.iloc[0,x.columns.get_loc('awayTeam')]['team_name']
                else:
                    team_name = x.iloc[0,x.columns.get_loc('awayTeam')]['team_name']
                    opp_name = x.iloc[0,x.columns.get_loc('homeTeam')]['team_name']
                
                fixtures_id = x.iloc[0,x.columns.get_loc('fixture_id')]
                game_fixture_id = str(fixtures_id) + " " + str(homeTeam_name) + "-" + str(awayTeam_name)
                
                print("THIS IS THE BEGGINING OD THE TEAM n° {}, for game n°{}".format(cpt+1,1+int(cpt/2)))
                
                master_function_data(need,all,team_id,opp_id,team_name,opp_name,game_fixture_id)
                
                if match_item_list_general(game_fixture_id,game_fixture_id_list): # only do it the second time because we need the data from both teams
                    master_function_reports(need,all,team_id,opp_id,team_name,opp_name,game_fixture_id)
                game_fixture_id_list.append(game_fixture_id)
                all = 0
                cpt += 1

# OK -
def master_function_data(need,all,team_id,opp_id,team_name,opp_name,game_fixture_id): # need can be set to 0

    download(team_id,last,nex,need,1,all,game_fixture_id) # k = 1 for the team, all = 0 or 1 depending on daily reset
    #download_all(team_id,last,nex,need,game_fixture_id) # We need to do it only if we do have to get game data for others 
    summarize_matrix(team_id,last_fixtures_lineups_duration,0,1,game_fixture_id) # Only the team, only the option 1 = classic
    summarize_matrix(team_id,last_fixtures_lineups_duration,0,2,game_fixture_id) # Only the team, only the option 2 = h2h
    summarize_matrix(team_id,last_fixtures_lineups_duration,0,3,game_fixture_id) # Only the team, only the option 3 = same period last year
    #summarize_matrix(team_id,last_fixtures_lineups_duration,1,1,game_fixture_id) # We need to do it only if we do have to get game data for others 
    initialize_matrix(team_id,1,game_fixture_id)

    switch_matrix(team_id,1,game_fixture_id)
    transfer_to_main_matrix(team_id,1,game_fixture_id) # Only the option 1

    last_minute_changes(team_id,opp_id,team_name,opp_name,game_fixture_id)

# OK -
def master_function_reports(need,all,team_id,opp_id,team_name,opp_name,game_fixture_id): # need can be set to 0

    fixtures_home_away = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_next_s'+ '_'+ str(team_id) +'_'+ str(nex) +'.pkl')
    homeTeam_id = int(fixtures_home_away.iloc[0,fixtures_home_away.columns.get_loc('homeTeam')]['team_id'])
    awayTeam_id = int(fixtures_home_away.iloc[0,fixtures_home_away.columns.get_loc('awayTeam')]['team_id'])
    homeTeam_name = fixtures_home_away.iloc[0,fixtures_home_away.columns.get_loc('homeTeam')]['team_name']
    awayTeam_name = fixtures_home_away.iloc[0,fixtures_home_away.columns.get_loc('awayTeam')]['team_name']
    
    df_raw_home_1 = pd.read_pickle(link_data+'{}'.format(homeTeam_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'new_matrix' +'_{}_{}'.format(homeTeam_id,1) + '.pkl')
    df_raw_home_2 = pd.read_pickle(link_data+'{}'.format(homeTeam_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'new_matrix' +'_{}_{}'.format(homeTeam_id,2) + '.pkl')
    df_raw_home_3 = pd.read_pickle(link_data+'{}'.format(homeTeam_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'new_matrix' +'_{}_{}'.format(homeTeam_id,3) + '.pkl')

    df_raw_away_1 = pd.read_pickle(link_data+'{}'.format(awayTeam_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'new_matrix' +'_{}_{}'.format(awayTeam_id,1) + '.pkl')
    df_raw_away_2 = pd.read_pickle(link_data+'{}'.format(awayTeam_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'new_matrix' +'_{}_{}'.format(awayTeam_id,2) + '.pkl')
    df_raw_away_3 = pd.read_pickle(link_data+'{}'.format(awayTeam_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'new_matrix' +'_{}_{}'.format(awayTeam_id,3) + '.pkl')


    introduction_master(team_id,team_name,opp_id,opp_name,game_fixture_id,name_folder_introduction,homeTeam_id,awayTeam_id,homeTeam_name,awayTeam_name,df_raw_home_1,df_raw_home_2,df_raw_home_3,df_raw_away_1,df_raw_away_2,df_raw_away_3)
    composition_master(team_id,team_name,opp_id,opp_name,game_fixture_id,name_folder_introduction,homeTeam_id,awayTeam_id,homeTeam_name,awayTeam_name,df_raw_home_1,df_raw_home_2,df_raw_home_3,df_raw_away_1,df_raw_away_2,df_raw_away_3)
    pressure_master(team_id,team_name,opp_id,opp_name,game_fixture_id,name_folder_introduction,homeTeam_id,awayTeam_id,homeTeam_name,awayTeam_name,df_raw_home_1,df_raw_home_2,df_raw_home_3,df_raw_away_1,df_raw_away_2,df_raw_away_3)
    typology_master(team_id,team_name,opp_id,opp_name,game_fixture_id,name_folder_introduction,homeTeam_id,awayTeam_id,homeTeam_name,awayTeam_name,df_raw_home_1,df_raw_home_2,df_raw_home_3,df_raw_away_1,df_raw_away_2,df_raw_away_3)
    #h2h_master(team_id,team_name,opp_id,opp_name,game_fixture_id,name_folder_introduction,homeTeam_id,awayTeam_id,homeTeam_name,awayTeam_name,df_raw_home_1,df_raw_home_2,df_raw_home_3,df_raw_away_1,df_raw_away_2,df_raw_away_3)