# Imports 
import requests
import json
import pandas as pd  
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from pathlib import Path
import time
import os
import os.path
from shutil import copyfile

from parameters_package import *
from core_functions import * # For nan_to_zero function

from coachs_package import *
from fixtures_package import *
from teams_package import *
from odds_package import *
from lineups_package import *
from leagues_package import *
from players_package import *
from sidelined_package import *
from statistics_package import *
from trophies_package import *
from events_package import *
from transfers_package import *

'''
Package parameters
------------------------------------------------------------------------------------
'''

'''
Main function
------------------------------------------------------------------------------------
'''

def output_matrix(team_id,last_fixtures_lineups_duration,all,option,game_fixture_id): # Option 1: classic last fixtures // Option 2: h2h games

    # Start of construction of matrix section
    indexes = []
    for i in range (last_fixtures_lineups_duration):
        indexes.append(i)
    matrix = pd.DataFrame(index = indexes, columns = cols)
    # End of construction of matrix section

    i = 0 # To be set to 0 because i variable was previously used 
    next_id = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_next_s'+ '_'+ str(team_id) + '_'+ str(nex) + '.pkl')
    try:
        if int(next_id.iloc[0,next_id.columns.get_loc("homeTeam")]['team_id']) == team_id:
            next_id = int(next_id.iloc[0,next_id.columns.get_loc("awayTeam")]['team_id'])
        else:
            next_id = int(next_id.iloc[0,next_id.columns.get_loc("homeTeam")]['team_id'])
        
        if option == 1 :
            variable_last_fixtures = pd.read_pickle(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/' +'fixtures_team_id_last_s'+ '_'+ str(team_id) +'_'+ str(last) +'.pkl') # The variable of last fixtures of a team
        if option == 2 :
            variable_last_fixtures = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_h2h_team_id_team_id_next_s'+ '_'+ str(team_id) + '_'+ str(next_id) + '.pkl') 
        if option == 3 :
            variable_last_fixtures = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_identical_season_s'+ '_'+ str(seasons[-2]) + '.pkl')
        
        while i < last_fixtures_lineups_duration :
            try :
                # Start of essentials data section
                matrix.iloc[i,matrix.columns.get_loc('fixture_id')] = variable_last_fixtures['fixture_id'][i]
                matrix.iloc[i,matrix.columns.get_loc('event_date')] = variable_last_fixtures['event_date'][i]
                matrix.iloc[i,matrix.columns.get_loc('round')] = variable_last_fixtures['round'][i]
                matrix.iloc[i,matrix.columns.get_loc('league_id')] = variable_last_fixtures['league_id'][i]

                """             
                x_time, x_name = 0,""
                for foldername in os.listdir(link_data + str(team_id)) :
                    if foldername != ".DS_Store" :
                        if os.path.getmtime(link_data + str(team_id) + '/'+ foldername)>x_time:
                            x_time = os.path.getmtime(link_data + str(team_id) + '/'+ foldername)
                            x_name = foldername
                try: 
                    data = pd.read_pickle(link_data + str(team_id) + '/'+ foldername + '/' + 'summarize_package' +'/' + 'new_matrix_'+str(team_id)+'_'+str(option)+'.pkl')
                    for cpt_10 in range (len(data)):
                        if data.iloc[cpt_10,data.columns.get_loc('fixture_id')] == variable_last_fixtures['fixture_id'][i]:
                            for cols in data.columns:
                                matrix[cols][i] = data[cols][cpt_10] """

                try: 
                    try:
                        variable_comments = pd.read_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixtures_league_id_round_s'+ '_'+ str(variable_last_fixtures['league_id'][i]) +'_' +str(variable_last_fixtures['round'][i])+'.pkl').\
                            loc[pd.read_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixtures_league_id_round_s'+ '_'+ str(variable_last_fixtures['league_id'][i]) +'_' +str(variable_last_fixtures['round'][i])+'.pkl')['fixture_id'] == variable_last_fixtures['fixture_id'][i]]
                    
                    except:
                        variable_comments = pd.read_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixtures_league_id_round_s'+ '_'+ str(variable_last_fixtures['league_id'][i]) +'_' +round_formating(str(variable_last_fixtures['round'][i]))+'.pkl').\
                            loc[pd.read_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixtures_league_id_round_s'+ '_'+ str(variable_last_fixtures['league_id'][i]) +'_' +round_formating(str(variable_last_fixtures['round'][i]))+'.pkl')['fixture_id'] == variable_last_fixtures['fixture_id'][i]]
                    
                    matrix.iloc[i,matrix.columns.get_loc('comments')] = [{'status':variable_comments['status'],'firstHalfStart':variable_comments['firstHalfStart'], 'secondHalfStart':variable_comments['secondHalfStart']}]
                except:
                    matrix.iloc[i,matrix.columns.get_loc('comments')] = ["No comments"]
                try: 
                    matrix.iloc[i,matrix.columns.get_loc('referee')] = variable_last_fixtures['referee'][i]
                except:
                    print("no referee")
                # End of essentials data section

                variable_statistics_fixture = pd.read_pickle(link_data+central_folder+'/'+link_data_package_statitics_central+'/' +'statistics_fixture_id_s'+'_' + str(variable_last_fixtures['fixture_id'][i])+'.pkl') # The statistics of a fixture
                try:
                    variable_teams = pd.read_pickle(link_data+central_folder+'/'+link_data_package_teams_central+'/' +'teams_league_id_s'+ '_'+ str(variable_last_fixtures['league_id'][i])+'.pkl') # The list of teams within a given legue
                    team_name = str(variable_teams.loc[variable_teams['team_id'] == team_id].iloc[0,variable_teams.loc[variable_teams['team_id'] == team_id].columns.get_loc('name')])
                except:
                    if type(pd.read_pickle(link_data+central_folder+'/'+'other'+'/' + 'name_manager' + '.pkl').iloc[team_id,0]) == type("string"):
                        team_name = pd.read_pickle(link_data+central_folder+'/'+'other'+'/' + 'name_manager' + '.pkl').iloc[team_id,0] 
                    else:
                        team_name = str(output_name(team_id)) 
                        p = pd.read_pickle(link_data+central_folder+'/'+'other'+'/' + 'name_manager' + '.pkl')
                        p.iloc[team_id,0] = team_name
                        p.to_pickle(link_data+central_folder+'/'+'other'+'/' + 'name_manager' + '.pkl')
                        p.to_excel(link_data+central_folder+'/'+'other'+'/' + 'name_manager' + '.xlsx')
                        print("Had to use the output_name() function for the team_name:{}".format(team_name))

                if variable_last_fixtures['awayTeam'][i]['team_name'] == team_name: 
                    matrix.iloc[i,matrix.columns.get_loc('away_home')] = "away"
                    matrix.iloc[i,matrix.columns.get_loc('opp_team_id')] = variable_last_fixtures['homeTeam'][i]['team_id']
                    try: 
                        variable_teams = pd.read_pickle(link_data+central_folder+'/'+link_data_package_teams_central+'/' +'teams_league_id_s'+ '_'+ str(variable_last_fixtures['league_id'][i])+'.pkl') # The list of teams within a given legue
                        opp_name = str(variable_teams.loc[variable_teams['team_id'] == variable_last_fixtures['homeTeam'][i]['team_id']].iloc[0,variable_teams.loc[variable_teams['team_id'] == variable_last_fixtures['homeTeam'][i]['team_id']].columns.get_loc('name')])
                    except:
                        if type(pd.read_pickle(link_data+central_folder+'/'+'other'+'/'+'name_manager' + '.pkl').iloc[variable_last_fixtures['homeTeam'][i]['team_id'],0]) == type("string"):
                            opp_name = pd.read_pickle(link_data+central_folder+'/'+'other'+'/' + 'name_manager' + '.pkl').iloc[variable_last_fixtures['homeTeam'][i]['team_id'],0] 
                        else:
                            opp_name = str(output_name(variable_last_fixtures['homeTeam'][i]['team_id'])) # Other alternative to pick the name of the team
                            p = pd.read_pickle(link_data+central_folder+'/'+'other'+'/' + 'name_manager' + '.pkl')
                            p.iloc[variable_last_fixtures['homeTeam'][i]['team_id'],0] = opp_name
                            p.to_pickle(link_data+central_folder+'/'+'other'+'/' + 'name_manager' + '.pkl')
                            p.to_excel(link_data+central_folder+'/'+'other'+'/' + 'name_manager' + '.xlsx')
                            print("Had to use the output_name() function for the opp_name:{}".format(opp_name))

                    matrix.iloc[i,matrix.columns.get_loc('opp_team_name')] = opp_name
                    matrix.iloc[i,matrix.columns.get_loc('BP')] = variable_last_fixtures['goalsAwayTeam'][i]
                    matrix.iloc[i,matrix.columns.get_loc('BC')] = variable_last_fixtures['goalsHomeTeam'][i]
                    try:
                        matrix.iloc[i,matrix.columns.get_loc('fouls_team')] = int(variable_statistics_fixture['Fouls']['away'])
                    except: 
                        pass
                    try:
                        matrix.iloc[i,matrix.columns.get_loc('fouls_opp')] = int(variable_statistics_fixture['Fouls']['home'])
                    except: 
                        pass

                    try:
                        matrix.iloc[i,matrix.columns.get_loc('Poss team')] = int(variable_statistics_fixture['Ball Possession']['away'][:-1])
                        matrix.iloc[i,matrix.columns.get_loc('Poss opp')] = int(variable_statistics_fixture['Ball Possession']['home'][:-1])
                    except:
                        pass
                    try:
                        matrix.iloc[i,matrix.columns.get_loc('passes_total_team')] = int(variable_statistics_fixture['Total passes']['away'])
                    except: 
                        pass
                    try:
                        matrix.iloc[i,matrix.columns.get_loc('passes_acc_team')] = int(variable_statistics_fixture['Passes accurate']['away'])
                    except: 
                        pass
                    try:
                        matrix.iloc[i,matrix.columns.get_loc('passes_total_opp')] = int(variable_statistics_fixture['Total passes']['home'])
                    except:
                        pass
                    try:
                        matrix.iloc[i,matrix.columns.get_loc('passes_acc_opp')] = int(variable_statistics_fixture['Passes accurate']['home'])
                    except: 
                        pass
                    try:
                        matrix.iloc[i,matrix.columns.get_loc('shots_team')] = int(variable_statistics_fixture['Total Shots']['away'])
                    except: 
                        pass
                    try:
                        matrix.iloc[i,matrix.columns.get_loc('shots_opp')] = int(variable_statistics_fixture['Total Shots']['home'])
                    except:
                        pass
                    
                    try:

                        if type(variable_statistics_fixture['Yellow Cards']['away']) == type(None):
                            matrix.iloc[i,matrix.columns.get_loc('yellow_team')] = 0
                        else:    
                            matrix.iloc[i,matrix.columns.get_loc('yellow_team')] = int(variable_statistics_fixture['Yellow Cards']['away'])
                        
                        if type(variable_statistics_fixture['Red Cards']['away']) == type(None):
                            matrix.iloc[i,matrix.columns.get_loc('red_team')] = 0
                        else:
                            matrix.iloc[i,matrix.columns.get_loc('red_team')] = int(variable_statistics_fixture['Red Cards']['away'])
                        
                        if type(variable_statistics_fixture['Yellow Cards']['home']) == type(None):
                            matrix.iloc[i,matrix.columns.get_loc('yellow_opp')] = 0
                        else:
                            matrix.iloc[i,matrix.columns.get_loc('yellow_opp')] = int(variable_statistics_fixture['Yellow Cards']['home'])
                        
                        if type(variable_statistics_fixture['Red Cards']['home']) == type(None):
                            matrix.iloc[i,matrix.columns.get_loc('red_opp')] = 0
                        else:
                            matrix.iloc[i,matrix.columns.get_loc('red_opp')] = int(variable_statistics_fixture['Red Cards']['home'])
                    except:
                        pass
                else:
                    matrix.iloc[i,matrix.columns.get_loc('away_home')] = "home"
                    matrix.iloc[i,matrix.columns.get_loc('opp_team_id')] = variable_last_fixtures['awayTeam'][i]['team_id']
                    try: 
                        variable_teams = pd.read_pickle(link_data+central_folder+'/'+link_data_package_teams_central+'/' +'teams_league_id_s'+ '_'+ str(variable_last_fixtures['league_id'][i])+'.pkl') # The list of teams within a given legue
                        opp_name = str(variable_teams.loc[variable_teams['team_id'] == variable_last_fixtures['awayTeam'][i]['team_id']].iloc[0,variable_teams.loc[variable_teams['team_id'] == variable_last_fixtures['awayTeam'][i]['team_id']].columns.get_loc('name')])
                    except:
                        if type(pd.read_pickle(link_data+central_folder+'/'+'other'+'/'+'name_manager'+'.pkl').iloc[variable_last_fixtures['awayTeam'][i]['team_id'],0]) == type("string"):
                            opp_name = pd.read_pickle(link_data+central_folder+'/'+'other'+'/'+'name_manager'+'.pkl').iloc[variable_last_fixtures['awayTeam'][i]['team_id'],0] 
                        else:
                            opp_name = str(output_name(variable_last_fixtures['awayTeam'][i]['team_id']))
                            p = pd.read_pickle(link_data+central_folder+'/'+'other'+'/' + 'name_manager' + '.pkl')
                            p.iloc[variable_last_fixtures['awayTeam'][i]['team_id'],0] = opp_name
                            p.to_pickle(link_data+central_folder+'/'+'other'+'/' + 'name_manager' + '.pkl')
                            p.to_excel(link_data+central_folder+'/'+'other'+'/' + 'name_manager' + '.xlsx')
                            print("Had to use the output_name() function for the opp_name:{}".format(opp_name))
                    matrix.iloc[i,matrix.columns.get_loc('opp_team_name')] = opp_name
                    matrix.iloc[i,matrix.columns.get_loc('BP')] = variable_last_fixtures['goalsHomeTeam'][i]
                    matrix.iloc[i,matrix.columns.get_loc('BC')] = variable_last_fixtures['goalsAwayTeam'][i]
                    try:
                        matrix.iloc[i,matrix.columns.get_loc('fouls_team')] = int(variable_statistics_fixture['Fouls']['home'])
                    except:
                        pass
                    try:
                        matrix.iloc[i,matrix.columns.get_loc('fouls_opp')] = int(variable_statistics_fixture['Fouls']['away'])
                    except:
                        pass
                    try:
                        matrix.iloc[i,matrix.columns.get_loc('Poss team')] = int(variable_statistics_fixture['Ball Possession']['home'][:-1])
                        matrix.iloc[i,matrix.columns.get_loc('Poss opp')] = int(variable_statistics_fixture['Ball Possession']['away'][:-1])
                    except:
                        pass
                    try:
                        matrix.iloc[i,matrix.columns.get_loc('passes_total_team')] = int(variable_statistics_fixture['Total passes']['home'])
                    except: 
                        pass
                    try:
                        matrix.iloc[i,matrix.columns.get_loc('passes_acc_team')] = int(variable_statistics_fixture['Passes accurate']['home'])
                    except: 
                        pass
                    try:
                        matrix.iloc[i,matrix.columns.get_loc('passes_total_opp')] = int(variable_statistics_fixture['Total passes']['away'])
                    except:
                        pass
                    try:
                        matrix.iloc[i,matrix.columns.get_loc('passes_acc_opp')] = int(variable_statistics_fixture['Passes accurate']['away'])
                    except: 
                        pass
                    try:
                        matrix.iloc[i,matrix.columns.get_loc('shots_team')] = int(variable_statistics_fixture['Total Shots']['home'])
                    except: 
                        pass
                    try:
                        matrix.iloc[i,matrix.columns.get_loc('shots_opp')] = int(variable_statistics_fixture['Total Shots']['away'])
                    except:
                        pass

                    try:
                        if type(variable_statistics_fixture['Yellow Cards']['home']) == type(None):
                            matrix.iloc[i,matrix.columns.get_loc('yellow_team')] = 0
                        else:    
                            matrix.iloc[i,matrix.columns.get_loc('yellow_team')] = int(variable_statistics_fixture['Yellow Cards']['home'])
                        
                        if type(variable_statistics_fixture['Red Cards']['home']) == type(None):
                            matrix.iloc[i,matrix.columns.get_loc('red_team')] = 0
                        else:
                            matrix.iloc[i,matrix.columns.get_loc('red_team')] = int(variable_statistics_fixture['Red Cards']['home'])
                        
                        if type(variable_statistics_fixture['Yellow Cards']['away']) == type(None):
                            matrix.iloc[i,matrix.columns.get_loc('yellow_opp')] = 0
                        else:
                            matrix.iloc[i,matrix.columns.get_loc('yellow_opp')] = int(variable_statistics_fixture['Yellow Cards']['away'])
                        
                        if type(variable_statistics_fixture['Red Cards']['away']) == type(None):
                            matrix.iloc[i,matrix.columns.get_loc('red_opp')] = 0
                        else:
                            matrix.iloc[i,matrix.columns.get_loc('red_opp')] = int(variable_statistics_fixture['Red Cards']['away'])
                    except:
                        pass
                variable_opp_id = int(matrix.iloc[i,matrix.columns.get_loc('opp_team_id')])

                if int(matrix.iloc[i,matrix.columns.get_loc('BC')])>int(matrix.iloc[i,matrix.columns.get_loc('BP')]) :
                    matrix.iloc[i,matrix.columns.get_loc('W-D-L')] = "L"
                elif int(matrix.iloc[i,matrix.columns.get_loc('BC')])<int(matrix.iloc[i,matrix.columns.get_loc('BP')]) :
                    matrix.iloc[i,matrix.columns.get_loc('W-D-L')] = "W"
                else:
                    matrix.iloc[i,matrix.columns.get_loc('W-D-L')] = "D"

                # Start of goals section
                matrix.iloc[i,matrix.columns.get_loc('BP_direct')] = output_direct_goals(team_id,team_id,variable_last_fixtures['fixture_id'][i])
                matrix.iloc[i,matrix.columns.get_loc('BP_own_goals')] = output_csc(team_id,team_id,variable_last_fixtures['fixture_id'][i],0)[0]
                matrix.iloc[i,matrix.columns.get_loc('BP_pre_red_card')] = output_number_event_pre_event_soft(team_id,variable_last_fixtures['fixture_id'][i],team_id,"Goal",variable_opp_id,"Card","Red Card")
                matrix.iloc[i,matrix.columns.get_loc('BP_pre_yellow_card')] = output_number_event_pre_event_soft(team_id,variable_last_fixtures['fixture_id'][i],team_id,"Goal",variable_opp_id,"Card","Yellow Card")
                matrix.iloc[i,matrix.columns.get_loc('BP_pre_penalty')] = output_number_event_pre_event_strict(team_id,variable_last_fixtures['fixture_id'][i],team_id,"Goal","Normal Goal",team_id,"Goal","Penalty")            
                
                matrix.iloc[i,matrix.columns.get_loc('BP_normal')] = output_number_event_pre_event_strict_3_events(team_id,variable_last_fixtures['fixture_id'][i],team_id,"Goal","Normal Goal",team_id,"Goal","Penalty",variable_opp_id,"Card","Red Card",variable_opp_id,"Card","Yellow Card")
                
                matrix.iloc[i,matrix.columns.get_loc('BP_subs')] = output_number_goals_subs(team_id,team_id,variable_last_fixtures['fixture_id'][i],variable_last_fixtures['league_id'][i],team_name,matrix.iloc[i,matrix.columns.get_loc('opp_team_name')])
                matrix.iloc[i,matrix.columns.get_loc('ABP_subs')] = output_number_assists_subs(team_id,team_id,variable_last_fixtures['fixture_id'][i],variable_last_fixtures['league_id'][i],team_name,matrix.iloc[i,matrix.columns.get_loc('opp_team_name')])
                matrix.iloc[i,matrix.columns.get_loc('BP_0-30')] = output_number_goals_X_Y_mins(team_id,team_id,0,30,variable_last_fixtures['fixture_id'][i])
                matrix.iloc[i,matrix.columns.get_loc('BP_30-60')] = output_number_goals_X_Y_mins(team_id,team_id,30,60,variable_last_fixtures['fixture_id'][i])
                matrix.iloc[i,matrix.columns.get_loc('BP_60-100')] = output_number_goals_X_Y_mins(team_id,team_id,60,100,variable_last_fixtures['fixture_id'][i])

                matrix.iloc[i,matrix.columns.get_loc('BC_direct')] = output_direct_goals(team_id,variable_opp_id,variable_last_fixtures['fixture_id'][i])
                matrix.iloc[i,matrix.columns.get_loc('BC_own_goals')] = output_csc(team_id,variable_opp_id,variable_last_fixtures['fixture_id'][i],0)[0]
                matrix.iloc[i,matrix.columns.get_loc('BC_pre_red_card')] = output_number_event_pre_event_soft(team_id,variable_last_fixtures['fixture_id'][i],variable_opp_id,"Goal",team_id,"Card","Red Card")
                matrix.iloc[i,matrix.columns.get_loc('BC_pre_yellow_card')] = output_number_event_pre_event_soft(team_id,variable_last_fixtures['fixture_id'][i],variable_opp_id,"Goal",team_id,"Card","Yellow Card")
                matrix.iloc[i,matrix.columns.get_loc('BC_pre_penalty')] = output_number_event_pre_event_strict(team_id,variable_last_fixtures['fixture_id'][i],variable_opp_id,"Goal","Normal Goal",variable_opp_id,"Goal","Penalty")
                
                matrix.iloc[i,matrix.columns.get_loc('BC_normal')] = output_number_event_pre_event_strict_3_events(team_id,variable_last_fixtures['fixture_id'][i],variable_opp_id,"Goal","Normal Goal",variable_opp_id,"Goal","Penalty",team_id,"Card","Red Card",team_id,"Card","Yellow Card")
                
                matrix.iloc[i,matrix.columns.get_loc('BC_subs')] = output_number_goals_subs(team_id,variable_opp_id,variable_last_fixtures['fixture_id'][i],variable_last_fixtures['league_id'][i],team_name,matrix.iloc[i,matrix.columns.get_loc('opp_team_name')])
                matrix.iloc[i,matrix.columns.get_loc('ABC_subs')] = output_number_assists_subs(team_id,variable_opp_id,variable_last_fixtures['fixture_id'][i],variable_last_fixtures['league_id'][i],team_name,matrix.iloc[i,matrix.columns.get_loc('opp_team_name')])
                matrix.iloc[i,matrix.columns.get_loc('BC_0-30')] = output_number_goals_X_Y_mins(team_id,variable_opp_id,0,30,variable_last_fixtures['fixture_id'][i])
                matrix.iloc[i,matrix.columns.get_loc('BC_30-60')] = output_number_goals_X_Y_mins(team_id,variable_opp_id,30,60,variable_last_fixtures['fixture_id'][i])
                matrix.iloc[i,matrix.columns.get_loc('BC_60-100')] = output_number_goals_X_Y_mins(team_id,variable_opp_id,60,100,variable_last_fixtures['fixture_id'][i])

                matrix.iloc[i,matrix.columns.get_loc('Penalty_comm_team')] = output_penalty_commited(team_id,team_id,variable_last_fixtures['fixture_id'][i])
                matrix.iloc[i,matrix.columns.get_loc('Penalty_comm_opp')] = output_penalty_commited(team_id,variable_opp_id,variable_last_fixtures['fixture_id'][i])
                matrix.iloc[i,matrix.columns.get_loc('First')] = output_first_goal(team_id,variable_last_fixtures['fixture_id'][i])
                # End of goals section

                variable_rank_fixtures = output_rank_fixtures(team_id,variable_last_fixtures['fixture_id'][i],game_fixture_id) # The rank of the current fixture in the list of all team fixtures : past and futures
                variable_fixtures = pd.read_pickle(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/' +'fixtures_team_id_s'+ '_'+ str(team_id)+'.pkl') # The list of all fixtures of a team : past and futures
                # Start of ranking of teams section 
                try :
                    matrix.iloc[i,matrix.columns.get_loc('rank_team')] = output_ranking_extract(matrix.iloc[i,matrix.columns.get_loc('round')],1,matrix.iloc[i,matrix.columns.get_loc('league_id')],team_id,team_id)
                except:
                    matrix.iloc[i,matrix.columns.get_loc('rank_team')] = output_ranking_extract(variable_fixtures.iloc[variable_rank_fixtures+1,variable_fixtures.columns.get_loc('round')],1,variable_fixtures.iloc[variable_rank_fixtures+1,variable_fixtures.columns.get_loc('league_id')],team_id,team_id)
                try : 
                    matrix.iloc[i,matrix.columns.get_loc('rank_opp')] = output_ranking_extract(matrix.iloc[i,matrix.columns.get_loc('round')],1,matrix.iloc[i,matrix.columns.get_loc('league_id')],team_id,variable_opp_id)
                except:
                    try:
                        matrix.iloc[i,matrix.columns.get_loc('rank_opp')] = output_ranking_extract(variable_fixtures.iloc[variable_rank_fixtures+1,variable_fixtures.columns.get_loc('round')],1,variable_fixtures.iloc[variable_rank_fixtures+1,variable_fixtures.columns.get_loc('league_id')],team_id,variable_opp_id)
                    except Exception as e:
                        print(e)
                # End of ranking of teams section

                # Start of neighbors teams 
                for cpt_2 in range (-neighbors,neighbors+1): # Only looking at neighbors 3 ranks away
                    if cpt_2 != 0:
                        try:
                            matrix.iloc[i,matrix.columns.get_loc("r{}_team".format(cpt_2))] = output_neighbors(str(matrix.iloc[i,matrix.columns.get_loc('round')]),1,matrix.iloc[i,matrix.columns.get_loc('league_id')],team_id,neighbors)[1][matrix.iloc[i,matrix.columns.get_loc('rank_team')][1]+cpt_2]
                        except:
                            matrix.iloc[i,matrix.columns.get_loc("r{}_team".format(cpt_2))] = "No team"
                # End of neighbors teams 

                # Start of futur games section
                for cpt_1 in range (1,max_future_game): # Max is 5
                    cpt_5 = 1
                    while variable_fixtures.iloc[variable_rank_fixtures-cpt_5,variable_fixtures.columns.get_loc('league_id')] != variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('league_id')] and cpt_5<10 :
                        cpt_5 += 1
                    try :
                        if cpt_5 != 10 : # Stop the loop
                            rounds = str(variable_fixtures.iloc[variable_rank_fixtures-cpt_5,variable_fixtures.columns.get_loc('round')])
                            league = variable_fixtures.iloc[variable_rank_fixtures-cpt_5,variable_fixtures.columns.get_loc('league_id')]
                            if int(variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('homeTeam')]['team_id']) == team_id :
                                matrix.iloc[i,matrix.columns.get_loc("N+{}_team".format(cpt_1))] = output_ranking_extract(rounds,0,league,team_id,variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('awayTeam')]['team_id'])+[variable_fixtures.iloc[variable_rank_fixtures-cpt_5,variable_fixtures.columns.get_loc('league')]['name']]+[variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('awayTeam')]['team_id']]
                            else :
                                matrix.iloc[i,matrix.columns.get_loc("N+{}_team".format(cpt_1))] = output_ranking_extract(rounds,0,league,team_id,variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('homeTeam')]['team_id'])+[variable_fixtures.iloc[variable_rank_fixtures-cpt_5,variable_fixtures.columns.get_loc('league')]['name']]+[variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('homeTeam')]['team_id']]
                        else: 
                                try:
                                    if int(variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('homeTeam')]['team_id']) == team_id :
                                        matrix.iloc[i,matrix.columns.get_loc("N+{}_team".format(cpt_1))] = [{"team_name":str(variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('awayTeam')]['team_name']),"team_id":int(variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('awayTeam')]['team_id']),"league_name":str(variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('league')]['name'])}]
                                    else:
                                        matrix.iloc[i,matrix.columns.get_loc("N+{}_team".format(cpt_1))] = [{"team_name":str(variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('homeTeam')]['team_name']),"team_id":int(variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('homeTeam')]['team_id']),"league_name":str(variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('league')]['name'])}]
                                except:
                                    matrix.iloc[i,matrix.columns.get_loc("N+{}_team".format(cpt_1))] = "STOP"
                    except:
                        try:
                            if int(variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('homeTeam')]['team_id']) == team_id :
                                matrix.iloc[i,matrix.columns.get_loc("N+{}_team".format(cpt_1))] = [{"team_name":str(variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('awayTeam')]['team_name']),"team_id":int(variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('awayTeam')]['team_id']),"league_name":str(variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('league')]['name'])}]
                            else:
                                matrix.iloc[i,matrix.columns.get_loc("N+{}_team".format(cpt_1))] = [{"team_name":str(variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('homeTeam')]['team_name']),"team_id":int(variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('homeTeam')]['team_id']),"league_name":str(variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('league')]['name'])}]
                        except Exception as e:    
                            print(e)

                # End of futur games section
                if all == 0:
                    # Start of futur games section for opponent
                    try:             
                        if os.path.exists(link_data+str(variable_opp_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/' +'fixtures_team_id_s'+ '_'+ str(variable_opp_id)+'.pkl'):
                            time_variable = os.path.getmtime(link_data+str(variable_opp_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/' +'fixtures_team_id_s'+ '_'+ str(variable_opp_id)+'.pkl')
                            file_variable = link_data+str(variable_opp_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/' +'fixtures_team_id_s'+ '_'+ str(variable_opp_id)+'.pkl'
                        else:           
                            time_variable = 0
                            file_variable = ""
                        for cpt_8 in os.listdir(link_data):
                            if cpt_8 != ".DS_Store" and cpt_8 != "old" and cpt_8 != "X_CENTRAL_X" : #and test_team_league(int(cpt_8),variable_last_fixtures['league_id'][i]):
                                for cpt_9 in os.listdir(link_data+cpt_8):
                                    if cpt_9 != '.DS_Store': 
                                        for filename in os.listdir(link_data+cpt_8 +'/'+cpt_9+'/'+'fixtures_package'):
                                            if (filename == "fixtures_team_id_s_" + str(variable_opp_id) + '.pkl') and filename != ".DS_Store":
                                                print("le lien"+ link_data+cpt_8 +'/'+cpt_9+'/'+'fixtures_package'+'/'+filename)
                                                if os.path.getmtime(link_data+cpt_8 +'/'+cpt_9+'/'+'fixtures_package'+'/'+filename)>time_variable:
                                                    time_variable = os.path.getmtime(link_data+cpt_8 +'/'+cpt_9+'/'+'fixtures_package'+'/'+filename)
                                                    file_variable = link_data+cpt_8 +'/'+cpt_9+'/'+'fixtures_package'+'/'+filename
                        if time_variable>(datetime.timestamp(datetime.now()-timedelta(seconds=detla_seconds_update))):
                            if file_variable != link_data+str(team_id)+'/'+game_fixture_id+'/'+'fixtures_package'+'/'+'fixtures_team_id_s_' + str(variable_opp_id)+'.pkl':
                                copyfile(file_variable,link_data+str(team_id)+'/'+game_fixture_id+'/'+'fixtures_package'+'/'+'fixtures_team_id_s_' + str(variable_opp_id)+'.pkl')
                        else:
                            fixtures_team_id_modified_s(team_id,variable_opp_id,game_fixture_id)


                        variable_fixtures = pd.read_pickle(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/' +'fixtures_team_id_s'+ '_'+ str(variable_opp_id)+'.pkl') # The list of all fixtures of a team : past and futures
                        variable_rank_fixtures = output_rank_fixtures_modified(team_id,variable_opp_id,variable_last_fixtures['fixture_id'][i],game_fixture_id) # The rank of the current fixture in the list of all team fixtures : past and futures

                        for cpt_1 in range (1,max_future_game): # Max is 5
                            cpt_5 = 1
                            while variable_fixtures.iloc[variable_rank_fixtures-cpt_5,variable_fixtures.columns.get_loc('league_id')] != variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('league_id')] and cpt_5<10 :
                                cpt_5 += 1
                            try :
                                if cpt_5 != 10 : # Stop the loop
                                    rounds = str(variable_fixtures.iloc[variable_rank_fixtures-cpt_5,variable_fixtures.columns.get_loc('round')])
                                    league = variable_fixtures.iloc[variable_rank_fixtures-cpt_5,variable_fixtures.columns.get_loc('league_id')]
                                    if int(variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('homeTeam')]['team_id']) == variable_opp_id :
                                        matrix.iloc[i,matrix.columns.get_loc("N+{}_opp".format(cpt_1))] = output_ranking_extract(rounds,0,league,team_id,variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('awayTeam')]['team_id'])
                                    else :
                                        matrix.iloc[i,matrix.columns.get_loc("N+{}_opp".format(cpt_1))] = output_ranking_extract(rounds,0,league,team_id,variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('homeTeam')]['team_id'])
                                else: 
                                        matrix.iloc[i,matrix.columns.get_loc("N+{}_opp".format(cpt_1))] = "STOP"
                            except:
                                try:
                                    if int(variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('homeTeam')]['team_id']) == variable_opp_id :
                                        matrix.iloc[i,matrix.columns.get_loc("N+{}_opp".format(cpt_1))] = variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('awayTeam')]['team_name']
                                    else:
                                        matrix.iloc[i,matrix.columns.get_loc("N+{}_opp".format(cpt_1))] = variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('homeTeam')]['team_name']
                                except:    
                                    print("erreur with N+{}_opp for i={}".format(cpt_1,i))
                    except Exception as e:
                        print(e)
                    # End of futur games section for opponent

                    # Start of futur games section for neighbors
                    for cpt_6 in range (-neighbors,neighbors+1):
                        if cpt_6 != 0:
                            if matrix.iloc[i,matrix.columns.get_loc("r{}_team".format(cpt_6))] != "No team" :
                                try:
                                    neighbors_id = int(matrix.iloc[i,matrix.columns.get_loc("r{}_team".format(cpt_6))][-2])
                                    neighbors_fixtures = int(matrix.iloc[i,matrix.columns.get_loc("r{}_team".format(cpt_6))][-1])
                                    try:
                                        if not os.path.exists(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/' +'fixtures_team_id_s'+ '_'+ str(neighbors_id)+'.pkl'):
                                            time_variable = 0
                                            file_variable = ""
                                            for cpt_8 in os.listdir(link_data):
                                                if cpt_8 != ".DS_Store" and cpt_8 != "old" and cpt_8 != "X_CENTRAL_X" : #and test_team_league(int(cpt_8),variable_last_fixtures['league_id'][i]):
                                                    for cpt_9 in os.listdir(link_data+cpt_8):
                                                        if cpt_9 != '.DS_Store':   
                                                            for filename in os.listdir(link_data+cpt_8 +'/'+cpt_9+'/'+'fixtures_package'):
                                                                if (filename == "fixtures_team_id_s_" + str(neighbors_id) + '.pkl') and filename != '.DS_Store':
                                                                    if os.path.getmtime(link_data+cpt_8 +'/'+cpt_9+'/'+'fixtures_package'+'/'+filename)>time_variable:
                                                                        time_variable = os.path.getmtime(link_data+cpt_8 +'/'+cpt_9+'/'+'fixtures_package'+'/'+filename)
                                                                        file_variable = link_data+cpt_8 +'/'+cpt_9+'/'+'fixtures_package'+'/'+filename
                                            if time_variable>(datetime.timestamp(datetime.now()-timedelta(seconds=detla_seconds_update))):
                                                if file_variable != link_data+str(team_id)+'/'+game_fixture_id+'/'+'fixtures_package'+'/'+'fixtures_team_id_s_' + str(neighbors_id)+ '.pkl':
                                                    copyfile(file_variable,link_data+str(team_id)+'/'+game_fixture_id+'/'+'fixtures_package'+'/'+'fixtures_team_id_s_' + str(neighbors_id)+ '.pkl')
                                            else:
                                                fixtures_team_id_modified_s(team_id,neighbors_id,game_fixture_id)

                                        else: 
                                            time_variable = 0
                                            file_variable = ""
                                            for cpt_8 in os.listdir(link_data):
                                                if cpt_8 != ".DS_Store" and cpt_8 != "old" and cpt_8 != "X_CENTRAL_X" and cpt_8 != str(team_id) : #and test_team_league(int(cpt_8),variable_last_fixtures['league_id'][i]):
                                                    for cpt_9 in os.listdir(link_data+cpt_8):
                                                        if cpt_9 != '.DS_Store' :    
                                                            for filename in os.listdir(link_data+cpt_8 +'/'+cpt_9+'/'+'fixtures_package'):
                                                                if (filename == "fixtures_team_id_s_" + str(neighbors_id)+ '.pkl') and filename != '.DS_Store':
                                                                    if os.path.getmtime(link_data+cpt_8 +'/'+cpt_9+'/'+'fixtures_package'+'/'+filename)>time_variable:
                                                                        time_variable = os.path.getmtime(link_data+cpt_8 +'/'+cpt_9+'/'+'fixtures_package'+'/'+filename)
                                                                        file_variable = link_data+cpt_8 +'/'+cpt_9+'/'+'fixtures_package'+'/'+filename
                                            if os.path.getmtime(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/' +'fixtures_team_id_s'+ '_'+ str(neighbors_id)+'.pkl')<(datetime.timestamp(datetime.now()-timedelta(seconds=detla_seconds_update))):
                                                if time_variable>(datetime.timestamp(datetime.now()-timedelta(seconds=detla_seconds_update))):
                                                    if file_variable != link_data+str(team_id)+'/'+game_fixture_id+'/'+'fixtures_package'+'/'+"fixtures_team_id_s_" + str(neighbors_id)+ '.pkl':
                                                        copyfile(file_variable,link_data+str(team_id)+'/'+game_fixture_id+'/'+'fixtures_package'+'/'+"fixtures_team_id_s_" + str(neighbors_id)+ '.pkl')
                                                else:
                                                    fixtures_team_id_modified_s(team_id,neighbors_id,game_fixture_id)
                                    except Exception as e:
                                        print(e)

                                    variable_rank_fixtures = output_rank_fixtures_modified(team_id,neighbors_id,neighbors_fixtures,game_fixture_id) # The rank of the current fixture in the list of all team fixtures : past and futures
                                    variable_fixtures = pd.read_pickle(link_data+str(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/' +'fixtures_team_id_s'+ '_'+ str(neighbors_id)+'.pkl') # The list of all fixtures of a team : past and futures

                                    for cpt_1 in range (0,max_future_game_neighbors): 
                                        cpt_5 = 1
                                        while variable_fixtures.iloc[variable_rank_fixtures-cpt_5,variable_fixtures.columns.get_loc('league_id')] != variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('league_id')] and cpt_5<10 :
                                            cpt_5 += 1
                                        try :
                                            if cpt_5 != 10 : # Stop the loop
                                                rounds = str(variable_fixtures.iloc[variable_rank_fixtures-cpt_5,variable_fixtures.columns.get_loc('round')])
                                                league = variable_fixtures.iloc[variable_rank_fixtures-cpt_5,variable_fixtures.columns.get_loc('league_id')]
                                                if int(variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('homeTeam')]['team_id']) == neighbors_id :
                                                    matrix.iloc[i,matrix.columns.get_loc("N+{}_r{}".format(cpt_1,cpt_6))] = output_ranking_extract(rounds,0,league,team_id,variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('awayTeam')]['team_id'])
                                                else :
                                                    matrix.iloc[i,matrix.columns.get_loc("N+{}_r{}".format(cpt_1,cpt_6))] = output_ranking_extract(rounds,0,league,team_id,variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('homeTeam')]['team_id'])
                                            else: 
                                                    matrix.iloc[i,matrix.columns.get_loc("N+{}_r{}".format(cpt_1,cpt_6))] = "STOP"
                                        except:
                                            try:
                                                if int(variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('homeTeam')]['team_id']) == neighbors_id :
                                                    matrix.iloc[i,matrix.columns.get_loc("N+{}_r{}".format(cpt_1,cpt_6))] = variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('awayTeam')]['team_name']
                                                else:
                                                    matrix.iloc[i,matrix.columns.get_loc("N+{}_r{}".format(cpt_1,cpt_6))] = variable_fixtures.iloc[variable_rank_fixtures+cpt_1,variable_fixtures.columns.get_loc('homeTeam')]['team_name']
                                            except:    
                                                matrix.iloc[i,matrix.columns.get_loc("N+{}_r{}".format(cpt_1,cpt_6))] = "No team"
                                except:
                                    for cpt_7 in range (cpt_1,max_future_game_neighbors):
                                        matrix.iloc[i,matrix.columns.get_loc("N+{}_r{}".format(cpt_7,cpt_6))] = "No team"      
                            else:
                                for cpt_1 in range (0,max_future_game_neighbors): 
                                    matrix.iloc[i,matrix.columns.get_loc("N+{}_r{}".format(cpt_1,cpt_6))] = "No team"
                    # End of futur games section for neighbors

                # Start of players lineups section
                variable_lineups = pd.read_pickle(link_data+central_folder+'/'+link_data_package_lineups_central+'/' +'lineups_fixture_id_s'+ '_'+ str(variable_last_fixtures['fixture_id'][i]) +'.pkl') # The variable of the lineup for the fixture
                matrix.iloc[i,matrix.columns.get_loc('formation')] = variable_lineups[team_name]['formation']
                goalkeeper,forward,middlefielder,defender = [],[],[],[]
                for cpt_6 in variable_lineups[team_name]['startXI']:
                    if cpt_6['pos'] == 'F':
                        forward.append(cpt_6['player_id'])    
                    elif cpt_6['pos'] == 'M':
                        middlefielder.append(cpt_6['player_id'])        
                    elif cpt_6['pos'] == 'D':
                        defender.append(cpt_6['player_id'])    
                    else :
                        goalkeeper.append(cpt_6['player_id'])    

                matrix.iloc[i,matrix.columns.get_loc('G')] = goalkeeper
                matrix.iloc[i,matrix.columns.get_loc('F')] = forward
                matrix.iloc[i,matrix.columns.get_loc('M')] = middlefielder
                matrix.iloc[i,matrix.columns.get_loc('D')] = defender
                # End of players lineups section
            
                # Start of players statistics section
                variable_statistics_player = pd.read_pickle(link_data+central_folder+'/'+link_data_package_players_central+'/' +'players_statistics_fixture_id_s'+ '_'+ str(variable_last_fixtures['fixture_id'][i]) +'.pkl') # The variable of the players statistics for a fixture
                cpt_4 = 0
                for cpt_3 in range (len(variable_statistics_player)):
                    if int(variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('team_id')]) == int(team_id) and type(variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('rating')]) != type(None) :
                        cpt_4 += 1
                        acc = 0
                        if int(variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('passes')]['accuracy'])>int(variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('passes')]['total']):
                            acc = int(int(variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('passes')]['accuracy'])*int(variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('passes')]['total'])/100)
                        else:
                            acc = int(variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('passes')]['accuracy'])
                        keys_P = ['player_id','captain','minutes_played','substitute','goals','assists','penalty_commited','red_cards','yellow_cards','passes','passes_acc','rating',"fouls",'shots','shots_on','dribbles','dribbles_w','duels','duels_w','tackles',"csc"]
                        try:
                            minutes = int(variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('minutes_played')])
                        except:
                            minutes = variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('minutes_played')]

                        data_P = [int(variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('player_id')]),variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('captain')],\
                        minutes,variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('substitute')],\
                        variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('goals')]['total'],variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('goals')]['assists'],\
                        variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('penalty')]['commited'],output_red_cards_commited(team_id,team_id,matrix.iloc[i,matrix.columns.get_loc('fixture_id')],\
                        int(variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('player_id')])),output_yellow_cards_commited(team_id,team_id,matrix.iloc[i,matrix.columns.get_loc('fixture_id')],\
                        int(variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('player_id')])),variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('passes')]['total'],\
                        acc,variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('rating')],\
                        variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('fouls')]['committed'],variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('shots')]['total'],\
                        variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('shots')]['on'],variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('dribbles')]['attempts'],\
                        variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('dribbles')]['success'],variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('duels')]['total'],\
                        variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('duels')]['won'],variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('tackles')]['total'],\
                        output_csc(team_id,team_id,variable_last_fixtures['fixture_id'][i],int(variable_statistics_player.iloc[cpt_3,variable_statistics_player.columns.get_loc('player_id')]))[1]]
                        
                        matrix.iloc[i,matrix.columns.get_loc("P{}_stats_mod".format(cpt_4))] = [dict(zip(keys_P,data_P))]
                # End of players statistics section
                i += 1   
            except: 
                i += 1   
            print(i)
        return matrix
    except:
        pass
    
    

