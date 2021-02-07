# Imports 
import requests
import json
import pandas as pd  
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from pathlib import Path
import time

from parameters_package import *
from output_v2 import *

'''
Package parameters
------------------------------------------------------------------------------------
'''

global new_matrix
global old_matrix

'''
Functions
------------------------------------------------------------------------------------
'''

# OK - 
def summarize_matrix(team_id,last_fixtures_lineups_duration,all,option,game_fixture_id): # 3 options
    global new_matrix
    new_matrix = [[j for j in range(10**6)] for i in range (1,4)] # for the 3 options

    if all == 0:
        print("start of calculation for team_id : {}".format(team_id))
        if option == 1 :
            #new_matrix[option-1][team_id] = output_matrix(team_id,last_fixtures_lineups_duration,all,option)
            new_matrix[option-1][team_id] = output_matrix_final(output_matrix(team_id,last_fixtures_lineups_duration,all,option,game_fixture_id))  
        else:
            new_matrix[option-1][team_id] = output_matrix(team_id,last_fixtures_lineups_duration,all,option,game_fixture_id)

        link_excel, link_pkl = link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+ '/' + 'new_matrix' +'_{}_{}'.format(team_id,option) + '.xlsx' , link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'new_matrix' +'_{}_{}'.format(team_id,option) + '.pkl'
        new_matrix[option-1][team_id].to_excel(link_excel)
        new_matrix[option-1][team_id].to_pickle(link_pkl)

        customize_excel(link_excel)
        print("end of calculation for team_id : {}".format(team_id))
    
    ''' This part has to be run after the main matrix was run ''' 
    if all == 1:
        option = 1
        matrix = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'new_matrix' +'_{}_{}'.format(team_id,option)+ '.pkl')
        opps_list = list(matrix['opp_team_id'])
        cpt = 0
        for x in opps_list:
            cpt += 1
            try:
                print("start of calculation for team_id : {}, with rank: {}/{}".format(x,cpt,last_fixtures_lineups_duration))
                new_matrix[option-1][x] = output_matrix_final(output_matrix(x,last_fixtures_lineups_duration,all,option,game_fixture_id))  
                #new_matrix[x] = output_matrix(x,last_fixtures_lineups_duration)

                link_excel, link_pkl = link_data+'{}'.format(x)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'new_matrix'+'_{}_{}'.format(x,option) + '.xlsx' , link_data+'{}'.format(x)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'new_matrix' +'_{}_{}'.format(x,option)+ '.pkl'
                new_matrix[option-1][x].to_excel(link_excel)
                new_matrix[option-1][x].to_pickle(link_pkl)
                
                customize_excel(link_excel)
                print("end of calculation for team_id : {}".format(x))
            except Exception as e:
                print(e)
# OK - 
def switch_matrix(team_id,option,game_fixture_id):
    global old_matrix
    old_matrix = [[j for j in range(10**6)] for i in range (1,4)]

    old_matrix[option-1][team_id] = new_matrix[option-1][team_id]
    old_matrix[option-1][team_id].to_excel(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'old_matrix'+'_{}_{}'.format(team_id,option) + '.xlsx')
    old_matrix[option-1][team_id].to_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'old_matrix' +'_{}_{}'.format(team_id,option)+ '.pkl')

    customize_excel(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'old_matrix'+'_{}_{}'.format(team_id,option) + '.xlsx')

    if option == 1:
        opps_list = list(new_matrix[option-1][team_id]['opp_team_id'])
        for p in opps_list:
            old_matrix[option-1][p] = new_matrix[option-1][p]
            try:
                old_matrix[option-1][p].to_excel(link_data+'{}'.format(p)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'old_matrix'+'_{}_{}'.format(p,option) + '.xlsx')
                old_matrix[option-1][p].to_pickle(link_data+'{}'.format(p)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'old_matrix' +'_{}_{}'.format(p,option)+ '.pkl')
                customize_excel(link_data+'{}'.format(p)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'old_matrix'+'_{}_{}'.format(p,option) + '.xlsx')
            except:
                pass
   
# OK - 
def initialize_matrix(team_id,option,game_fixture_id):
    global new_matrix
    global old_matrix
    new_matrix = [[j for j in range(10**6)] for i in range (1,4)]
    #old_matrix = [[j for j in range(10**6)] for i in range (1,4)]

    new_matrix[option-1][team_id] = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'new_matrix' +'_{}_{}'.format(team_id,option)+ '.pkl')
    #old_matrix[option-1][team_id] = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'old_matrix' +'_{}_{}'.format(team_id,option)+ '.pkl')
    
    if option == 1:
        opps_list = list(new_matrix[option-1][team_id]['opp_team_id'])
        for p in opps_list:
            try:
                new_matrix[option-1][p] = pd.read_pickle(link_data+'{}'.format(p)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'new_matrix' +'_{}_{}'.format(p,option)+ '.pkl')
            except:
                pass
            #try:
                #old_matrix[option-1][p] = pd.read_pickle(link_data+'{}'.format(p)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'old_matrix' +'_{}_{}'.format(p,option)+ '.pkl')
            #except: 
                #pass

'''
Other functions
------------------------------------------------------------------------------------
'''

# OK - 
def transfer_to_main_matrix(team_id,option,game_fixture_id):
    team_id = int(team_id)
    initialize_matrix(team_id,option,game_fixture_id)
    for col in new_matrix[option-1][team_id].columns:
        if col[:2] == '^O':
            for i in range (len(new_matrix[option-1][team_id])):
                fixture_id = int(new_matrix[option-1][team_id].iloc[i,new_matrix[option-1][team_id].columns.get_loc('fixture_id')])
                opp_id = int(new_matrix[option-1][team_id].iloc[i,new_matrix[option-1][team_id].columns.get_loc('opp_team_id')])
                try :
                    p = 0
                    while p<len(new_matrix[option-1][opp_id]) and int(new_matrix[option-1][opp_id].iloc[p,new_matrix[option-1][opp_id].columns.get_loc('fixture_id')]) != fixture_id :
                        p += 1
                    if p != len(new_matrix[option-1][opp_id]):   
                        new_matrix[option-1][team_id].iloc[i,new_matrix[option-1][team_id].columns.get_loc(col)] = new_matrix[option-1][opp_id].iloc[p,new_matrix[option-1][opp_id].columns.get_loc('^T'+col[2:])]
                except:
                    pass
    link_excel, link_pkl = link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'new_matrix'+'_{}_{}'.format(team_id,option) + '.xlsx' , link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'new_matrix' +'_{}_{}'.format(team_id,option)+ '.pkl'
    new_matrix[option-1][team_id].to_excel(link_excel)
    new_matrix[option-1][team_id].to_pickle(link_pkl) 
    customize_excel(link_excel)      
