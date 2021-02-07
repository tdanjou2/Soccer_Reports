# Imports
import requests
import json
import pandas as pd  
import numpy as np
from pathlib import Path
from datetime import datetime
import time
from datetime import timedelta  
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import ColorFormat, RGBColor
import codecs  


"""
API parameters ----------------------------------------------------------------------
"""

global headers
global url
headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "" }

url = "https://api-football-v1.p.rapidapi.com/v2/"

global request_cpt
request_cpt = 0

"""
---------------------------------------------- DATA ----------------------------------------------
"""

"""
Input parameters for Data --------------------------------------------------------------------
"""

# Game parameters
""" global team_name
global opp_name
global team_id
global opp_id
global game_fixture_id

team_name = 'Crystal Palace' # Is not used afterwards 
opp_name = 'Aston Villa' # HAS TO BE SPECIFIED 
team_id = 52 # HAS TO BE SPECIFIED
opp_id = 66 # Is not used afterwards 
game_fixture_id = str(team_id)+ ' - ' + opp_name  """

global input_dic
input_dic = {1:{'team_id':79,'opp_id':89},2:{'team_id':89,'opp_id':79},3:{'team_id':48,'opp_id':40},\
    4:{'team_id':40,'opp_id':48},5:{'team_id':724,'opp_id':530},6:{'team_id':530,'opp_id':724},7:{'team_id':0,'opp_id':0},8:{'team_id':0,'opp_id':0}}


# Other parameters
global last
global nex

global last_fixtures_lineups_duration
global neighbors
global max_future_game
global max_future_game_neighbors
global time_players_impact 
global significant_games 
global size_extract_identical 
global start_date 
global now_time 
global start_time_update # Start time for update of empty dataframe
global detla_seconds_update

last = 25
nex = 10

last_fixtures_lineups_duration = 20
neighbors = 2
max_future_game = 6
max_future_game_neighbors = 3
time_players_impact = 5 # The number of last games during whihc the data occured
significant_games = 5 # The number of games during which the data has been calculated
size_extract_identical = last + 1 # The size of identical period
start_date = 2012 # Strictly superior 
now_time = datetime.timestamp(datetime.now())
start_time_update = datetime.timestamp(datetime(2020, 11, 1))
detla_seconds_update = 60*60*24 # 24 hours of refreshment for the fixtures fo each neighbor

global list_pending
global cols

# ^SECTION^ # ^to be calculated with separate function
list_pending = ["^GOALKEEPER^","^T_Av_BC","^T_Av_BC_norm","^T_Av_BC_G","^T_Av_BC_G_norm","^O_Av_BC","^O_Av_BC_norm","^O_Av_BC_G","^O_Av_BC_G_norm","^DEFENDERS^","^T_BC_D1","^T_BC_D2",\
"^T_BC_D3","^T_BC_D4","^T_BC_D5","^T_Av_BC_D","^T_Av_BC_D_norm","^O_BC_D1","^O_BC_D2","^O_BC_D3","^O_BC_D4","^O_BC_D5","^O_Av_BC_D","^O_Av_BC_D_norm","^MIDDLEFIELDERS^","^T_Av_poss","^T_Pass_M1","^T_Pass_M2",\
"^T_Pass_M3","^T_Pass_M4","^T_Pass_M5","^T_Av_poss_M","^O_Av_poss","^O_Pass_M1","^O_Pass_M2","^O_Pass_M3","^O_Pass_M4","^O_Pass_M5","^O_Av_poss_M","^FORWARDS^","^T_Av_BP","^T_BP_F1","^T_BP_F2","^T_BP_F3",\
"^T_Av_BP_F","^T_Av_BP_F_norm","^O_Av_BP","^O_BP_F1","^O_BP_F2","^O_BP_F3","^O_Av_BP_F","^O_Av_BP_F_norm"]