'''
Other output functions
------------------------------------------------------------------------------------
'''

def output_ranking(rounds,n,league_id,team_id): # n = 1 then it's ranking before the "rounds", if n = 0 then it's ranking after the "rounds"
    rounds = str(rounds)
    n = int(n)
    
    try:
        try:
            x = int(rounds[-2:])
        except:
            x = int(rounds[-1])
        columns = pd.read_pickle(link_data+central_folder+'/'+link_data_package_teams_central+'/' +'teams_league_id_s'+'_' + str(league_id)+'.pkl')['team_id']
        ranking = {key: [0,0,0,0,0,0,0] for key in columns}
        round_list = pd.read_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/' +'fixturesrounds_league_id_s'+'_' + str(league_id)+'.pkl')
        i = 0
        while i < len(round_list) and i<(x-n): # This is where the "n" parameter is used
            p = str(round_list.iloc[i,0])
            fixtures_list = pd.read_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixtures_league_id_round_s'+ '_'+ str(league_id) +'_' +str(p)+'.pkl')
            for j in range (len(fixtures_list)):
                status = str(fixtures_list.iloc[j,fixtures_list.columns.get_loc('status')])
                home_team_id = fixtures_list.iloc[j,fixtures_list.columns.get_loc('homeTeam')]['team_id']
                home_team_id = fixtures_list.iloc[j,fixtures_list.columns.get_loc('homeTeam')]['team_id']
                home_team_score = fixtures_list.iloc[j,fixtures_list.columns.get_loc('goalsHomeTeam')]
                away_team_id = fixtures_list.iloc[j,fixtures_list.columns.get_loc('awayTeam')]['team_id']
                away_team_score = fixtures_list.iloc[j,fixtures_list.columns.get_loc('goalsAwayTeam')]   
                   
                try: 
                    if status == "Match Finished" :
                        ranking[home_team_id][1] += 1
                        ranking[away_team_id][1] += 1
                        ranking[home_team_id][5] += home_team_score
                        ranking[away_team_id][5] += away_team_score
                        ranking[home_team_id][6] += away_team_score
                        ranking[away_team_id][6] += home_team_score

                        if home_team_score > away_team_score :
                            ranking[home_team_id][0] += 3
                            ranking[home_team_id][2] += 1
                            ranking[away_team_id][4] += 1
                        elif home_team_score < away_team_score :
                            ranking[away_team_id][0] += 3
                            ranking[away_team_id][2] += 1
                            ranking[home_team_id][4] += 1
                        else :
                            ranking[away_team_id][0] += 1
                            ranking[home_team_id][0] += 1
                            ranking[home_team_id][3] += 1
                            ranking[away_team_id][3] += 1
                except: 
                    ranking[away_team_id][0] += 0
                    ranking[home_team_id][0] += 0  
            i += 1    
        ranking = pd.DataFrame.from_dict(ranking).T
        ranking = ranking.rename(columns={0: "rank", 1: "played",2:"W",3:"D",4:"L",5:"BP",6:"BC"})
        ranking = ranking.sort_values(by=["rank"],ascending=False)
        
    except:
        ranking = "No ranking"
    return ranking

