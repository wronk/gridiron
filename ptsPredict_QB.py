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
#qb_id = qb_id[0:2]
#######################################
### Cull selected stats for all these QBs
qb_game_ids = [] # List of lists of game GSIS ID numbers
qb_game_agg = [] # List of lists of PlayPlayer objects for each game

# Get game ID numbers for each player
for player_id in qb_id:
    q = nfldb.Query(db).game(season_year=seasons, season_type='Regular')
    q.player(player_id=player_id)
    qb_game_ids.append([g.gsis_id for g in q.as_games()])

# get all stats on a game by game basis for each player
for player_id, g_list in zip(qb_id, qb_game_ids):
    temp_list=[]
    for g_id in g_list:
	q = nfldb.Query(db).game(season_year=seasons, season_type='Regular',
					  gsis_id=g_id)
	q.player(player_id=player_id)
	temp_list.append(q.as_aggregate()[0])				

    qb_game_agg.append(temp_list)

#######################################
### Pull desired offensive stats from set of all stats

qb_select_stats = []
# find intersection of recorded stats and desired stats
for player_game_list in qb_game_agg:
    player_select_stats = np.zeros((len(player_game_list), len(stats_off)))
    for gi, game in enumerate(player_game_list):
	for attr in game.fields.intersection(stats_off):
	    player_select_stats[gi, stats_off.index(attr)] = getattr(game, attr)
    qb_select_stats.append(player_select_stats)

#######################################
### Pull desired defensive stats from set of all stats
# Get list of defensive player IDs faced by QB for a game

# Get list of plays QB played in
# Get PlayPlayer objects for each Play
# Get unique list of defensive players from PlayPlayer object
#######################################
def player_def_stats(player_id, team, stats_desired, seasons=[2013],
		     season_type='Regular'):

    # in: player, team, year, stats desired
    # out: avg stats over games desired
    
    # Get game ID numbers (GSIS_ID) for player of interest
    game_ids=[]
    q = nfldb.Query(db).game(season_year=seasons, season_type=season_type)
    q.player(player_id=player_id)
    game_ids.append([g.gsis_id for g in q.as_games()])

    # Get all stats on a game by game basis for desired player
    player_stats_all = []
    for g_id in game_ids:
	q = nfldb.Query(db).game(season_year=seasons, gsis_id=g_id)
	q.player(player_id=player_id)
	player_stats_all.append(q.as_aggregate()[0])

    # Get all stats on a game by game basis for desired player
    player_select_stats = np.zeros((len(game_ids), len(stats_desired)))
    for gi, game in enumerate(player_game_list):
	for attr in game.fields.intersection(stats_off):
	    player_select_stats[gi, stats_off.index(attr)] = getattr(game, attr)
