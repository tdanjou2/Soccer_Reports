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
# Need to get intermediary calculations

# OK - 
def coachs_coach_id(coach_id):    
    coach_id = str(coach_id)
    coachs_coach_id = url + "coachs/coach/" + coach_id 
    response = requests.request("GET", coachs_coach_id, headers=headers)
    print("coachs_coach_id + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['coachs']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['coachs'])

# OK - No test // Problem coach_id // team_id
def coachs_team_id_s(team_id,game_fixture_id):    
    start_time = time.time()
    data = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'leagues_package'+'/'+'leagues_team_id_relevant_s'+ '_'+ str(team_id) +'.pkl') 
    for i in range (len(data)):
        try :
            league_id = data.iloc[i,data.columns.get_loc('league_id')]
            x = pd.read_pickle(link_data+central_folder+'/'+link_data_package_teams_central+'/'+'teams_league_id_s'+ '_'+ str(league_id) + '.pkl')
            for j in range (len(x)):
                team_id_2 = x.iloc[j,x.columns.get_loc('team_id')]
                y = coachs_coach_id(team_id_2)[1]
                y.to_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' + 'coachs_package'+'/'+'coachs_team_id_s'+ '_'+ str(team_id_2) +'.pkl')
        except:
            print("Error with {},{}".format(i,j))
    print("coachs_team_id_s() : {}".format(round(time.time()-start_time,2))) 