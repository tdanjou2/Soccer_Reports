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

'''
Package parameters
------------------------------------------------------------------------------------
'''

'''
Central function to quick off a batch of reports
------------------------------------------------------------------------------------
'''

# OK -
def download_all(team_id,last,nex,need,game_fixture_id): # "need" variable is for formulas without a test, but maybe not wort updating. Ex: coachs_team_id_s  
    start_time = time.time()
    
    opps_list = fixtures_list_opp_id(team_id,game_fixture_id)
    k = 0
    all = 0
    cpt = 0
    for x in opps_list :
        cpt += 1
        x = int(x)
        print("team_id: {}".format(x), "compteur: {}/{}".format(cpt,last_fixtures_lineups_duration))

        download(x,last,nex,need,k,all,game_fixture_id)

    print("download_all() : {}".format(round(time.time()-start_time,2))) 
    
# OK - 
def download(team_id,last,nex,need,k,all,game_fixture_id): # k = 1 for the team, k = 0 for the opponents
    start_time = time.time()
    exist_data = 0
    
    # Creation of the folders
    # For the Data folders
    if not os.path.exists(link_data + str(team_id)):
        os.mkdir(link_data + str(team_id))
        exist_data = 0
        print("Directory " , link_data + str(team_id)," Created ")
    else:    
        exist_data = 1
        print("Directory " , link_data + str(team_id) ,  " already exists")

    # For the Reports folders
    if k == 1:
        if not os.path.exists(link_reports + str(game_fixture_id)):
            os.mkdir(link_reports + str(game_fixture_id))
            print("Directory " , link_reports + str(game_fixture_id)," Created ")
        else:    
            print("Directory " , link_reports + str(game_fixture_id) ,  " already exists")

    # For the Data folders
    if exist_data == 1:
        if len(link_data + str(team_id)) != 0: 
            x_time, x_name = 0,""
            for foldername in os.listdir(link_data + str(team_id)) :
                if foldername != ".DS_Store" :
                    if os.path.getmtime(link_data + str(team_id) + '/'+ foldername)>x_time:
                        x_time = os.path.getmtime(link_data + str(team_id) + '/'+ foldername)
                        x_name = foldername
            try:
                shutil.copytree(link_data + str(team_id) +'/'+ x_name, link_data + str(team_id) +'/'+ game_fixture_id)
                for p1 in os.listdir(link_data + str(team_id) +'/'+ game_fixture_id) :
                    if p1 == "summarize_package" :
                        for p2 in os.listdir(link_data + str(team_id) +'/'+ game_fixture_id +'/' +p1):
                            os.remove(link_data + str(team_id) +'/'+ game_fixture_id +'/' +p1 +'/'+p2)
            except:
                print("file {} already exists".format(link_data + str(team_id) +'/'+ game_fixture_id))
        for cpt_1 in list_links:
            if not os.path.exists(link_data + str(team_id) +'/'+ str(game_fixture_id) + '/' + cpt_1):
                os.mkdir(link_data + str(team_id) +'/'+ str(game_fixture_id) + '/' + cpt_1)
    else:
        if not os.path.exists(link_data + str(team_id)+'/'+game_fixture_id):
            os.mkdir(link_data + str(team_id)+'/'+game_fixture_id)
            print("Directory " , link_data + str(team_id)+'/'+game_fixture_id , " Created ")
        else:    
            print("Directory " , link_data + str(team_id)+'/'+game_fixture_id ,  " already exists")

        for p in list_links:
            if not os.path.exists(link_data + str(team_id)+'/'+ str(game_fixture_id) + '/' +p):
                os.mkdir(link_data + str(team_id)+'/'+ str(game_fixture_id) + '/' +p)
                print("Directory " , link_data + str(team_id)+'/'+ str(game_fixture_id) + '/' +p ," Created ")
            else:    
                print("Directory " , link_data + str(team_id)+'/'+ str(game_fixture_id) + '/' +p , " already exists")
    
    # For the Reports folders
    if k == 1:
        if not os.path.exists(link_reports +game_fixture_id):
            os.mkdir(link_reports+game_fixture_id)
                
        for foldername_2 in os.listdir(link_reports + str(central_folder)):
            if foldername_2 != ".DS_Store" and foldername_2 != "other" :
                if not os.path.exists(link_reports +game_fixture_id +'/'+ foldername_2):
                    os.mkdir(link_reports+game_fixture_id +'/'+ foldername_2)
                for p in os.listdir(link_reports + str(central_folder) +'/'+ foldername_2):
                    try:
                        if not os.path.exists(link_reports + game_fixture_id + '/' + foldername_2 + '/' + p):
                            copyfile(link_reports + str(central_folder) +'/'+ foldername_2 +'/'+ p, link_reports + game_fixture_id + '/' + foldername_2 + '/' + p)
                    except Exception as e:
                        print(e)

    
    # Test // X_CENTRAL_X
    leagues_season_s(team_id) # -> 1 - 0 (max - max)
    print("ok : leagues_season_s")

    leagues_team_id_s(team_id,game_fixture_id) # -> 1 - 1 (max - max)
    print("ok : leagues_team_id_s")

    leagues_team_id_relevant_s(team_id,game_fixture_id) # -> 1 - 1 (max - max)
    print("ok : leagues_team_id_relevant_s")

    leagues_team_id_relevant2_s(team_id,game_fixture_id) # -> 1 - 1 (max - max)
    print("ok : leagues_team_id_relevant2_s")

    leagues_team_id_relevant3_s(team_id,game_fixture_id) # -> 1 - 1 (max - max)
    print("ok : leagues_team_id_relevant3_s")

    if all == 1:
        fixturesrounds_league_id_current_round_master_s(team_id,"champions_league",0,0,0) # Possibility to not updated
        print("ok : fixturesrounds_league_id_current_round_master_s")

    fixtures_team_id_s(team_id,game_fixture_id) # -> 1 - 1 (max - max)
    print("ok : fixtures_team_id_s")

    fixtures_team_id_last_s(team_id,last,game_fixture_id) # -> 1 - 1 (max - max)
    print("ok : fixtures_team_id_last_s")

    fixtures_team_id_next_s(team_id,nex,game_fixture_id) # -> 1 - 1 (max - max)
    print("ok : fixtures_team_id_next_s")

    fixtures_identical_season_s(team_id,k,game_fixture_id) # -> 0 - 0 (max - max)
    print("ok : fixtures_identical_season_s")
        
    fixtures_h2h_team_id_team_id_next_s(team_id,nex,k,game_fixture_id) # -> 1 - 1 (max - max)
    print("ok : fixtures_h2h_team_id_team_id_next_s")

    # Test // X_CENTRAL_X
    teams_league_id_s(team_id,k,game_fixture_id) # -> 5 - 0 (max - max)
    print("ok : teams_league_id_s")

    if all == 1:
        download_central_data("champions_league",0,0,0)
        print("ok : download_central_data")

    ''' NOT USEFUL '''
    # Test light
    #fixtures_league_id_s(team_id) 
    #print("ok : fixtures_league_id_s")

    ''' NOT USEFUL '''
    #fixtures_league_id_last_s(team_id,last)
    #print("ok : fixtures_league_id_last_s")

    ''' NOT USEFUL '''
    #fixtures_league_id_next_s(team_id,nex)
    #print("ok : fixtures_league_id_next_s")

    # Test // X_CENTRAL_X
    fixturesrounds_league_id_s(team_id,k,game_fixture_id) # -> 5 - 0 (max - max)
    print("ok : fixturesrounds_league_id_s")

    # Test light // X_CENTRAL_X
    fixtures_league_id_round_s(team_id,k,game_fixture_id) 
    print("ok : fixtures_league_id_round_s")

    # Test // X_CENTRAL_X
    events_fixture_id_s(team_id,k,game_fixture_id) # -> last - 0 (max - max)
    print("ok : events_fixture_id_s")

    # Test // X_CENTRAL_X
    lineups_fixture_id_s(team_id,k,game_fixture_id) # -> last - 0 (max - max)
    print("ok : lineups_fixture_id_s")

    # Test // X_CENTRAL_X
    statistics_fixture_id_s(team_id,k,game_fixture_id) # -> last - 0 (max - max)
    print("ok : statistics_fixture_id_s")

    ''' NOT USEFUL '''
    #statistics_team_id_league_id_s(team_id) 
    #print("ok : statistics_team_id_league_id_s")

    ''' NOT USEFUL '''
    #if need == 1: # Can be done on a yearly basis
        #coachs_team_id_s(team_id)
        #print("ok : coachs_team_id_s")

    if need == 1: # Can be done on a yearly basis
        # Test ligth
        players_squad_team_id_season_s(team_id,game_fixture_id)
        print("ok : players_squad_team_id_season_s")

    ''' NOT USEFUL '''
    # Test
    #transfers_player_id_s(team_id)
    #print("ok : transfers_player_id_s")

    ''' NOT USEFUL '''
    # Test // Problem coach_id // team_id
    #trophies_coach_id_s(team_id)
    #print("ok : trophies_coach_id_s")

    ''' NOT USEFUL '''
    # Test
    #players_statistics_team_id_season_s(team_id)
    #print("ok : players_statistics_team_id_season_s")

    ''' NOT USEFUL '''
    # Test
    #players_statistics_player_id_season_s(team_id)
    #print("ok : players_statistics_player_id_season_s")
    
    # Test // X_CENTRAL_X
    players_statistics_fixture_id_s(team_id,k,game_fixture_id)
    print("ok : players_statistics_fixture_id_s")

    # Test // X_CENTRAL_X
    #teams_logo_team_id_s(team_id)
    #print("ok : teams_logo_team_id_s")

    print("download() team_id {} : {}".format(team_id,round(time.time()-start_time,2))) 

# OK -
def download_central_data(exc1,exc2,exc3,exc4):
    
    leagues_league_id_master_s(exc1,exc2,exc3,exc4)
    print( "ok : leagues_league_id_master_s")

    teams_league_id_master_s(exc1,exc2,exc3,exc4)
    print( "ok : teams_league_id_master_s")

    fixturesrounds_league_id_master_s(exc1,exc2,exc3,exc4)
    print("ok : fixturesrounds_league_id_master_s")

    fixtures_league_id_round_master_s(exc1,exc2,exc3,exc4)
    print("ok : fixtures_league_id_round_master_s")

    # Test
    #trophies_player_id_s(team_id)
    #print("ok : trophies_player_id_s")
