"""
@author wronk
"""

import nfldb
import numpy as np
import itertools
#import sklearn

db = nfldb.connect()

#######################################
### Params
stats_off = ['passing_cmp', 'passing_att', 'passing_int', 'passing_yds',
             'passing_tds', 'rushing_yds', 'rushing_tds']
stats_def = ['defense_int', 'defense_pass_def', 'defense_qbhit',
             'defense_sk', 'defense_frec']
def_pos = ['DE', 'DT', 'LB', 'OLB', 'LB', 'MLB', 'ILB', 'CB',
           'SS', 'FS', 'NT', 'NB', 'DB', 'SAF']
seasons = [2012, 2013]
pos = 'QB'

#######################################
### Get list of QBs to make predictions on
q = nfldb.Query(db).game(season_year=seasons, season_type='Regular')
q.player(years_pro__ge=len(seasons), position=pos)

# GSIS ID number of matching QBs
qb_id = [p.player_id for p in q.as_players()]
qb_team = [p.team for p in q.as_players()]
qb_id = qb_id[0:1]
#######################################
### Cull selected stats for all these QBs
qb_game_ids = []  # List of lists of game GSIS ID numbers
qb_game_agg = []  # List of lists of PlayPlayer objects for each game

# Get game ID numbers for each player
for player_id in qb_id:
    q = nfldb.Query(db).game(season_year=seasons, season_type='Regular')
    q.player(player_id=player_id)
    qb_game_ids.append([g.gsis_id for g in q.as_games()])

# get all stats on a game by game basis for each player
for player_id, g_list in zip(qb_id, qb_game_ids):
    temp_list = []
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
            player_select_stats[gi, stats_off.index(attr)] = \
                getattr(game, attr)
    qb_select_stats.append(player_select_stats)

#######################################
### Pull desired defensive stats from set of all stats
# Get opposing team
stats_desired = ['defense_int', 'defense_qbhit']
team = 'NE'
season_type = 'Regular'
q = nfldb.Query(db).game(season_year=seasons, season_type=season_type,
                         team=team)
def_games = q.as_games()
# Get all stats for desired team
team_select_stats = np.zeros((len(def_games), len(stats_desired)))

for gi, g in enumerate(def_games):
    temp_array = np.zeros((len(g.play_players), len(stats_desired)))
    for ppi, pp in enumerate(g.play_players):
        for attr in pp.fields.intersection(stats_desired):
            temp_array[ppi, stats_desired.index(attr)] = getattr(pp, attr)
        team_select_stats[gi, :] = temp_array.sum(axis=0)

# Get select stats for some number of games

'''
# Get list of defensive player IDs faced by QB for a game

# Get identifiers for list of plays QB played in
qb_play_ids = []
for player_id, g_list in zip(qb_id, qb_game_ids):
    temp_list = []
    for g_id in g_list:
        q = nfldb.Query(db).game(gsis_id=g_id)
        q.player(player_id=player_id) temp_list.append([(play.gsis_id, play.drive_id, play.play_id)
                          for play in q.as_plays()])
    qb_play_ids.append(temp_list)
#import pdb; pdb.set_trace()
# Get PlayPlayer objects for each Play
#TODO: missing game list loop I think. Iterate over: QB, game, play
def_players = []
for qb_game_list in qb_play_ids:
    temp_qb_game_opp = []
    # Iterate over a list of plays for one game
    for play_list in qb_game_list:
        for (gsis_id, drive_id, play_id) in play_list:
            p = nfldb.Play.from_id(db, gsis_id, drive_id, play_id)
            #q = nfldb.Query(db).game(gsis_id=g_id).drive(drive_id=drive_id)
            #q.play(play_id=play_id)
            #pdb.set_trace()
            temp_qb_game_opp.append([pp.player.player_id for pp in p.play_players
                                     if pp.team is not pp.play.pos_team])

        #TODO: get unique player IDs
        def_players.append(list(itertools.chain.from_iterable(temp_qb_game_opp)))


# Get unique list of defensive players from PlayPlayer object
'''


'''
# get all stats on a game by game basis for each player
qb_def_players = []
for gi, g_list in enumerate(qb_game_ids):
    temp_list=[]
    for g_id in g_list:
    q = nfldb.Query(db).game(gsis_id=g_id)
    #q.player(position='DB')
    temp_list.append([(p.full_name, p.player_id, p.team)
                      for p in q.as_players()
                      if p.position.name in def_pos and p.team != qb_team[gi]])
    qb_def_players.append(temp_list)
'''
#######################################


def team_def_stats(team, stats_desired, seasons=[2013],
                   season_type='Regular'):

    # in: team, year, stats desired
    # out: avg stats over games desired

    q = nfldb.Query(db).game(season_year=seasons, season_type=season_type,
                            team=team)
    def_games = q.as_games()
    # Get all stats for desired team
    team_select_stats = np.zeros((len(def_games), len(stats_desired)))

    for gi, g in enumerate(def_games):
        temp_array = np.zeros((len(g.play_players), len(stats_desired)))
        for ppi, pp in enumerate(g.play_players):
            for attr in pp.fields.intersection(stats_desired):
                temp_array[ppi, stats_desired.index(attr)] = getattr(pp, attr)
            team_select_stats[gi, :] = temp_array.sum(axis=0)

    return team_select_stats

#######################################
def player_def_stats(player_id, team, stats_desired, seasons=[2013],
                     season_type='Regular'):

    # in: player, team, year, stats desired
    # out: avg stats over games desired

    # Get game ID numbers (GSIS_ID) for player of interest
    game_ids = []
    q = nfldb.Query(db).game(season_year=seasons, season_type=season_type)
    q.player(player_id=player_id)
    game_ids.append([g.gsis_id for g in q.as_games()])

    # Get all stats on a game by game basis for desired player
    player_stats_all = []
    for g_id in game_ids:
        q = nfldb.Query(db).game(season_year=seasons, gsis_id=g_id)
        q.player(player_id=player_id)
        player_stats_all.append(q.as_aggregate()[0])

    # Get desired stats on a game by game basis for desired player
    player_select_stats = np.zeros((len(game_ids), len(stats_desired)))
    for gi, game in enumerate(player_stats_all):
        for attr in game.fields.intersection(stats_desired):
            player_select_stats[gi, stats_off.index(attr)] = \
                getattr(game, attr)

    return player_select_stats