def output_neighbors(rounds,n,league_id,team_id,neighbors): # n = 1 then it's ranking before the "rounds", if n = 0 then it's ranking after the "rounds"
    team_id = int(team_id)
    ranking = output_ranking(rounds,n,league_id,team_id)
    variable_leagues = pd.read_pickle(link_data+central_folder+'/'+link_data_package_teams_central+'/' +'teams_league_id_s'+ '_'+ str(league_id)+'.pkl')
    
    try:
        variable_fixtures_round = pd.read_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/' +'fixtures_league_id_round_s'+ '_'+ str(league_id) + '_'+ str(rounds)+'.pkl')
    except:
        rounds = round_formating(rounds)
        variable_fixtures_round = pd.read_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/' +'fixtures_league_id_round_s'+ '_'+ str(league_id) + '_'+ str(rounds)+'.pkl')

    x = 1 + ranking.index.get_loc(team_id)
    k_min = max(1,x-neighbors)
    k_max = min(len(ranking),x+neighbors)
    neighbors = {key: ["x",0,0,0,0,0,0,0,0,0,0] for key in range (k_min, k_max+1)}

    for i in range (k_min,k_max+1):
        if i != x :
            neighbors[i][0] = str(variable_leagues.loc[variable_leagues['team_id'] == ranking.iloc[i-1].name].iloc[0,variable_leagues.loc[variable_leagues['team_id'] == ranking.iloc[i-1].name].columns.get_loc('name')])
            neighbors[i][1] = int(i)
            neighbors[i][2] = int(ranking.iloc[i-1,0])
            neighbors[i][3] = int(ranking.iloc[i-1,1])
            neighbors[i][4] = int(ranking.iloc[i-1,2])
            neighbors[i][5] = int(ranking.iloc[i-1,3])
            neighbors[i][6] = int(ranking.iloc[i-1,4])
            neighbors[i][7] = int(ranking.iloc[i-1,5])
            neighbors[i][8] = int(ranking.iloc[i-1,6])
            for cpt_0 in range (len(variable_fixtures_round)):
                if str(variable_fixtures_round.iloc[cpt_0,variable_fixtures_round.columns.get_loc("awayTeam")]['team_name']) == str(neighbors[i][0]) :
                    neighbors[i][9] = int(variable_fixtures_round.iloc[cpt_0,variable_fixtures_round.columns.get_loc("awayTeam")]['team_id'])
                    neighbors[i][10] = int(variable_fixtures_round.iloc[cpt_0,variable_fixtures_round.columns.get_loc("fixture_id")])
                elif str(variable_fixtures_round.iloc[cpt_0,variable_fixtures_round.columns.get_loc("homeTeam")]['team_name']) == str(neighbors[i][0]) :
                    neighbors[i][9] = int(variable_fixtures_round.iloc[cpt_0,variable_fixtures_round.columns.get_loc("homeTeam")]['team_id'])
                    neighbors[i][10] = int(variable_fixtures_round.iloc[cpt_0,variable_fixtures_round.columns.get_loc("fixture_id")])
    return ranking, neighbors # Difference with output_ranking_extract because returns 2 objects