cols = ["^GENERAL^",\
"^GAME^","comments",'fixture_id','event_date',"referee",'round','away_home','W-D-L','league_id','opp_team_id','opp_team_name',"formation","G","F",'M',"D","P1_stats_mod","P2_stats_mod",\
"P3_stats_mod","P4_stats_mod","P5_stats_mod","P6_stats_mod","P7_stats_mod","P8_stats_mod","P9_stats_mod","P10_stats_mod","P11_stats_mod","P12_stats_mod",\
"P13_stats_mod","P14_stats_mod","P15_stats_mod","P16_stats_mod","BP","BP_direct","BC","BC_direct","BP_own_goals","BC_own_goals","BP_pre_red_card","BC_pre_red_card",\
"BP_pre_yellow_card","BC_pre_yellow_card","BP_pre_penalty","BC_pre_penalty","BP_normal","BC_normal","Poss team","Poss opp","shots_team","shots_opp","fouls_team","fouls_opp","passes_total_team","passes_acc_team","passes_total_opp","passes_acc_opp",\
"yellow_team","red_team","yellow_opp","red_opp","BP_subs","ABP_subs","ABC_subs","BC_subs","Penalty_comm_team","Penalty_comm_opp",\
"First","BP_0-30","BP_30-60","BP_60-100","BC_0-30","BC_30-60","BC_60-100","^NOT_GAME^","rank_team","rank_opp","r-3_team","r-2_team","r-1_team","r1_team","r2_team","r3_team",\
"N+1_team","N+2_team","N+3_team","N+4_team","N+5_team","N+1_opp","N+2_opp","N+3_opp","N+4_opp","N+5_opp","N+0_r-1","N+1_r-1","N+2_r-1","N+0_r-2","N+1_r-2","N+2_r-2","N+0_r-3","N+1_r-3","N+2_r-3","N+0_r1","N+1_r1","N+2_r1","N+0_r2","N+1_r2","N+2_r2","N+0_r3","N+1_r3","N+2_r3",\
"^REPORTS^"\
] + list_pending    

"""
Data folder parameters ---------------------------------------------------------------------
"""

# Only used in packages to create the data
""" global link_data
global central_folder
global link_data_package_coachs
global link_data_package_fixtures
global link_data_package_odds
global link_data_package_players
global link_data_package_sidelined
global link_data_package_summarize
global link_data_package_teams
global link_data_package_leagues
global link_data_package_statitics
global link_data_package_events
global link_data_package_trophies
global link_data_package_lineups
global link_data_package_transfers
global link_data_package_output """

global link_data_package_coachs_central
global link_data_package_fixtures_central
global link_data_package_odds_central
global link_data_package_players_central
global link_data_package_sidelined_central
global link_data_package_summarize_central
global link_data_package_teams_central
global link_data_package_leagues_central
global link_data_package_statitics_central
global link_data_package_events_central
global link_data_package_trophies_central
global link_data_package_lineups_central
global link_data_package_transfers_central
global link_data_package_output_central

global list_links

link_data = '/Users/danjoutheophile/Desktop/Bureau - MacBook Pro de DANJOU (935)/Projets/Research soccer/Data/' 

central_folder = "X_CENTRAL_X"
link_data_package_coachs = 'coachs_package'
link_data_package_fixtures = 'fixtures_package'
link_data_package_odds = 'odds_package'
link_data_package_players = 'players_package'
link_data_package_sidelined = 'sidelined_package'
link_data_package_summarize = 'summarize_package'
link_data_package_teams = 'teams_package'
link_data_package_leagues = 'leagues_package'
link_data_package_statitics = 'statistics_package'
link_data_package_events = 'events_package'
link_data_package_trophies = 'trophies_package'
link_data_package_lineups = 'lineups_package'
link_data_package_transfers = 'transfers_package'
link_data_package_output = 'output_package'

link_data_package_coachs_central = 'coachs_package'
link_data_package_fixtures_central = 'fixtures_package'
link_data_package_odds_central = 'odds_package'
link_data_package_players_central =  'players_package'
link_data_package_sidelined_central = 'sidelined_package'
link_data_package_summarize_central = 'summarize_package'
link_data_package_teams_central = 'teams_package'
link_data_package_leagues_central = 'leagues_package'
link_data_package_statitics_central = 'statistics_package'
link_data_package_events_central = 'events_package'
link_data_package_trophies_central = 'trophies_package'
link_data_package_lineups_central = 'lineups_package'
link_data_package_transfers_central =  'transfers_package'
link_data_package_output_central = 'output_package'

list_links = [link_data_package_coachs,link_data_package_fixtures,link_data_package_odds,link_data_package_players,link_data_package_sidelined,link_data_package_summarize,link_data_package_teams,link_data_package_leagues,link_data_package_statitics,link_data_package_events,link_data_package_trophies,link_data_package_lineups,link_data_package_transfers,link_data_package_output] 

"""
---------------------------------------------- REPORTS ----------------------------------------------
"""

