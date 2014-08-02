"""
Created on July 27th

@author: wronk

Functions to compute points for offense, kickers, and defense based on stats
Point values based on ESPN standard scoring system guide
"""


def point_parse_off(passing_yds=0, passing_tds=0, passing_int=0, rushing_yds=0,
		    rushing_tds=0, receiving_tds=0, receiving_yds=0,
		     receiving_twoptm=0,
 		    rushing_twoptm=0, fumbles_lost=0, fumbles_rec_tds=0):
    """Compute points for offensive events

    Parameters
    ----------
    rushOrRecieveTD : int
        Number of rushing or recieving TDs

    Returns
    -------
    pts : int
        Number of points scored by offensive player
    """

    # Could alternatively put this in text/excel file and load it
    pts = (
        01 * (passing_yds % 25) +
        04 * passing_tds +
        -1 * passing_int +
        01 * (rushing_yds % 10) +
        06 * rushing_tds +
	01 * (receiving_yds % 10) +
        06 * receiving_tds +
        02 * (receiving_twoptm + rushing_twoptm)
        -2 * fumbles_lost +
        06 * fumbles_rec_tds)

    if passing_yds >= 300:
	pts += 2
    if rushing_yds >= 100:
	pts += 3
    if passing_yds >= 100:
	pts += 2

    return pts


def points_parse_kick(kicking_fgm_yds=None, kicking_xpmade=0):
    """Compute points for kicking events

    Parameters
    ----------
    made : list
        List of made kicks in yards
    PAT : int
        Number of point-after-touchdown kicks made

    Returns
    -------
    pts : int
        Number of points scored by kicking player
    """
    pts = 0
    for kick in made:
        if kick < 40:
            pts += 3
        elif kick >= 40 and kick < 50:
            pts += 4
        else:
            pts += 5

    '''
    for kick in missed:
        if kick < 40:
            pts += -2
        else:
            pts += -1
    '''

    pts += 1 * PAT

    return pts


def points_parse_def(defense_sk=0, defense_int=0, defense_frec=0,
		     defense_frec_tds=0, defense_int_tds=0,
		     defense_misc_tds=0, defense_safe=0, defense_fgblk=0,
		     defense_puntblk=0, kickret_tds=0, pntret_tds=0,
		     pts_against=0)
    """
    Parameters
    ----------
    pts_against : int
        Number of points scored by opposing team (includes all points)
    defense_int : int
        Number of defensive interceptions 
    defense_frec : int
        Number of fumble recoveries

    #TODO: finish up rest of doc
    Returns
    -------
    pts : int
        Number of points scored by defensive squad
    """
    # Check that points against has a reasonable value
    if pts_against < 0 or pts_against > 70:
        raise ValueError('Points against not between 0-70')

    pts = (
        01 * defense_sk +
        02 * defense_int +
	02 * defense_frec +
        06 * (defense_frec_tds + defense_int_tds + defense_misc_tds)
        02 * defense_safe +
        02 * (defense_fgblk + defense_puntblk) +
        06 * (kickret_tds + pntret_tds))

    # point divisions for points scored against
    ptDivs = [2, 7, 14, 21, 28, 35]
    ptDivAllot = [10, 7, 4, 1, 0, -1, -4]

    # Compute FF points for defense/special teams points scored against
    if ptsAgainst == 0:
        pts += ptDivAllot[0]
    elif ptsAgainst >= ptDivs[0] and ptsAgainst < ptDivs[1]:
        pts += ptDivAllot[1]
    elif ptsAgainst >= ptDivs[1] and ptsAgainst < ptDivs[2]:
        pts += ptDivAllot[2]
    elif ptsAgainst >= ptDivs[2] and ptsAgainst < ptDivs[3]:
        pts += ptDivAllot[3]
    elif ptsAgainst >= ptDivs[3] and ptsAgainst < ptDivs[4]:
        pts += ptDivAllot[4]
    elif ptsAgainst >= ptDivs[4] and ptsAgainst < ptDivs[5]:
        pts += ptDivAllot[5]
    elif ptsAgainst >= ptDivs[5]:
        pts += ptDivAllot[6]

    return pts