def output_ranking_extract(rounds,n,league_id,team_id,var_team_id): # n = 1 then it's ranking before the "rounds", if n = 0 then it's ranking after the "rounds"
    
    team_id = int(team_id)
    var_team_id = int(var_team_id)

    ranking = output_ranking(rounds,n,league_id,team_id)
    variable_leagues = pd.read_pickle(link_data+central_folder+'/'+link_data_package_teams_central+'/' +'teams_league_id_s'+ '_'+ str(league_id)+'.pkl')
    x = 1 + ranking.index.get_loc(var_team_id)
    extract = ["x",0,0,0,0,0,0,0,0]
    
    extract[0] = str(variable_leagues.loc[variable_leagues['team_id'] == ranking.iloc[x-1].name].iloc[0,variable_leagues.loc[variable_leagues['team_id'] == ranking.iloc[x-1].name].columns.get_loc('name')])
    extract[1] = int(x)
    extract[2] = int(ranking.iloc[x-1,0])
    extract[3] = int(ranking.iloc[x-1,1])
    extract[4] = int(ranking.iloc[x-1,2])
    extract[5] = int(ranking.iloc[x-1,3])
    extract[6] = int(ranking.iloc[x-1,4])
    extract[7] = int(ranking.iloc[x-1,5])
    extract[8] = int(ranking.iloc[x-1,6])
    return extract # Difference with output_ranking_extract because returns 1 object

'''
Final computation of the output_matrix
------------------------------------------------------------------------------------
'''