"""
Input parameters for Reports --------------------------------------------------------------------
"""
global english # "0" if French and "1" if English

global font_1

global home_color_report
global home_color_plot 
global away_color_report 
global away_color_plot 
global white_color_report 
global white_color_plot 
global black_color_report 
global black_color_plot
global green_color_report 
global green_plot_plot 
global red_color_report 
global red_color_plot 
global win_color_report 
global win_color_plot 
global draw_color_report 
global draw_color_plot 
global lose_color_report 
global lose_color_plot 

global colors_data

global graph_format
global pic_format
global jpg_format
global png_format
global dpi_1

global font_size_ranking
global font_size_bubble
global font_size_bubble_number
global font_size_titleh1
global font_size_titleh2
global font_size_table

global height_1 # This is for graphs
global height_2 # This is for logos
global height_3 
global height_4 
global height_5
global height_6
global buffer # An extra size to make sure we can't see the edge
global buffer_adv
global matrix_positions_introduction 

global name_folder_introduction

english = 0

font_1 = "Helvetica"

blue_color_report = RGBColor(0,0,255) # OK

home_color_report = RGBColor(255,165,0) # OK
home_color_plot = 'orange'

away_color_report = RGBColor(106,90,205) # OK
away_color_plot = 'slateblue'

white_color_report = RGBColor(255,255,255) # OK
white_color_plot = 'white'

black_color_report = RGBColor(0,0,0) # OK
black_color_plot = 'black' 

green_color_report = RGBColor(0,176,80) # OK
green_plot_plot = 'green'

red_color_report = RGBColor(255,0,0) # OK
red_color_plot = 'red'

yellow_color_report = RGBColor(255, 255, 0) # OK
yellow_color_plot = 'yellow'

win_color_report = green_color_report # OK
win_color_plot = green_plot_plot

draw_color_report = RGBColor(211,211, 211) # OK
draw_color_plot = 'lightgrey'

lose_color_report = red_color_report # OK
lose_color_plot = red_color_plot

defender_color_plot = 'r' # OK

midfielder_color_plot = 'olive' # OK

forward_color_plot = 'b' # OK

colors_data = {'4-4-2':'deepskyblue','4-1-4-1':'lightblue','4-2-3-1':'cadetblue','4-3-2-1':'darkturquoise','4-3-3':'aliceblue','4-5-1':'slategray','5-4-1':'pink','3-1-4-2':'plum','3-5-2':'peachpuff','3-4-3':'khaki','4-3-1-2':'limegreen','3-4-1-2':'tan','3-4-2-1':'rosybrown','5-3-2':'firebrick','4-4-1-1':'violet','other':'lightgrey'}

graph_format = '.png'
pic_format = '.png'
jpg_format = '.jpg'
png_format = '.png'
dpi_1 = 600

font_size_ranking = 9
font_size_bubble = 12
font_size_bubble_number = 32
font_size_titleh1 = 17
font_size_titleh2 = 14
font_size_table = 11

height_1 = 9.0 # For just 1 graph on the page
height_5 = 4.5 # In cm for the formation animations
height_6 = 5.87 # For just 2 graph on the page

height_2 = 2.0 # In cm for the 2 logos in the begining
height_3 = 0.79 # In cm for the logos in the ranking tables
height_4 = 0.92 # In cm for the logos in the 2 home and team biggest win and defeat
height_7 = 1.68 # In cm for the logos at the subs goals/assits analysis
height_8 = 5.28 # In cm for data profile of each player

