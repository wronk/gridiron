"""
@author wronk
"""

import nfldb
import numpy as np
#import sklearn

db = nfldb.connect()

#######################################
### Params
stats_off = ['passing_cmp', 'passing_att', 'passing_int', 'passing_yds',
	     'passing_tds', 'rushing_yds', 'rushing_tds']
stats_def = ['defense_int', 'defense_pass_def', 'defense_qbhit',
	     'defense_sk', 'defense_frec']

seasons = [2012, 2013]
pos = 'QB'

#######################################
### Get list of QBs to make predictions on
q = nfldb.Query(db).game(season_year=seasons, season_type='Regular')
q.player(years_pro__ge=len(seasons), position=pos)

# GSIS ID number of matching QBs
qb_id = [p.player_id for p in q.as_players()]
qb_id = qb_id[0:2]
#######################################
### Cull selected stats for all these QBs
qb_game_ids = []
qb_game_agg = []

# get player ID numbers 
for player_id in qb_id:
    q = nfldb.Query(db).game(season_year=seasons, season_type='Regular')
    q.player(player_id=player_id)
    qb_game_ids.append([g.gsis_id for g in q.as_games()])

# get all stats on game by game basis for each player
for player_id, g_list in zip(qb_id, qb_game_ids):
    temp_list=[]
    for g_id in g_list:
	q = nfldb.Query(db).game(season_year=seasons, season_type='Regular',
					  gsis_id=g_id)
	q.player(player_id=player_id)
	temp_list.append(q.as_aggregate()[0])				

    qb_game_agg.append(temp_list)

#######################################
### Pull selected stats from set of all stats

# find intersection of recorded stats and desired stats
for player_game_list in qb_game_agg:
    for game in player_game_list:
	for attr in game.fields.intersection(stats_off):
	    print attr


#union = pp.fields.intersection(stats_off)

#######################################