def output_players_impact(matrix,i):
    # Declaration of the dicts 
    goalkeeper = {"player_id":"0","#XI":0,"fouls_XI":0,"red_XI":0,"yellow_XI":0,"penalty_XI":0,"cpt_XI":0,"#subs":0,"fouls_subs":0,"red_subs":0,"yellow_subs":0,"penalty_subs":0,"cpt_subs":0}

    defender = {1:{"player_id":"0","#XI":0,"min_XI":0,"fouls_XI":0,"fouls_XI_team%":0,"red_XI":0,"yellow_XI":0,"yellow_team_XI%":0,"penalty_XI":0,"duels_XI":0,"duels_w_XI":0,"tackles_XI":0,"csc_XI":0,"passes_XI":0,"passes_acc_XI%":0,"passes_team_XI%":0,"cpt_XI":0,"#subs":0,"min_subs":0,"fouls_subs":0,"fouls_subs_team%":0,"red_subs":0,"yellow_subs":0,"yellow_team_subs%":0,"penalty_subs":0,"duels_subs":0,"duels_w_subs":0,"tackles_subs":0,"csc_subs":0,"passes_subs":0,"passes_acc_subs%":0,"passes_team_subs%":0,"cpt_subs":0},\
    2:{"player_id":"0","#XI":0,"min_XI":0,"fouls_XI":0,"fouls_XI_team%":0,"red_XI":0,"yellow_XI":0,"yellow_team_XI%":0,"penalty_XI":0,"duels_XI":0,"duels_w_XI":0,"tackles_XI":0,"csc_XI":0,"passes_XI":0,"passes_acc_XI%":0,"passes_team_XI%":0,"cpt_XI":0,"#subs":0,"min_subs":0,"fouls_subs":0,"fouls_subs_team%":0,"red_subs":0,"yellow_subs":0,"yellow_team_subs%":0,"penalty_subs":0,"duels_subs":0,"duels_w_subs":0,"tackles_subs":0,"csc_subs":0,"passes_subs":0,"passes_acc_subs%":0,"passes_team_subs%":0,"cpt_subs":0},\
    3:{"player_id":"0","#XI":0,"min_XI":0,"fouls_XI":0,"fouls_XI_team%":0,"red_XI":0,"yellow_XI":0,"yellow_team_XI%":0,"penalty_XI":0,"duels_XI":0,"duels_w_XI":0,"tackles_XI":0,"csc_XI":0,"passes_XI":0,"passes_acc_XI%":0,"passes_team_XI%":0,"cpt_XI":0,"#subs":0,"min_subs":0,"fouls_subs":0,"fouls_subs_team%":0,"red_subs":0,"yellow_subs":0,"yellow_team_subs%":0,"penalty_subs":0,"duels_subs":0,"duels_w_subs":0,"tackles_subs":0,"csc_subs":0,"passes_subs":0,"passes_acc_subs%":0,"passes_team_subs%":0,"cpt_subs":0},\
    4:{"player_id":"0","#XI":0,"min_XI":0,"fouls_XI":0,"fouls_XI_team%":0,"red_XI":0,"yellow_XI":0,"yellow_team_XI%":0,"penalty_XI":0,"duels_XI":0,"duels_w_XI":0,"tackles_XI":0,"csc_XI":0,"passes_XI":0,"passes_acc_XI%":0,"passes_team_XI%":0,"cpt_XI":0,"#subs":0,"min_subs":0,"fouls_subs":0,"fouls_subs_team%":0,"red_subs":0,"yellow_subs":0,"yellow_team_subs%":0,"penalty_subs":0,"duels_subs":0,"duels_w_subs":0,"tackles_subs":0,"csc_subs":0,"passes_subs":0,"passes_acc_subs%":0,"passes_team_subs%":0,"cpt_subs":0},\
    5:{"player_id":"0","#XI":0,"min_XI":0,"fouls_XI":0,"fouls_XI_team%":0,"red_XI":0,"yellow_XI":0,"yellow_team_XI%":0,"penalty_XI":0,"duels_XI":0,"duels_w_XI":0,"tackles_XI":0,"csc_XI":0,"passes_XI":0,"passes_acc_XI%":0,"passes_team_XI%":0,"cpt_XI":0,"#subs":0,"min_subs":0,"fouls_subs":0,"fouls_subs_team%":0,"red_subs":0,"yellow_subs":0,"yellow_team_subs%":0,"penalty_subs":0,"duels_subs":0,"duels_w_subs":0,"tackles_subs":0,"csc_subs":0,"passes_subs":0,"passes_acc_subs%":0,"passes_team_subs%":0,"cpt_subs":0}} 
    defender_together = {"#games":0,"BC":0,"fouls":0,"red":0,"yellow":0,"penalty":0}

    middlefielder = {1:{"player_id":"0","#XI":0,"min_XI":0,"goals_XI":0,"assists_XI":0,"passes_XI_team%":0,"passes_acc_XI%":0,"shots_XI":0,"shots_on_XI":0,"dribbles_XI":0,"dribbles_w_XI":0,"duels_XI":0,"duels_w_XI":0,"cpt_XI":0,"calc1":0,"fouls_team_XI":0,"shots_team_XI":0,"fouls_XI":0,"BP_indirect_XI":0,"#subs":0,"min_subs":0,"goals_subs":0,"assists_subs":0,"passes_subs_team%":0,"passes_acc_subs%":0,"shots_subs":0,"shots_on_subs":0,"dribbles_subs":0,"dribbles_w_subs":0,"duels_subs":0,"duels_w_subs":0,"cpt_subs":0,"calc2":0,"fouls_team_XI":0,"shots_team_XI":0,"fouls_subs":0,"BP_indirect_subs":0},\
    2:{"player_id":"0","#XI":0,"min_XI":0,"goals_XI":0,"assists_XI":0,"passes_XI_team%":0,"passes_acc_XI%":0,"shots_XI":0,"shots_on_XI":0,"dribbles_XI":0,"dribbles_w_XI":0,"duels_XI":0,"duels_w_XI":0,"cpt_XI":0,"calc1":0,"fouls_team_XI":0,"shots_team_XI":0,"fouls_XI":0,"BP_indirect_XI":0,"#subs":0,"min_subs":0,"goals_subs":0,"assists_subs":0,"passes_subs_team%":0,"passes_acc_subs%":0,"shots_subs":0,"shots_on_subs":0,"dribbles_subs":0,"dribbles_w_subs":0,"duels_subs":0,"duels_w_subs":0,"cpt_subs":0,"calc2":0,"fouls_team_XI":0,"shots_team_XI":0,"fouls_subs":0,"BP_indirect_subs":0},\
    3:{"player_id":"0","#XI":0,"min_XI":0,"goals_XI":0,"assists_XI":0,"passes_XI_team%":0,"passes_acc_XI%":0,"shots_XI":0,"shots_on_XI":0,"dribbles_XI":0,"dribbles_w_XI":0,"duels_XI":0,"duels_w_XI":0,"cpt_XI":0,"calc1":0,"fouls_team_XI":0,"shots_team_XI":0,"fouls_XI":0,"BP_indirect_XI":0,"#subs":0,"min_subs":0,"goals_subs":0,"assists_subs":0,"passes_subs_team%":0,"passes_acc_subs%":0,"shots_subs":0,"shots_on_subs":0,"dribbles_subs":0,"dribbles_w_subs":0,"duels_subs":0,"duels_w_subs":0,"cpt_subs":0,"calc2":0,"fouls_team_XI":0,"shots_team_XI":0,"fouls_subs":0,"BP_indirect_subs":0},\
    4:{"player_id":"0","#XI":0,"min_XI":0,"goals_XI":0,"assists_XI":0,"passes_XI_team%":0,"passes_acc_XI%":0,"shots_XI":0,"shots_on_XI":0,"dribbles_XI":0,"dribbles_w_XI":0,"duels_XI":0,"duels_w_XI":0,"cpt_XI":0,"calc1":0,"fouls_team_XI":0,"shots_team_XI":0,"fouls_XI":0,"BP_indirect_XI":0,"#subs":0,"min_subs":0,"goals_subs":0,"assists_subs":0,"passes_subs_team%":0,"passes_acc_subs%":0,"shots_subs":0,"shots_on_subs":0,"dribbles_subs":0,"dribbles_w_subs":0,"duels_subs":0,"duels_w_subs":0,"cpt_subs":0,"calc2":0,"fouls_team_XI":0,"shots_team_XI":0,"fouls_subs":0,"BP_indirect_subs":0},\
    5:{"player_id":"0","#XI":0,"min_XI":0,"goals_XI":0,"assists_XI":0,"passes_XI_team%":0,"passes_acc_XI%":0,"shots_XI":0,"shots_on_XI":0,"dribbles_XI":0,"dribbles_w_XI":0,"duels_XI":0,"duels_w_XI":0,"cpt_XI":0,"calc1":0,"fouls_team_XI":0,"shots_team_XI":0,"fouls_XI":0,"BP_indirect_XI":0,"#subs":0,"min_subs":0,"goals_subs":0,"assists_subs":0,"passes_subs_team%":0,"passes_acc_subs%":0,"shots_subs":0,"shots_on_subs":0,"dribbles_subs":0,"dribbles_w_subs":0,"duels_subs":0,"duels_w_subs":0,"cpt_subs":0,"calc2":0,"fouls_team_XI":0,"shots_team_XI":0,"fouls_subs":0,"BP_indirect_subs":0}} 
    middlefielder_together = {"#games":0,"poss":0,"passes_tot":0,"passes_acc%":0} 

    forward = {1:{"player_id":"0","#XI":0,"min_XI":0,"goals_XI":0,"assists_XI":0,"shots_XI":0,"shots_on_XI":0,"dribbles_XI":0,"dribbles_w_XI":0,"cpt_XI":0,"#subs":0,"min_subs":0,"goals_subs":0,"assists_subs":0,"shots_subs":0,"shots_on_subs":0,"dribbles_subs":0,"dribbles_w_subs":0,"cpt_subs":0},\
    2:{"player_id":"0","#XI":0,"min_XI":0,"goals_XI":0,"assists_XI":0,"shots_XI":0,"shots_on_XI":0,"dribbles_XI":0,"dribbles_w_XI":0,"cpt_XI":0,"#subs":0,"min_subs":0,"goals_subs":0,"assists_subs":0,"shots_subs":0,"shots_on_subs":0,"dribbles_subs":0,"dribbles_w_subs":0,"cpt_subs":0},\
    3:{"player_id":"0","#XI":0,"min_XI":0,"goals_XI":0,"assists_XI":0,"shots_XI":0,"shots_on_XI":0,"dribbles_XI":0,"dribbles_w_XI":0,"cpt_XI":0,"#subs":0,"min_subs":0,"goals_subs":0,"assists_subs":0,"shots_subs":0,"shots_on_subs":0,"dribbles_subs":0,"dribbles_w_subs":0,"cpt_subs":0}} 
    forward_together = {"#games":0,"BP":0,"shots":0} 

    # Construction of the goalkeeper dict
    try:
        if len(matrix.iloc[i,matrix.columns.get_loc('G')])> 0:
            goalkeeper['player_id'] = int(matrix.iloc[i,matrix.columns.get_loc('G')][0])
    except:
        print("error with goalkeeper id, for i: {}, and game round: {}".format(i,matrix.iloc[i,matrix.columns.get_loc('round')]))

    # Construction of the defender dict
    try:    
        if len(matrix.iloc[i,matrix.columns.get_loc('D')])> 0:
            for cpt_0 in range (len(matrix.iloc[i,matrix.columns.get_loc('D')])):
                defender[cpt_0+1]['player_id'] = int(matrix.iloc[i,matrix.columns.get_loc('D')][cpt_0])
    except:
        print("too many defenders, for i: {}, and game round: {}".format(i,matrix.iloc[i,matrix.columns.get_loc('round')])) 

    # Construction of the middlefielder dict
    try:
        if len(matrix.iloc[i,matrix.columns.get_loc('M')])> 0:
            for cpt_0 in range (len(matrix.iloc[i,matrix.columns.get_loc('M')])):
                middlefielder[cpt_0+1]['player_id'] = int(matrix.iloc[i,matrix.columns.get_loc('M')][cpt_0])
    except:
        print("too many middlefielders, for i: {}, and game round: {}".format(i,matrix.iloc[i,matrix.columns.get_loc('round')])) 

    # Construction of the forward dict
    try:
        if len(matrix.iloc[i,matrix.columns.get_loc('F')])> 0:
            for cpt_0 in range (len(matrix.iloc[i,matrix.columns.get_loc('F')])):
                forward[cpt_0+1]['player_id'] = int(matrix.iloc[i,matrix.columns.get_loc('F')][cpt_0])
    except:
        print("too many forwards, for i: {}, and game round: {}".format(i,matrix.iloc[i,matrix.columns.get_loc('round')])) 
    
    # Calculation of the dicts
    cpt_1 = i
    while cpt_1<last_fixtures_lineups_duration-1: 
        nb_D = 0
        nb_M = 0
        nb_F = 0
        for cpt_3 in range (matrix.columns.get_loc("P1_stats_mod"),matrix.columns.get_loc("P16_stats_mod")+1):
            x_0 = matrix.iloc[cpt_1 + 1,cpt_3]
            if type(x_0) == type([]):
                x = x_0[0] # Converting the lsit into a dict with taking only the first element
                try: 
                    if int(x['player_id']) == goalkeeper['player_id']:
                        if x['substitute'] == "False" and goalkeeper["cpt_XI"]<significant_games:
                            if cpt_1-i < time_players_impact: # Counting only if it was a game during the last 5 games (time_players_impact)
                                goalkeeper['#XI'] += 1
                            if type(x['fouls']) == type(1):
                                goalkeeper['fouls_XI'] += int(x['fouls'])
                            if type(x['red_cards']) == type(1):
                                goalkeeper['red_XI'] += int(x['red_cards'])
                            if type(x['yellow_cards']) == type(1):
                                goalkeeper['yellow_XI'] += int(x['yellow_cards'])
                            if type(x['penalty_commited']) == type(1):  
                                goalkeeper['penalty_XI'] += int(x['penalty_commited'])
                            goalkeeper["cpt_XI"] += 1
                        if x['substitute'] == "True" and goalkeeper["cpt_subs"]<significant_games:
                            if cpt_1-i < time_players_impact: # To be checked
                                goalkeeper['#subs'] += 1
                            if type(x['fouls']) == type(1):
                                goalkeeper['fouls_subs'] += int(x['fouls'])
                            if type(x['red_subs']) == type(1):
                                goalkeeper['red_subs'] += int(x['red_cards'])
                            if type(x['yellow_cards']) == type(1):
                                goalkeeper['yellow_subs'] += int(x['yellow_cards'])
                            if type(x['penalty_commited']) == type(1):  
                                goalkeeper['penalty_subs'] += int(x['penalty_commited'])     
                            goalkeeper["cpt_subs"] += 1 
                    else: 
                        for d in defender.values():
                            if int(x['player_id']) == d['player_id'] :
                                nb_D += 1
                                if x['substitute'] == "False" and d["cpt_XI"]<significant_games:
                                    if cpt_1-i < time_players_impact: # To be checked
                                        d['#XI'] += 1
                                    if type(x['minutes_played']) == type(1) or type(x['minutes_played']) == type(1.5) :
                                        d["min_XI"] += int(x['minutes_played']) 
                                    if type(x['fouls']) == type(1):
                                        d["fouls_XI"] += int(x['fouls']) 
                                    if type(matrix.iloc[cpt_1 + 1,matrix.columns.get_loc('fouls_team')]) == type(1):
                                        d["fouls_XI_team%"] += int(matrix.iloc[cpt_1 + 1,matrix.columns.get_loc('fouls_team')])
                                    if type(x['red_cards']) == type(1):
                                        d["red_XI"] += int(x['red_cards'])
                                    if type(x['yellow_cards']) == type(1):
                                        d["yellow_XI"] += int(x['yellow_cards']) 
                                    if type(x['penalty_commited']) == type(1):
                                        d["penalty_XI"] += int(x['penalty_commited']) 
                                    if type(x['duels']) == type(1):
                                        d["duels_XI"] += int(x['duels'])
                                    if type(x['duels_w']) == type(1):
                                        d["duels_w_XI"] += int(x['duels_w'])
                                    if type(x['tackles']) == type(1):
                                        d["tackles_XI"] += int(x['tackles']) 
                                    if type(x['csc']) == type(1):
                                        d["csc_XI"] += int(x['csc'])
                                    if type(x['passes']) == type(1):
                                        d["passes_XI"] += int(x['passes'])
                                    if type(x['passes_acc']) == type(1):
                                        d["passes_acc_XI%"] += int(x['passes_acc'])
                                    if type(matrix.iloc[cpt_1+1,matrix.columns.get_loc('passes_total_team')]) == type(1):
                                        d["passes_team_XI%"] += matrix.iloc[cpt_1+1,matrix.columns.get_loc('passes_total_team')]
                                    if type(matrix.iloc[cpt_1+1,matrix.columns.get_loc('yellow_team')]) == type(1):
                                        d["yellow_team_XI%"] += matrix.iloc[cpt_1+1,matrix.columns.get_loc('yellow_team')]
                                    
                                    d["cpt_XI"] += 1

                                if x['substitute'] == "True" and d["cpt_subs"] < significant_games:
                                    if cpt_1-i < time_players_impact: # To be checked
                                        d['#subs'] += 1
                                    if type(x['minutes_played']) == type(1) or type(x['minutes_played']) == type(1.5) :
                                        d["min_subs"] += int(x['minutes_played']) 
                                    if type(x['fouls']) == type(1):
                                        d["fouls_subs"] += int(x['fouls']) 
                                    if type(matrix.iloc[cpt_1 + 1,matrix.columns.get_loc('fouls_team')]) == type(1):
                                        d["fouls_subs_team%"] += int(matrix.iloc[cpt_1 + 1,matrix.columns.get_loc('fouls_team')])
                                    if type(x['red_cards']) == type(1):
                                        d["red_subs"] += int(x['red_cards'])
                                    if type(x['yellow_cards']) == type(1):
                                        d["yellow_subs"] += int(x['yellow_cards']) 
                                    if type(x['penalty_commited']) == type(1):
                                        d["penalty_subs"] += int(x['penalty_commited']) 
                                    if type(x['duels']) == type(1):
                                        d["duels_subs"] += int(x['duels'])
                                    if type(x['duels_w']) == type(1):
                                        d["duels_w_subs"] += int(x['duels_w'])
                                    if type(x['tackles']) == type(1):
                                        d["tackles_subs"] += int(x['tackles']) 
                                    if type(x['csc']) == type(1):
                                        d["csc_subs"] += int(x['csc'])
                                    if type(x['passes']) == type(1):
                                        d["passes_subs"] += int(x['passes'])
                                    if type(x['passes_acc']) == type(1):
                                        d["passes_acc_subs%"] += int(x['passes_acc'])
                                    if type(x['passes_acc']) == type(1):
                                        d["passes_acc_subs%"] += int(x['passes_acc'])
                                    if type(matrix.iloc[cpt_1+1,matrix.columns.get_loc('passes_total_team')]) == type(1):
                                        d["passes_team_subs%"] += matrix.iloc[cpt_1+1,matrix.columns.get_loc('passes_total_team')]
                                    if type(matrix.iloc[cpt_1+1,matrix.columns.get_loc('yellow_team')]) == type(1):
                                        d["yellow_team_subs%"] += matrix.iloc[cpt_1+1,matrix.columns.get_loc('yellow_team')]

                                    d["cpt_subs"] += 1

                        for m in middlefielder.values():
                            if int(x['player_id']) == m['player_id'] :
                                nb_M += 1
                                if x['substitute'] == "False" and m["cpt_XI"]<significant_games:
                                    if cpt_1-i < time_players_impact: # To be checked
                                        m['#XI'] += 1
                                    if type(x['minutes_played']) == type(1) or type(x['minutes_played']) == type(1.5) :
                                        m["min_XI"] += int(x['minutes_played']) 
                                    if type(x['goals']) == type(1):
                                        m["goals_XI"] += int(x['goals']) 
                                    if type(x['assists']) == type(1):
                                        m["assists_XI"] += int(x['assists'])
                                    if type(x['passes']) == type(1):
                                        m["passes_XI_team%"] += int(x['passes'])
                                    if type(x['passes_acc']) == type(1):
                                        m["passes_acc_XI%"] += int(x['passes_acc']) 
                                    if type(x['fouls']) == type(1):
                                        m["fouls_XI"] += int(x['fouls']) 
                                    if type(x['shots']) == type(1):
                                        m["shots_XI"] += int(x['shots']) 
                                    if type(x['shots_on']) == type(1):
                                        m["shots_on_XI"] += int(x['shots_on'])
                                    if type(x['dribbles']) == type(1):
                                        m["dribbles_XI"] += int(x['dribbles'])
                                    if type(x['dribbles_w']) == type(1):
                                        m["dribbles_w_XI"] += int(x['dribbles_w']) 
                                    if type(x['duels']) == type(1):
                                        m["duels_XI"] += int(x['duels'])
                                    if type(x['duels_w']) == type(1):
                                        m["duels_w_XI"] += int(x['duels_w'])
                                    if type(matrix.iloc[cpt_1+1,matrix.columns.get_loc('passes_total_team')]) == type(1):
                                        m["calc1"] += int(matrix.iloc[cpt_1+1,matrix.columns.get_loc('passes_total_team')])
                                    if type(matrix.iloc[cpt_1+1,matrix.columns.get_loc('shots_team')]) == type(1):
                                        m["shots_team_XI"] += int(matrix.iloc[cpt_1+1,matrix.columns.get_loc('shots_team')])
                                    if type(matrix.iloc[cpt_1+1,matrix.columns.get_loc('fouls_team')]) == type(1):
                                        m["fouls_team_XI"] += int(matrix.iloc[cpt_1+1,matrix.columns.get_loc('fouls_team')])
                                    if type(matrix.iloc[cpt_1+1,matrix.columns.get_loc('BP')]) == type(1):
                                        m["BP_indirect_XI"] += (int(matrix.iloc[cpt_1+1,matrix.columns.get_loc('BP')])-int(matrix.iloc[cpt_1+1,matrix.columns.get_loc('BP_direct')]))

                                    m["cpt_XI"] += 1
                                if x['substitute'] == "True" and m["cpt_subs"]<significant_games:
                                    if cpt_1-i < time_players_impact: # To be checked
                                        m['#subs'] += 1
                                    if type(x['minutes_played']) == type(1) or type(x['minutes_played']) == type(1.5) :
                                        m["min_subs"] += int(x['minutes_played']) 
                                    if type(x['goals']) == type(1):
                                        m["goals_subs"] += int(x['goals']) 
                                    if type(x['assists']) == type(1):
                                        m["assists_subs"] += int(x['assists'])
                                    if type(x['passes']) == type(1):
                                        m["passes_subs_team%"] += int(x['passes'])
                                    if type(x['passes_acc']) == type(1):
                                        m["passes_acc_subs%"] += int(x['passes_acc']) 
                                    if type(x['fouls']) == type(1):
                                        m["fouls_subs"] += int(x['fouls']) 
                                    if type(x['shots']) == type(1):
                                        m["shots_subs"] += int(x['shots']) 
                                    if type(x['shots_on']) == type(1):
                                        m["shots_on_subs"] += int(x['shots_on'])
                                    if type(x['dribbles']) == type(1):
                                        m["dribbles_subs"] += int(x['dribbles'])
                                    if type(x['dribbles_w']) == type(1):
                                        m["dribbles_w_subs"] += int(x['dribbles_w']) 
                                    if type(x['duels']) == type(1):
                                        m["duels_subs"] += int(x['duels'])
                                    if type(x['duels_w']) == type(1):
                                        m["duels_w_subs"] += int(x['duels_w'])
                                    if type(matrix.iloc[cpt_1 + 1,matrix.columns.get_loc('passes_total_team')]) == type(1):
                                        m["calc2"] += int(matrix.iloc[cpt_1 + 1,matrix.columns.get_loc('passes_total_team')])
                                    if type(matrix.iloc[cpt_1+1,matrix.columns.get_loc('shots_team')]) == type(1):
                                        m["shots_team_subs"] += int(matrix.iloc[cpt_1+1,matrix.columns.get_loc('shots_team')])
                                    if type(matrix.iloc[cpt_1+1,matrix.columns.get_loc('fouls_team')]) == type(1):
                                        m["fouls_team_subs"] += int(matrix.iloc[cpt_1+1,matrix.columns.get_loc('fouls_team')])
                                    if type(matrix.iloc[cpt_1+1,matrix.columns.get_loc('BP')]) == type(1):
                                        m["BP_indirect_subs"] += (int(matrix.iloc[cpt_1+1,matrix.columns.get_loc('BP')])-int(matrix.iloc[cpt_1+1,matrix.columns.get_loc('BP_direct')]))

                                    m["cpt_subs"] += 1
                        for f in forward.values():
                            if int(x['player_id']) == f['player_id'] :
                                nb_F += 1
                                if x['substitute'] == "False" and f["cpt_XI"]<significant_games:
                                    if cpt_1-i < time_players_impact: # To be checked
                                        f['#XI'] += 1
                                    if type(x['minutes_played']) == type(1) or type(x['minutes_played']) == type(1.5):
                                        f["min_XI"] += int(x['minutes_played']) 
                                    if type(x['goals']) == type(1):
                                        f["goals_XI"] += int(x['goals']) 
                                    if type(x['assists']) == type(1):
                                        f["assists_XI"] += int(x['assists'])
                                    if type(x['shots']) == type(1):
                                        f["shots_XI"] += int(x['shots']) 
                                    if type(x['shots_on']) == type(1):
                                        f["shots_on_XI"] += int(x['shots_on'])
                                    if type(x['dribbles']) == type(1):
                                        f["dribbles_XI"] += int(x['dribbles'])
                                    if type(x['dribbles_w']) == type(1):
                                        f["dribbles_w_XI"] += int(x['dribbles_w']) 
                                    if type(matrix.iloc[cpt_1 + 1,matrix.columns.get_loc('BP')]) == type(1):
                                        f["BP_XI"] += int(matrix.iloc[cpt_1 + 1,matrix.columns.get_loc('BP')])
                                    if type(matrix.iloc[cpt_1+1,matrix.columns.get_loc('BP')]) == type(1):
                                        f["BP_indirect_XI"] += (int(matrix.iloc[cpt_1+1,matrix.columns.get_loc('BP')])-int(matrix.iloc[cpt_1+1,matrix.columns.get_loc('BP_direct')]))
                                    if type(matrix.iloc[cpt_1 + 1,matrix.columns.get_loc('shots_team')]) == type(1):
                                        f["shots_team_XI"] += int(matrix.iloc[cpt_1 + 1,matrix.columns.get_loc('shots_team')])

                                    f["cpt_XI"] += 1
                                if x['substitute'] == "True" and f["cpt_subs"]<significant_games:
                                    if cpt_1-i < time_players_impact: # To be checked
                                        f['#subs'] += 1
                                    if type(x['minutes_played']) == type(1) or type(x['minutes_played']) == type(1.5):
                                        f["min_subs"] += int(x['minutes_played']) 
                                    if type(x['goals']) == type(1):
                                        f["goals_subs"] += int(x['goals']) 
                                    if type(x['assists']) == type(1):
                                        f["assists_subs"] += int(x['assists'])
                                    if type(x['shots']) == type(1):
                                        f["shots_subs"] += int(x['shots']) 
                                    if type(x['shots_on']) == type(1):
                                        f["shots_on_subs"] += int(x['shots_on'])
                                    if type(x['dribbles']) == type(1):
                                        f["dribbles_subs"] += int(x['dribbles'])
                                    if type(x['dribbles_w']) == type(1):
                                        f["dribbles_w_subs"] += int(x['dribbles_w']) 
                                    if type(matrix.iloc[cpt_1 + 1,matrix.columns.get_loc('BP')]) == type(1):
                                        f["BP_subs"] += int(matrix.iloc[cpt_1 + 1,matrix.columns.get_loc('BP')])
                                    if type(matrix.iloc[cpt_1+1,matrix.columns.get_loc('BP')]) == type(1):
                                        f["BP_indirect_subs"] += (int(matrix.iloc[cpt_1+1,matrix.columns.get_loc('BP')])-int(matrix.iloc[cpt_1+1,matrix.columns.get_loc('BP_direct')]))
                                    if type(matrix.iloc[cpt_1 + 1,matrix.columns.get_loc('shots_team')]) == type(1):
                                        f["shots_team_subs"] += int(matrix.iloc[cpt_1 + 1,matrix.columns.get_loc('shots_team')])
                                    f["cpt_subs"] += 1
                except:
                    print("no player id for i, cpt_1, cpt_3:{},{},{}".format(i,cpt_1,cpt_3))
        # Calclulation of the together
        if nb_D>2 and defender_together['#games']<significant_games:
            defender_together['#games'] += 1
            defender_together['BC'] += int(matrix.iloc[cpt_1 + 1,matrix.columns.get_loc('BC')])
            defender_together['fouls'] += int(matrix.iloc[cpt_1 + 1,matrix.columns.get_loc('fouls_team')])
            defender_together['red'] += int(matrix.iloc[cpt_1 + 1,matrix.columns.get_loc('red_team')])
            defender_together['yellow'] += int(matrix.iloc[cpt_1 + 1,matrix.columns.get_loc('yellow_team')])
            defender_together['penalty'] += int(matrix.iloc[cpt_1 + 1,matrix.columns.get_loc('Penalty_comm_team')])

        if nb_M>2 and middlefielder_together['#games']<significant_games: 
            middlefielder_together['#games'] += 1
            middlefielder_together['poss'] += int(matrix.iloc[cpt_1 + 1,matrix.columns.get_loc("Poss team")])
            middlefielder_together['passes_tot'] += int(matrix.iloc[cpt_1 + 1,matrix.columns.get_loc('passes_total_team')])
            middlefielder_together["passes_acc%"] += int(matrix.iloc[cpt_1 + 1,matrix.columns.get_loc('passes_acc_team')])
        
        if nb_F>1 and forward_together['#games']<significant_games:
            forward_together['#games'] += 1
            forward_together['BP'] += int(matrix.iloc[cpt_1+1,matrix.columns.get_loc('BP')])
            forward_together['shots'] += int(matrix.iloc[cpt_1+1,matrix.columns.get_loc('shots_team')])
        
        cpt_1 += 1

    # Re calculation of the defender
    for d in defender.values():
        if d['duels_XI'] != 0:
            d['duels_w_XI'] = int(100*round(d['duels_w_XI']/d['duels_XI'],2)) # CRITERIA % of duels won by player
        if d['passes_XI'] != 0:
            d['passes_acc_XI%'] = int(100*round(d['passes_acc_XI%']/d['passes_XI'],2)) # CRITERIA % of passes won by player
        if d['passes_team_XI%'] != 0:
            d['passes_team_XI%'] = int(100*round(d['passes_XI']/d['passes_team_XI%'],2)) # CRITERIA % of passes vs. team passes
        if d['yellow_team_XI%'] != 0:
            d["yellow_team_XI%"] = int(100*round(d['yellow_XI']/d['yellow_team_XI%'],2)) # CRITERIA % of yellow vs. team yellow
        if d['fouls_XI_team%'] != 0: 
                d['fouls_XI_team%'] = int(100*round(d['fouls_XI']/d['fouls_XI_team%'],2)) # CRITERIA % of fouls vs. team fouls  

        if d['duels_subs'] != 0:
            d['duels_w_subs'] = int(100*round(d['duels_w_subs']/d['duels_subs'],2)) # CRITERIA % of duels won by player
        if d['passes_subs'] != 0:
            d['passes_acc_subs%'] = int(100*round(d['passes_acc_subs%']/d['passes_subs'],2)) # CRITERIA % of passes won by player
        if d['passes_team_subs%'] != 0:
            d['passes_team_subs%'] = int(100*round(d['passes_subs']/d['passes_team_subs%'],2)) # CRITERIA % of passes vs. team passes
        if d['yellow_team_subs%'] != 0:
            d["yellow_team_subs%"] = int(100*round(d['yellow_subs']/d['yellow_team_subs%'],2)) # CRITERIA % of yellow vs. team yellow
        if d['fouls_subs_team%'] != 0: 
                d['fouls_subs_team%'] = int(100*round(d['fouls_subs']/d['fouls_subs_team%'],2)) # CRITERIA % of fouls vs. team fouls  

        if d['cpt_XI'] != 0: 
            d['min_XI'] = round(d['min_XI']/d['cpt_XI'],2)  
            d['fouls_XI'] = round(d['fouls_XI']/d['cpt_XI'],2)
            d['red_XI'] = round(d['red_XI']/d['cpt_XI'],2)
            d['yellow_XI'] = round(d['yellow_XI']/d['cpt_XI'],2)
            d['penalty_XI'] = round(d['penalty_XI']/d['cpt_XI'],2)
            d['duels_XI'] = round(d['duels_XI']/d['cpt_XI'],2)
            d['tackles_XI'] = round(d['tackles_XI']/d['cpt_XI'],2)
            d['csc_XI'] = round(d['csc_XI']/d['cpt_XI'],2)
        
        if d['cpt_subs'] != 0: 
            d['min_subs'] = round(d['min_subs']/d['cpt_subs'],2)           
            d['fouls_subs'] = round(d['fouls_subs']/d['cpt_subs'],2)
            d['red_subs'] = round(d['red_subs']/d['cpt_subs'],2)
            d['yellow_subs'] = round(d['yellow_subs']/d['cpt_subs'],2)
            d['penalty_subs'] = round(d['penalty_subs']/d['cpt_subs'],2)
            d['duels_subs'] = round(d['duels_subs']/d['cpt_subs'],2)
            d['tackles_subs'] = round(d['tackles_subs']/d['cpt_subs'],2)
            d['csc_subs'] = round(d['csc_subs']/d['cpt_subs'],2)

    # Re calculation of the middlefielder
    for m in middlefielder.values():
        
        if m['passes_XI_team%'] != 0:
            m['passes_acc_XI%'] = int(100*round(m['passes_acc_XI%']/m['passes_XI_team%'],2)) # CRITERIA % of accurate passes %
        if m['calc1'] != 0:
            m['passes_XI_team%'] = int(100*round(m['passes_XI_team%']/m['calc1'],2)) # CRITERIA % of passes vs. team
        if m["BP_indirect_XI"] != 0:
            m["assists_XI"] = int(100*round(m["assists_XI"]/m["BP_indirect_XI"],2)) # CRITERIA % of assists
        if m['shots_team_XI'] != 0:
            m['shots_XI'] = int(100*round(m['shots_XI']/m['shots_team_XI'],2)) # CRITERIA % of shots vs. team
        if m['fouls_team'] != 0:
            m['fouls_XI'] = int(100*round(m['fouls_XI']/m['fouls_team'],2)) # CRITERIA % of fouls vs. team

        if m['passes_subs_team%'] != 0:
            m['passes_acc_subs%'] = int(100*round(m['passes_acc_subs%']/m['passes_subs_team%'],2)) # CRITERIA % of accurate passes %
        if m['calc2'] != 0:
            m['passes_subs_team%'] = int(100*round(m['passes_subs_team%']/m['calc2'],2)) # CRITERIA % of passes vs. team
        if m["BP_indirect_subs"] != 0:
            m["assists_subs"] = int(100*round(m["assists_subs"]/m["BP_indirect_subs"],2)) # CRITERIA % of assists
        if m['shots_team_subs'] != 0:
            m['shots_subs'] = int(100*round(m['shots_subs']/m['shots_team_subs'],2)) # CRITERIA % of shots vs. team
        if m['fouls_team'] != 0:
            m['fouls_subs'] = int(100*round(m['fouls_subs']/m['fouls_team'],2)) # CRITERIA % of fouls vs. team
        
        if m['cpt_XI'] != 0: 
            m['min_XI'] = round(m['min_XI']/m['cpt_XI'],2)
            m['goals_XI'] = round(m['goals_XI']/m['cpt_XI'],2)
            m['dribbles_XI'] = round(m['dribbles_XI']/m['cpt_XI'],2)
            m['dribbles_w_XI'] = round(m['dribbles_w_XI']/m['cpt_XI'],2)
            m['duels_XI'] = round(m['duels_XI']/m['cpt_XI'],2)
            m['duels_w_XI'] = round(m['duels_w_XI']/m['cpt_XI'],2)
        if m['cpt_subs'] != 0: 
            m['min_subs'] = round(m['min_subs']/m['cpt_subs'],2)
            m['goals_subs'] = round(m['goals_subs']/m['cpt_subs'],2)
            m['dribbles_subs'] = round(m['dribbles_subs']/m['cpt_subs'],2)
            m['dribbles_w_subs'] = round(m['dribbles_w_subs']/m['cpt_subs'],2)
            m['duels_subs'] = round(m['duels_subs']/m['cpt_subs'],2)
            m['duels_w_subs'] = round(m['duels_w_subs']/m['cpt_subs'],2)
    
    data_middlefielder = []
    for m in middlefielder.values():
        little_keys = []
        little_data = []
        for x in m.keys():
            if x[:4] != "calc" :
                little_keys.append(x)
                little_data.append(m[x])
        data_middlefielder.append(dict(zip(little_keys,little_data)))
    middlefielder = dict(zip(middlefielder.keys(),data_middlefielder))

    # Re calculation of the forward
    for f in forward.values():
        
        if f['BP_XI'] != 0:
            f['goals_XI'] = int(100*round(f['goals_XI']/f['BP_XI'],2)) # CRITERIA % of goal vs. team
        if f["BP_indirect_XI"] != 0:
            f["assists_XI"] = int(100*round(f["assists_XI"]/f["BP_indirect_XI"],2)) # CRITERIA % of assists
        if f["dribbles_XI"] != 0:
            f["dribbles_w_XI"] = int(100*round(f["dribbles_w_XI"]/f["dribbles_XI"],2)) # CRITERIA % of dribbles
        if f['shots_XI'] != 0:
            f['shots_on_XI'] = int(100*round(f['shots_on_XI']/f['shots_XI'],2)) # CRITERIA % of shots vs. team     
        if f['shots_team_XI'] != 0:
            f['shots_XI'] = int(100*round(f['shots_XI']/f['shots_team_XI'],2)) # CRITERIA % of shots vs. team

        if f['BP_subs'] != 0:
            f['goals_subs'] = int(100*round(f['goals_subs']/f['BP_subs'],2)) # CRITERIA % of goal vs. team
        if f["BP_indirect_subs"] != 0:
            f["assists_subs"] = int(100*round(f["assists_subs"]/f["BP_indirect_subs"],2)) # CRITERIA % of assists
        if f["dribbles_subs"] != 0:
            f["dribbles_w_subs"] = int(100*round(f["dribbles_w_subs"]/f["dribbles_subs"],2)) # CRITERIA % of dribbles
        if f['shots_subs'] != 0:
            f['shots_on_XI'] = int(100*round(f['shots_on_XI']/f['shots_subs'],2)) # CRITERIA % of shots vs. team
        if f['shots_team_subs'] != 0:
            f['shots_subs'] = int(100*round(f['shots_subs']/f['shots_team_subs'],2)) # CRITERIA % of shots vs. team

        if f['cpt_XI'] != 0: 
            f['min_XI'] = round(f['min_XI']/f['cpt_XI'],2)
        if f['cpt_subs'] != 0: 
            f['min_subs'] = round(f['min_subs']/f['cpt_subs'],2)

    # Re calculations of the togethers
    if defender_together['#games'] != 0:
        defender_together['BC'] = round(defender_together['BC']/defender_together['#games'],2)
        defender_together['fouls'] = round(defender_together['fouls']/defender_together['#games'],2)
        defender_together['red'] = round(defender_together['red']/defender_together['#games'],2)
        defender_together['yellow'] = round(defender_together['yellow']/defender_together['#games'],2)
        defender_together['penalty'] = round(defender_together['penalty']/defender_together['#games'],2) 
    if middlefielder_together['#games'] != 0:
        middlefielder_together['poss'] = round(middlefielder_together['poss']/middlefielder_together['#games'],2) 
        middlefielder_together['passes_acc%'] = round(middlefielder_together['passes_acc%']/middlefielder_together['passes_tot'],2) 
        middlefielder_together['passes_tot'] = round(middlefielder_together['passes_tot']/middlefielder_together['#games'],2) 
    if forward_together['#games'] != 0:
        forward_together['BP'] = round(forward_together['BP']/forward_together['#games'],2)
        forward_together['shots'] = round(forward_together['shots']/forward_together['#games'],2)

    return [[goalkeeper],[defender,defender_together],[middlefielder,middlefielder_together],[forward,forward_together]]
    