buffer = 0.02 # In cm
buffer_adv = 0.5 # In cm
matrix_positions_introduction = {'logo_team_home':{'page_number':0,'pos_left': 0.42 , 'pos_top' :2.63,'width' :0,'height' :0},\
'logo_team_away':{'page_number':0,'pos_left': 16.63 , 'pos_top' :2.62,'width' :0,'height' :0},\

'logo_1':{'page_number':3,'pos_left': 0.48 , 'pos_top' :15.12,'width' :0,'height' :0},\
'logo_2':{'page_number':3,'pos_left': 8.31 , 'pos_top' :15.12,'width' :0,'height' :0},\
'logo_3':{'page_number':3,'pos_left': 9.8 , 'pos_top' :15.11,'width' :0,'height' :0},\
'logo_4':{'page_number':3,'pos_left': 17.63 , 'pos_top' :15.11,'width' :0,'height' :0},\
'logo_5':{'page_number':3,'pos_left': 0.48 , 'pos_top' :22.43,'width' :0,'height' :0},\
'logo_6':{'page_number':3,'pos_left': 8.31 , 'pos_top' :22.42,'width' :0,'height' :0},\
'logo_7':{'page_number':3,'pos_left': 9.73 , 'pos_top' :22.43,'width' :0,'height' :0},\
'logo_8':{'page_number':3,'pos_left': 17.63 , 'pos_top' :22.41,'width' :0,'height' :0},\

'logo_9':{'page_number':3,'pos_left': 0.47 , 'pos_top' :18.05,'width' :0,'height' :0},\
'logo_10':{'page_number':3,'pos_left': 8.3 , 'pos_top' :18.05,'width' :0,'height' :0},\
'logo_11':{'page_number':3,'pos_left': 9.79 , 'pos_top' :18.04,'width' :0,'height' :0},\
'logo_12':{'page_number':3,'pos_left': 17.63 , 'pos_top' :18.04,'width' :0,'height' :0},\
'logo_13':{'page_number':3,'pos_left': 0.46 , 'pos_top' :25.27,'width' :0,'height' :0},\
'logo_14':{'page_number':3,'pos_left': 8.3 , 'pos_top' :25.27,'width' :0,'height' :0},\
'logo_15':{'page_number':3,'pos_left': 9.78 , 'pos_top' :25.26,'width' :0,'height' :0},\
'logo_16':{'page_number':3,'pos_left': 17.62 , 'pos_top' :25.26,'width' :0,'height' :0},\

'introduction_global_photo_home_1':{'page_number':0,'pos_left': 1.9 , 'pos_top' :21.33,'width' :0,'height' :0},\
'introduction_global_photo_home_2':{'page_number':0,'pos_left': 1.9 , 'pos_top' :22.32,'width' :0,'height' :0},\
'introduction_global_photo_home_3':{'page_number':0,'pos_left': 1.9 , 'pos_top' :23.29,'width' :0,'height' :0},\
'introduction_global_photo_home_4':{'page_number':0,'pos_left': 1.9 , 'pos_top' :24.26,'width' :0,'height' :0},\
'introduction_global_photo_home_5':{'page_number':0,'pos_left': 1.9 , 'pos_top' :25.23,'width' :0,'height' :0},\
'introduction_global_photo_home_6':{'page_number':0,'pos_left': 1.9 , 'pos_top' :26.2,'width' :0,'height' :0},\
'introduction_global_photo_home_7':{'page_number':0,'pos_left': 1.9 , 'pos_top' :27.18,'width' :0,'height' :0},\

'introduction_global_photo_away_1':{'page_number':0,'pos_left': 11.1 , 'pos_top' :21.33,'width' :0,'height' :0},\
'introduction_global_photo_away_2':{'page_number':0,'pos_left': 11.1 , 'pos_top' :22.32,'width' :0,'height' :0},\
'introduction_global_photo_away_3':{'page_number':0,'pos_left': 11.1 , 'pos_top' :23.3,'width' :0,'height' :0},\
'introduction_global_photo_away_4':{'page_number':0,'pos_left': 11.1 , 'pos_top' :24.26,'width' :0,'height' :0},\
'introduction_global_photo_away_5':{'page_number':0,'pos_left': 11.1 , 'pos_top' :25.23,'width' :0,'height' :0},\
'introduction_global_photo_away_6':{'page_number':0,'pos_left': 11.1 , 'pos_top' :26.2,'width' :0,'height' :0},\
'introduction_global_photo_away_7':{'page_number':0,'pos_left': 11.1 , 'pos_top' :27.18,'width' :0,'height' :0},\

'introduction_home_photo_1':{'page_number':1,'pos_left': 1.9 , 'pos_top' :4.78,'width' :0,'height' :0},\
'introduction_home_photo_2':{'page_number':1,'pos_left': 1.9, 'pos_top' :5.77,'width' :0,'height' :0},\
'introduction_home_photo_3':{'page_number':1,'pos_left': 1.9 , 'pos_top' :6.75,'width' :0,'height' :0},\
'introduction_home_photo_4':{'page_number':1,'pos_left': 1.9 , 'pos_top' :7.72,'width' :0,'height' :0},\
'introduction_home_photo_5':{'page_number':1,'pos_left': 1.9 , 'pos_top' :8.69,'width' :0,'height' :0},\
'introduction_home_photo_6':{'page_number':1,'pos_left': 1.9 , 'pos_top' :9.65,'width' :0,'height' :0},\
'introduction_home_photo_7':{'page_number':1,'pos_left': 1.9 , 'pos_top' :10.64,'width' :0,'height' :0},\

'introduction_away_photo_1':{'page_number':1,'pos_left': 11.1 , 'pos_top' :4.79,'width' :0,'height' :0},\
'introduction_away_photo_2':{'page_number':1,'pos_left': 11.1 , 'pos_top' :5.78,'width' :0,'height' :0},\
'introduction_away_photo_3':{'page_number':1,'pos_left': 11.1 , 'pos_top' :6.75,'width' :0,'height' :0},\
'introduction_away_photo_4':{'page_number':1,'pos_left': 11.1 , 'pos_top' :7.72,'width' :0,'height' :0},\
'introduction_away_photo_5':{'page_number':1,'pos_left': 11.12 , 'pos_top' :8.69,'width' :0,'height' :0},\
'introduction_away_photo_6':{'page_number':1,'pos_left': 11.1 , 'pos_top' :9.66,'width' :0,'height' :0},\
'introduction_away_photo_7':{'page_number':1,'pos_left': 11.12 , 'pos_top' :10.64,'width' :0,'height' :0},\

'introduction_reports_chart_section1':{'page_number':1,'pos_left':4.78,'pos_top' :20.33,'width' :0,'height' :0},\
'introduction_reports_chart_section2':{'page_number':2,'pos_left': 4.78 , 'pos_top' :20.44,'width' :0,'height' :0},\
'introduction_reports_chart_section3':{'page_number':2,'pos_left': 4.78 , 'pos_top' :4.51,'width' :0,'height' :0},\
'introduction_reports_chart_section4':{'page_number':3,'pos_left': 0.53 , 'pos_top' :2.73,'width' :0,'height' :0},\
'introduction_reports_chart_section5':{'page_number':3,'pos_left': 9.73 , 'pos_top' :2.73,'width' :0,'height' :0},\

'introduction_advantage':{'page_number':3,'pos_left': 0.43 , 'pos_top' :28.29,'width' :0,'height' :0},\
}

