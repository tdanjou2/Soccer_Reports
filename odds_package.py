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

# OK -
def odds_fixture_id(fixture_id):    
    fixture_id = str(fixture_id)
    url_odds_fixture_id = url + "odds/fixture/" + fixture_id 
    response = requests.request("GET", url_odds_fixture_id, headers=headers)
    print("odds_fixture_id + 1")
    return list(pd.DataFrame.from_dict(json.loads(response.text)['api']['odds']).columns) , pd.DataFrame.from_dict(json.loads(response.text)['api']['odds'])

# OK - No Test
def odds_fixture_id_s(team_id,game_fixture_id):    
    start_time = time.time()
    data = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_last_s'+ '_'+ str(team_id) + '_'+ str(last) +'.pkl') 
    data_2 = pd.read_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'fixtures_package'+'/'+'fixtures_team_id_next_s'+ '_'+ str(team_id) + '_'+ str(nex) +'.pkl') 
    for i in range (len(data)):
        try :
            fixture_id = data.iloc[i,data.columns.get_loc('fixture_id')]   
            x = odds_fixture_id(fixture_id)[1]
            x.to_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'odds_package'+'/'+'odds_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
        except:
            print("Error with {}".format(i))
    for i in range (len(data_2)):
        try :
            fixture_id = data_2.iloc[i,data_2.columns.get_loc('fixture_id')]
            x = odds_fixture_id(fixture_id)[1]
            x.to_pickle(link_data+'{}'.format(team_id)+'/'+str(game_fixture_id) + '/' +'odds_package'+'/'+'odds_fixture_id_s'+ '_'+ str(fixture_id) +'.pkl')
        except:
            print("Error with {}".format(i))
    print("odds_fixture_id_s() : {}".format(round(time.time()-start_time,2))) 