def output_matrix_final(matrix):
    try:
        for i in range (len(matrix)):
            BP, BC, Poss_team = 0,0,0
            cpt_BP,cpt_BC,cpt_Poss = 0,0,0
            try:
                players_impact = output_players_impact(matrix,i)    
            except:
                print("problem with output_players_impact, for i:{}".format(i))
                players_impact = 6*[6*[6*[6*[6*[0]]]]] # Construction of fictive list
            if i<len(matrix)-1 :
                for j in range (i+1,len(matrix)) :
                    if type(matrix.iloc[j,matrix.columns.get_loc("opp_team_id")]) == type(2): # Test in order to count only the occurences with numbers
                        try:
                            BP += int(matrix.iloc[j,matrix.columns.get_loc("BP")])
                            cpt_BP += 1
                        except:
                            pass
                        try:
                            BC += int(matrix.iloc[j,matrix.columns.get_loc("BC")])
                            cpt_BC += 1
                        except:
                            pass
                        try:
                            Poss_team += int(matrix.iloc[j,matrix.columns.get_loc("Poss team")])
                            cpt_Poss += 1
                        except:
                            pass

                # Setting the values in the matrix

                ''' 0. Goalkeepers '''
                # Team side
                if cpt_BC != 0:
                    matrix.iloc[i,matrix.columns.get_loc("^T_Av_BC")] = round(BC/cpt_BC,2)
                #matrix.iloc[i,matrix.columns.get_loc("^T_Av_BC_norm")] =
                #matrix.iloc[i,matrix.columns.get_loc("^T_Av_BC_G")] =
                #matrix.iloc[i,matrix.columns.get_loc("^T_Av_BC_G_norm")] =
                
                # Opp side 
                #matrix.iloc[i,matrix.columns.get_loc("^O_Av_BC")] = // Filled in Step III
                #matrix.iloc[i,matrix.columns.get_loc("^O_Av_BC_norm")] = // Filled in Step III
                #matrix.iloc[i,matrix.columns.get_loc("^O_Av_BC_G")] = // Filled in Step III
                #matrix.iloc[i,matrix.columns.get_loc("^O_Av_BC_G_norm")] = // Filled in Step III
                
                ''' 1. Defenders '''
                # Team side
                
                #matrix.iloc[i,matrix.columns.get_loc("^T_Av_BC")] = round(BC/cpt_1,2)
                matrix.iloc[i,matrix.columns.get_loc("^T_BC_D1")] = [players_impact[1][0][1]]
                matrix.iloc[i,matrix.columns.get_loc("^T_BC_D2")] = [players_impact[1][0][2]]
                matrix.iloc[i,matrix.columns.get_loc("^T_BC_D3")] = [players_impact[1][0][3]]
                matrix.iloc[i,matrix.columns.get_loc("^T_BC_D4")] = [players_impact[1][0][4]]
                matrix.iloc[i,matrix.columns.get_loc("^T_BC_D5")] = [players_impact[1][0][5]]
                matrix.iloc[i,matrix.columns.get_loc("^T_Av_BC_D")] = [players_impact[1][1]]
                #matrix.iloc[i,matrix.columns.get_loc("^T_Av_BC_D_norm")] =

                # Opp side
                #matrix.iloc[i,matrix.columns.get_loc("^O_Av_BC")] = // Filled in Step III
                #matrix.iloc[i,matrix.columns.get_loc("^O_BC_D1")] = // Filled in Step III
                #matrix.iloc[i,matrix.columns.get_loc("^O_BC_D2")] = // Filled in Step III
                #matrix.iloc[i,matrix.columns.get_loc("^O_BC_D3")] = // Filled in Step III
                #matrix.iloc[i,matrix.columns.get_loc("^O_BC_D4")] = // Filled in Step III
                #matrix.iloc[i,matrix.columns.get_loc("^O_BC_D5")] = // Filled in Step III
                #matrix.iloc[i,matrix.columns.get_loc("^O_Av_BC_D")] = // Filled in Step III
                #matrix.iloc[i,matrix.columns.get_loc("^O_Av_BC_D_norm")] = // Filled in Step III

                ''' 2. Middlefielders '''
                # Team side
                if cpt_Poss != 0:
                    matrix.iloc[i,matrix.columns.get_loc("^T_Av_poss")] = round(Poss_team/cpt_Poss,2)
                matrix.iloc[i,matrix.columns.get_loc("^T_Pass_M1")] = [players_impact[2][0][1]]
                matrix.iloc[i,matrix.columns.get_loc("^T_Pass_M2")] = [players_impact[2][0][2]]
                matrix.iloc[i,matrix.columns.get_loc("^T_Pass_M3")] = [players_impact[2][0][3]]
                matrix.iloc[i,matrix.columns.get_loc("^T_Pass_M4")] = [players_impact[2][0][4]]
                matrix.iloc[i,matrix.columns.get_loc("^T_Pass_M5")] = [players_impact[2][0][5]]
                matrix.iloc[i,matrix.columns.get_loc("^T_Av_poss_M")] = [players_impact[2][1]]

                # Opp side
                #matrix.iloc[i,matrix.columns.get_loc("^O_Av_poss")] = // Filled in Step III 
                #matrix.iloc[i,matrix.columns.get_loc("^O_Pass_M1")] = // Filled in Step III
                #matrix.iloc[i,matrix.columns.get_loc("^O_Pass_M2")] = // Filled in Step III
                #matrix.iloc[i,matrix.columns.get_loc("^O_Pass_M3")] = // Filled in Step III
                #matrix.iloc[i,matrix.columns.get_loc("^O_Pass_M4")] = // Filled in Step III
                #matrix.iloc[i,matrix.columns.get_loc("^O_Pass_M5")] = // Filled in Step III
                #matrix.iloc[i,matrix.columns.get_loc("^O_Av_poss_M")] = // Filled in Step III

                ''' 3. Forwards '''
                # Team side
                if cpt_BP != 0:
                    matrix.iloc[i,matrix.columns.get_loc("^T_Av_BP")] = round(BP/cpt_BP,2)
                matrix.iloc[i,matrix.columns.get_loc("^T_BP_F1")] = [players_impact[3][0][1]] # Returns the list of the forward 1
                matrix.iloc[i,matrix.columns.get_loc("^T_BP_F2")] = [players_impact[3][0][2]] # Returns the list of the forward 2
                matrix.iloc[i,matrix.columns.get_loc("^T_BP_F3")] = [players_impact[3][0][3]] # Returns the list of the forward 3
                matrix.iloc[i,matrix.columns.get_loc("^T_Av_BP_F")] = [players_impact[3][1]] # Returns the list of forward_together
                #matrix.iloc[i,matrix.columns.get_loc("^T_Av_BP_F_norm")] = 

                # Opp side
                #matrix.iloc[i,matrix.columns.get_loc("^O_Av_BP")] = // Filled in Step III
                #matrix.iloc[i,matrix.columns.get_loc("^O_BP_F1")] = // Filled in Step III
                #matrix.iloc[i,matrix.columns.get_loc("^O_BP_F2")] = // Filled in Step III
                #matrix.iloc[i,matrix.columns.get_loc("^O_BP_F3")] = // Filled in Step III
                #matrix.iloc[i,matrix.columns.get_loc("^O_Av_BP_F")] = // Filled in Step III
                #matrix.iloc[i,matrix.columns.get_loc("^O_Av_BP_F_norm")] = // Filled in Step III
        return matrix
    except:
        pass
    