matrix_positions_composition = {'formation_home':{'page_number':4,'pos_left': 1.58 , 'pos_top' :8.97,'width' :0,'height' :0},\
'formation_away':{'page_number':4,'pos_left':11.52 , 'pos_top' :9.01,'width' :0,'height' :0},\

'home_logo_1':{'page_number':6,'pos_left':1.58 , 'pos_top' :4.5,'width' :0,'height' :0},\
'away_logo_1':{'page_number':6,'pos_left':15.25 , 'pos_top' :4.49,'width' :0,'height' :0},\
'home_logo_2':{'page_number':6,'pos_left':1.58 , 'pos_top' :10.44,'width' :0,'height' :0},\
'away_logo_2':{'page_number':6,'pos_left':15.25 , 'pos_top' :10.43,'width' :0,'height' :0},\

'composition_reports_chart_section1':{'page_number':4,'pos_left':4.96,'pos_top' :15.22,'width' :0,'height' :0},\
'composition_reports_chart_section2':{'page_number':4,'pos_left': 4.91 , 'pos_top' :24.46,'width' :0,'height' :0},\
'composition_reports_chart_section3':{'page_number':5,'pos_left': 0.87 , 'pos_top' :0.33,'width' :0,'height' :0},\
'composition_reports_chart_section4':{'page_number':5,'pos_left': 2.78 , 'pos_top' :9.56,'width' :0,'height' :0},\
'composition_reports_chart_section5':{'page_number':5,'pos_left': 0.53 , 'pos_top' :22.56,'width' :0,'height' :0},\
'composition_reports_chart_section6':{'page_number':5,'pos_left': 9.73 , 'pos_top' :22.56,'width' :0,'height' :0},\
'composition_reports_chart_section8':{'page_number':6,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\

'composition_reports_section_goal_home_1':{'page_number':7,'pos_left': 0.47 , 'pos_top' :17.35,'width' :0,'height' :0},\
'composition_reports_section_goal_away_1':{'page_number':7,'pos_left': 0.47 , 'pos_top' :17.35,'width' :0,'height' :0},\

'composition_reports_section_defender_home_1':{'page_number':7,'pos_left': 0.47 , 'pos_top' :17.35,'width' :0,'height' :0},\
'composition_reports_section_defender_home_2':{'page_number':7,'pos_left': 10.75 , 'pos_top' :17.35,'width' :0,'height' :0},\
'composition_reports_section_defender_home_3':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_defender_home_4':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_defender_home_5':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_defender_home_6':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\

'composition_reports_section_defender_away_1':{'page_number':7,'pos_left': 0.47 , 'pos_top' :17.35,'width' :0,'height' :0},\
'composition_reports_section_defender_away_2':{'page_number':7,'pos_left': 10.75 , 'pos_top' :17.35,'width' :0,'height' :0},\
'composition_reports_section_defender_away_3':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_defender_away_4':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_defender_away_5':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_defender_away_6':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\

'composition_reports_section_midfielder_home_1':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_midfielder_home_2':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_midfielder_home_3':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_midfielder_home_4':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_midfielder_home_5':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_midfielder_home_6':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\

'composition_reports_section_midfielder_away_1':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_midfielder_away_2':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_midfielder_away_3':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_midfielder_away_4':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_midfielder_away_5':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_midfielder_away_6':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\

'composition_reports_section_forward_home_1':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_forward_home_2':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_forward_home_3':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_forward_home_4':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_forward_home_5':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_forward_home_6':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\

'composition_reports_section_forward_away_1':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_forward_away_2':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_forward_away_3':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_forward_away_4':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_forward_away_5':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\
'composition_reports_section_forward_away_6':{'page_number':8,'pos_left': 2.74 , 'pos_top' :18.79,'width' :0,'height' :0},\

'composition_advantage':{'page_number':6,'pos_left': 0.43 , 'pos_top' :28.29,'width' :0,'height' :0},\
}


matrix_positions_pressure = {'logo_team_h_1':{'page_number':7,'pos_left': 0.54 , 'pos_top' :12.87,'width' :0,'height' :0},\
'logo_team_h_2':{'page_number':10,'pos_left':0.54 , 'pos_top' :14.27,'width' :0,'height' :0},\
'logo_team_h_3':{'page_number':10,'pos_left':0.54,'pos_top' :15.68,'width' :0,'height' :0},\
'logo_team_h_4':{'page_number':10,'pos_left': 0.54 , 'pos_top' :17.08,'width' :0,'height' :0},\
'logo_team_a_1':{'page_number':11,'pos_left': 0.54 , 'pos_top' :3.86,'width' :0,'height' :0},\
'logo_team_a_2':{'page_number':11,'pos_left': 0.54 , 'pos_top' :5.26,'width' :0,'height' :0},\
'logo_team_a_3':{'page_number':11,'pos_left': 0.54 , 'pos_top' :6.66,'width' :0,'height' :0},\
'logo_team_a_4':{'page_number':11,'pos_left': 0.54 , 'pos_top' :8.07,'width' :0,'height' :0},\

'pressure_reports_chart_section1':{'page_number':10,'pos_left': 0.53 , 'pos_top' :23.64,'width' :0,'height' :0},\
'pressure_reports_chart_section2':{'page_number':10,'pos_left': 9.73 , 'pos_top' :23.64,'width' :0,'height' :0},\
'pressure_reports_chart_section3':{'page_number':11,'pos_left': 0.53 , 'pos_top' :16.04,'width' :0,'height' :0},\
'pressure_reports_chart_section4':{'page_number':11,'pos_left': 9.73 , 'pos_top' :16.04,'width' :0,'height' :0},\

'pressure_advantage':{'page_number':9,'pos_left': 0.43 , 'pos_top' :28.29,'width' :0,'height' :0},\
}

matrix_positions_typology = {'typology_reports_chart_section1':{'page_number':14,'pos_left': 0.53 , 'pos_top' :10.25,'width' :0,'height' :0},\
'typology_reports_chart_section2':{'page_number':14,'pos_left':9.73 , 'pos_top' :10.25,'width' :0,'height' :0},\
'typology_reports_chart_section3':{'page_number':14,'pos_left':0.6,'pos_top' :22.3,'width' :0,'height' :0},\
'typology_reports_chart_section4':{'page_number':14,'pos_left': 9.8 , 'pos_top' :22.3,'width' :0,'height' :0},\
'typology_reports_chart_section5':{'page_number':15,'pos_left': 0.53 , 'pos_top' :19.21,'width' :0,'height' :0},\
'typology_reports_chart_section6':{'page_number':15,'pos_left': 9.73 , 'pos_top' :19.21,'width' :0,'height' :0},\
'typology_reports_chart_section7':{'page_number':16,'pos_left': 4.89 , 'pos_top' :6.55,'width' :0,'height' :0},\
'typology_reports_chart_section8':{'page_number':16,'pos_left': 4.89 , 'pos_top' :17.1,'width' :0,'height' :0},\
'typology_reports_chart_section9':{'page_number':17,'pos_left': 0.53 , 'pos_top' :3.17,'width' :0,'height' :0},\
'typology_reports_chart_section10':{'page_number':17,'pos_left': 9.73 , 'pos_top' :3.17,'width' :0,'height' :0},\
'typology_reports_chart_section11':{'page_number':17,'pos_left': 0.53 , 'pos_top' :16.71,'width' :0,'height' :0},\
'typology_reports_chart_section12':{'page_number':17,'pos_left': 9.73 , 'pos_top' :16.71,'width' :0,'height' :0},\

'typology_advantage':{'page_number':9,'pos_left': 0.43 , 'pos_top' :28.29,'width' :0,'height' :0},\
}

matrix_positions_h2h = {

'h2h_advantage':{'page_number':9,'pos_left': 0.43 , 'pos_top' :28.29,'width' :0,'height' :0},\
}


name_folder_introduction = 'introduction'
name_folder_composition = 'composition'
name_folder_pressure = 'pressure'
name_folder_typology = 'typology'
name_folder_h2h = 'h2h'

"""
Reports parameters ---------------------------------------------------------------------
"""

link_reports = '/Users/danjoutheophile/Desktop/Bureau - MacBook Pro de DANJOU (935)/Projets/Research soccer/Reports/' # 

"""
Other ------------------------------------------------------------------------------
"""

global seasons_diff
global seasons
seasons_diff = ["2010-2011","2011-2012","2012-2013","2013-2014","2014-2015","2015-2016","2016-2017","2017-2018","2018-2019","2019-2020"]
seasons = ["2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020"]

'''
Documentation, variables
------------------------------------------------------------------------------------
'''

fixtures_var = ['fixture_id','league_id','league','event_date','event_timestamp','firstHalfStart',\
'secondHalfStart','round','status','statusShort','elapsed','venue','referee','homeTeam','awayTeam',\
'goalsHomeTeam','goalsAwayTeam','score']

team_var = ['team_id', 'team_name', 'logo']

leagues_var = ['league_id','name','type','country','country_code','season','season_start',\
'season_end','logo','flag','standings','is_current','coverage']

odds_var = ['fixture', 'bookmakers']

events_var = ['elapsed','elapsed_plus','team_id','teamName','player_id','player','assist_id',\
'assist','type','detail','comments']

lineups_var = ['teamAXXX, teamVXXX']

statistics_fixture_var = ['Shots on Goal','Shots off Goal','Total Shots','Blocked Shots','Shots insidebox','Shots outsidebox',\
'Fouls','Corner Kicks','Offsides','Ball Possession','Yellow Cards','Red Cards','Goalkeeper Saves','Total passes',\
'Passes accurate','Passes %']

statistics_team_var = ['matchs', 'goals', 'goalsAvg']

players_squad_var = ['player_id','player_name','firstname','lastname','number','position','age',\
'birth_date','birth_place','birth_country','nationality','height','weight']

players_statistics_var = ['player_id','player_name','firstname','lastname','number','position','age','birth_date','birth_place',\
'birth_country','nationality','height','weight','injured','rating','team_id','team_name','league_id','league','season','captain',\
'shots','goals','passes','tackles','duels','dribbles','fouls','cards','penalty','games','substitutes']

players_transfers_var = ['player_id','player_name','transfer_date','type','team_in','team_out','lastUpdate']

players_statistics_fixtures_var = ['event_id','updateAt','player_id','player_name','team_id','team_name','number','position','rating',\
'minutes_played','captain','substitute','offsides','shots','goals','passes','tackles','duels','dribbles','fouls','cards','penalty']

coachs_var = ['id','name','firstname','lastname','age','birth_date','birth_place','birth_country','nationality','height',\
'weight','team','career']

trophies_var = ['league', 'country', 'season', 'place']

sidelined_var = ['type', 'start', 'end']

'''
Only Function
------------------------------------------------------------------------------------
'''


    
    
    