# OK -
def last_minute_changes(team_id,opp_id,team_name,opp_name,game_fixture_id):
    
    option = 1
    matrix = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'new_matrix' +'_{}_{}'.format(team_id,option)+ '.pkl')

    max_date_raw = matrix.iloc[len(matrix)-1,matrix.columns.get_loc('event_date')]
    max_date = datetime.timestamp(datetime(int(max_date_raw[:4]),int(max_date_raw[5:7]),int(max_date_raw[8:10])))

    fixture_team = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_s'+ '_'+ str(team_id) +'.pkl')
    fixture_team = fixture_team.sort_index(ascending=False)
    fixture_team = fixture_team.set_index(pd.Index([i for i in range (len(fixture_team))]))

    BP_win_0_team, BC_win_0_team, team_win_team_id, team_win_team_name, date_win_team, homeaway_win, BP_lose_0_team, BC_lose_0_team, team_lose_team_id, team_lose_team_name, date_lose_team, homeaway_lose = 0,0,0,0,0,0,0,0,0,0,0,0

    i = 0

    while i<len(fixture_team) and int(fixture_team.iloc[i,fixture_team.columns.get_loc('event_date')][:4])>2019:
        if str(fixture_team.iloc[i,fixture_team.columns.get_loc('status')]) == "Match Finished" and max_date>datetime.timestamp(datetime(int(fixture_team.iloc[i,fixture_team.columns.get_loc('event_date')][:4]),int(fixture_team.iloc[i,fixture_team.columns.get_loc('event_date')][5:7]),int(fixture_team.iloc[i,fixture_team.columns.get_loc('event_date')][8:10]))):
            try:  
                if int(fixture_team.iloc[i,fixture_team.columns.get_loc('homeTeam')]['team_id']) == team_id:
                    BP = int(fixture_team.iloc[i,fixture_team.columns.get_loc('goalsHomeTeam')])
                    BC = int(fixture_team.iloc[i,fixture_team.columns.get_loc('goalsAwayTeam')])
                    if (BP-BC)>(BP_win_0_team-BC_win_0_team):
                        BP_win_0_team, BC_win_0_team = BP, BC
                        team_win_team_id = int(fixture_team.iloc[i,fixture_team.columns.get_loc('awayTeam')]['team_id'])
                        team_win_team_name = str(fixture_team.iloc[i,fixture_team.columns.get_loc('awayTeam')]['team_name'])
                        homeaway_win = "home"
                        date_win_team = fixture_team.iloc[i,fixture_team.columns.get_loc('event_date')]
                    elif (BP-BC)<(BP_lose_0_team-BC_lose_0_team):
                        BP_lose_0_team, BC_lose_0_team = BP, BC
                        team_lose_team_id = int(fixture_team.iloc[i,fixture_team.columns.get_loc('awayTeam')]['team_id'])
                        team_lose_team_name = str(fixture_team.iloc[i,fixture_team.columns.get_loc('awayTeam')]['team_name'])
                        homeaway_lose = "home"
                        date_lose_team = fixture_team.iloc[i,fixture_team.columns.get_loc('event_date')]
                    elif (BP-BC)==(BP_win_0_team-BC_win_0_team):
                        if BP>BP_win_0_team:
                            BP_win_0_team, BC_win_0_team = BP, BC
                            team_win_team_id = int(fixture_team.iloc[i,fixture_team.columns.get_loc('awayTeam')]['team_id'])
                            team_win_team_name = str(fixture_team.iloc[i,fixture_team.columns.get_loc('awayTeam')]['team_name'])
                            homeaway_win = "home"
                            date_win_team = fixture_team.iloc[i,fixture_team.columns.get_loc('event_date')]
                    elif (BP-BC)==(BP_lose_0_team-BC_lose_0_team):
                        if BC>BC_lose_0_team:
                            BP_lose_0_team, BC_lose_0_team = BP, BC
                            team_lose_team_id = int(fixture_team.iloc[i,fixture_team.columns.get_loc('awayTeam')]['team_id'])
                            team_lose_team_name = str(fixture_team.iloc[i,fixture_team.columns.get_loc('awayTeam')]['team_name'])
                            homeaway_lose = "home"
                            date_lose_team = fixture_team.iloc[i,fixture_team.columns.get_loc('event_date')]
                else:   
                    BC = int(fixture_team.iloc[i,fixture_team.columns.get_loc('goalsHomeTeam')])
                    BP = int(fixture_team.iloc[i,fixture_team.columns.get_loc('goalsAwayTeam')])
                    if (BP-BC)>(BP_win_0_team-BC_win_0_team):
                        BP_win_0_team, BC_win_0_team = BP, BC
                        team_win_team_id = int(fixture_team.iloc[i,fixture_team.columns.get_loc('homeTeam')]['team_id'])
                        team_win_team_name = str(fixture_team.iloc[i,fixture_team.columns.get_loc('homeTeam')]['team_name'])
                        homeaway_win = "away"
                        date_win_team = fixture_team.iloc[i,fixture_team.columns.get_loc('event_date')]
                    elif (BP-BC)<(BP_lose_0_team-BC_lose_0_team):
                        BP_lose_0_team, BC_lose_0_team = BP, BC
                        team_lose_team_id = int(fixture_team.iloc[i,fixture_team.columns.get_loc('homeTeam')]['team_id'])
                        team_lose_team_name = str(fixture_team.iloc[i,fixture_team.columns.get_loc('homeTeam')]['team_name'])
                        homeaway_lose = "away"
                        date_lose_team = fixture_team.iloc[i,fixture_team.columns.get_loc('event_date')]
                    elif (BP-BC)==(BP_win_0_team-BC_win_0_team):
                        if BP>BP_win_0_team:
                            BP_win_0_team, BC_win_0_team = BP, BC
                            team_win_team_id = int(fixture_team.iloc[i,fixture_team.columns.get_loc('homeTeam')]['team_id'])
                            team_win_team_name = str(fixture_team.iloc[i,fixture_team.columns.get_loc('homeTeam')]['team_name'])
                            homeaway_win = "away"
                            date_win_team = fixture_team.iloc[i,fixture_team.columns.get_loc('event_date')]
                    elif (BP-BC)==(BP_lose_0_team-BC_lose_0_team):
                        if BC>BC_lose_0_team:
                            BP_lose_0_team, BC_lose_0_team = BP, BC
                            team_lose_team_id = int(fixture_team.iloc[i,fixture_team.columns.get_loc('homeTeam')]['team_id'])
                            team_lose_team_name = str(fixture_team.iloc[i,fixture_team.columns.get_loc('homeTeam')]['team_name'])
                            homeaway_lose = "away"
                            date_lose_team = fixture_team.iloc[i,fixture_team.columns.get_loc('event_date')]
            except:
                pass
        i += 1
    
    matrix['biggest win'] = [{'BP':BP_win_0_team, 'BC':BC_win_0_team,'team_name':team_win_team_name,'team_id':team_win_team_id,'Date':date_win_team, "homeaway":homeaway_win}]*last_fixtures_lineups_duration
    matrix['biggest defeat'] = [{'BP':BP_lose_0_team, 'BC':BC_lose_0_team,'team_name':team_lose_team_name,'team_id':team_lose_team_id,'Date':date_lose_team, "homeaway":homeaway_lose}]*last_fixtures_lineups_duration
    
    lineup_opp = []
    for i in range (len(matrix)):
        try:
            variable_lineups = pd.read_pickle(link_data+central_folder+'/'+link_data_package_lineups_central+'/' +'lineups_fixture_id_s'+ '_'+ str(matrix.iloc[i,matrix.columns.get_loc('fixture_id')]) +'.pkl') 
            lineup_opp.append(variable_lineups[str(matrix.iloc[i,matrix.columns.get_loc('opp_team_name')])]['formation']) 
        except:
            lineup_opp.append("n.a.")
    matrix['formation_opp'] = lineup_opp

    link_excel, link_pkl = link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+ '/' + 'new_matrix' +'_{}_{}'.format(team_id,option) + '.xlsx' , link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'summarize_package'+'/' + 'new_matrix' +'_{}_{}'.format(team_id,option) + '.pkl'
    matrix.to_excel(link_excel)
    matrix.to_pickle(link_pkl)

def output_ranking_home(rounds,n,league_id,team_id): # n = 1 then it's ranking before the "rounds", if n = 0 then it's ranking after the "rounds"
    rounds = str(rounds)
    n = int(n)
    
    try:
        try:
            x = int(rounds[-2:])
        except:
            x = int(rounds[-1])
        columns = pd.read_pickle(link_data+central_folder+'/'+link_data_package_teams_central+'/' +'teams_league_id_s'+'_' + str(league_id)+'.pkl')['team_id']
        ranking = {key: [0,0,0,0,0,0,0] for key in columns}
        round_list = pd.read_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/' +'fixturesrounds_league_id_s'+'_' + str(league_id)+'.pkl')
        i = 0
        while i < len(round_list) and i<(x-n): # This is where the "n" parameter is used
            p = str(round_list.iloc[i,0])
            fixtures_list = pd.read_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixtures_league_id_round_s'+ '_'+ str(league_id) +'_' +str(p)+'.pkl')
            for j in range (len(fixtures_list)):
                status = str(fixtures_list.iloc[j,fixtures_list.columns.get_loc('status')])
                home_team_id = fixtures_list.iloc[j,fixtures_list.columns.get_loc('homeTeam')]['team_id']
                home_team_id = fixtures_list.iloc[j,fixtures_list.columns.get_loc('homeTeam')]['team_id']
                home_team_score = fixtures_list.iloc[j,fixtures_list.columns.get_loc('goalsHomeTeam')]
                away_team_id = fixtures_list.iloc[j,fixtures_list.columns.get_loc('awayTeam')]['team_id']
                away_team_score = fixtures_list.iloc[j,fixtures_list.columns.get_loc('goalsAwayTeam')]   

                try: 
                    if status == "Match Finished" :
                        ranking[home_team_id][1] += 1
                        ranking[home_team_id][5] += home_team_score
                        ranking[home_team_id][6] += away_team_score

                        if home_team_score > away_team_score :
                            ranking[home_team_id][0] += 3
                            ranking[home_team_id][2] += 1
                        elif home_team_score < away_team_score :
                            ranking[home_team_id][4] += 1
                        else :
                            ranking[home_team_id][0] += 1
                            ranking[home_team_id][3] += 1
                except: 
                    ranking[home_team_id][0] += 0  
            i += 1    
        ranking = pd.DataFrame.from_dict(ranking).T
        ranking = ranking.rename(columns={0: "rank", 1: "played",2:"W",3:"D",4:"L",5:"BP",6:"BC"})
        ranking = ranking.sort_values(by=["rank"],ascending=False)
        
    except:
        ranking = "No ranking"
    return ranking


def output_ranking_away(rounds,n,league_id,team_id): # n = 1 then it's ranking before the "rounds", if n = 0 then it's ranking after the "rounds"
    rounds = str(rounds)
    n = int(n)
    
    try:
        try:
            x = int(rounds[-2:])
        except:
            x = int(rounds[-1])
        columns = pd.read_pickle(link_data+central_folder+'/'+link_data_package_teams_central+'/' +'teams_league_id_s'+'_' + str(league_id)+'.pkl')['team_id']
        ranking = {key: [0,0,0,0,0,0,0] for key in columns}
        round_list = pd.read_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/' +'fixturesrounds_league_id_s'+'_' + str(league_id)+'.pkl')
        i = 0
        while i < len(round_list) and i<(x-n): # This is where the "n" parameter is used
            p = str(round_list.iloc[i,0])
            fixtures_list = pd.read_pickle(link_data+central_folder+'/'+link_data_package_fixtures_central+'/'+'fixtures_league_id_round_s'+ '_'+ str(league_id) +'_' +str(p)+'.pkl')
            for j in range (len(fixtures_list)):
                status = str(fixtures_list.iloc[j,fixtures_list.columns.get_loc('status')])
                home_team_id = fixtures_list.iloc[j,fixtures_list.columns.get_loc('homeTeam')]['team_id']
                home_team_id = fixtures_list.iloc[j,fixtures_list.columns.get_loc('homeTeam')]['team_id']
                home_team_score = fixtures_list.iloc[j,fixtures_list.columns.get_loc('goalsHomeTeam')]
                away_team_id = fixtures_list.iloc[j,fixtures_list.columns.get_loc('awayTeam')]['team_id']
                away_team_score = fixtures_list.iloc[j,fixtures_list.columns.get_loc('goalsAwayTeam')]   
                   
                try: 
                    if status == "Match Finished" :
                        ranking[away_team_id][1] += 1
                        ranking[away_team_id][5] += away_team_score
                        ranking[away_team_id][6] += home_team_score

                        if home_team_score > away_team_score :
                            ranking[away_team_id][4] += 1
                        elif home_team_score < away_team_score :
                            ranking[away_team_id][0] += 3
                            ranking[away_team_id][2] += 1
                        else :
                            ranking[away_team_id][0] += 1
                            ranking[away_team_id][3] += 1
                except: 
                    ranking[away_team_id][0] += 0
            i += 1    
        ranking = pd.DataFrame.from_dict(ranking).T
        ranking = ranking.rename(columns={0: "rank", 1: "played",2:"W",3:"D",4:"L",5:"BP",6:"BC"})
        ranking = ranking.sort_values(by=["rank"],ascending=False)
        
    except:
        ranking = "No ranking"
    return ranking


def output_ranking_extract_home(rounds,n,league_id,team_id,var_team_id): # n = 1 then it's ranking before the "rounds", if n = 0 then it's ranking after the "rounds"
    
    team_id = int(team_id)
    var_team_id = int(var_team_id)

    ranking = output_ranking_home(rounds,n,league_id,team_id)
    variable_leagues = pd.read_pickle(link_data+central_folder+'/'+link_data_package_teams_central+'/' +'teams_league_id_s'+ '_'+ str(league_id)+'.pkl')
    x = 1 + ranking.index.get_loc(var_team_id)
    extract = ["x",0,0,0,0,0,0,0,0]
    
    extract[0] = str(variable_leagues.loc[variable_leagues['team_id'] == ranking.iloc[x-1].name].iloc[0,variable_leagues.loc[variable_leagues['team_id'] == ranking.iloc[x-1].name].columns.get_loc('name')])
    extract[1] = int(x)
    extract[2] = int(ranking.iloc[x-1,0])
    extract[3] = int(ranking.iloc[x-1,1])
    extract[4] = int(ranking.iloc[x-1,2])
    extract[5] = int(ranking.iloc[x-1,3])
    extract[6] = int(ranking.iloc[x-1,4])
    extract[7] = int(ranking.iloc[x-1,5])
    extract[8] = int(ranking.iloc[x-1,6])
    return extract # Difference with output_ranking_extract because returns 1 object

def output_ranking_extract_away(rounds,n,league_id,team_id,var_team_id): # n = 1 then it's ranking before the "rounds", if n = 0 then it's ranking after the "rounds"
    
    team_id = int(team_id)
    var_team_id = int(var_team_id)

    ranking = output_ranking_away(rounds,n,league_id,team_id)
    variable_leagues = pd.read_pickle(link_data+central_folder+'/'+link_data_package_teams_central+'/' +'teams_league_id_s'+ '_'+ str(league_id)+'.pkl')
    x = 1 + ranking.index.get_loc(var_team_id)
    extract = ["x",0,0,0,0,0,0,0,0]
    
    extract[0] = str(variable_leagues.loc[variable_leagues['team_id'] == ranking.iloc[x-1].name].iloc[0,variable_leagues.loc[variable_leagues['team_id'] == ranking.iloc[x-1].name].columns.get_loc('name')])
    extract[1] = int(x)
    extract[2] = int(ranking.iloc[x-1,0])
    extract[3] = int(ranking.iloc[x-1,1])
    extract[4] = int(ranking.iloc[x-1,2])
    extract[5] = int(ranking.iloc[x-1,3])
    extract[6] = int(ranking.iloc[x-1,4])
    extract[7] = int(ranking.iloc[x-1,5])
    extract[8] = int(ranking.iloc[x-1,6])
    return extract # Difference with output_ranking_extract because returns 1 object

'''
To be corrected
------------------------------------------------------------------------------------
'''
