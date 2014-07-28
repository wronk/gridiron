"""
Created on July 27th

@author: wronk

Functions to compute points for offense, kickers, and defense based on stats
Point values based on ESPN standard scoring system guide
"""


def point_parse_off(rushOrRecieveTD=0, kickoffOrPuntTD=0, fumbleTD=0,
                    passingTD=0, rushOrRecieve2PtConv=0, passing2PtConv=0,
                    ydsRushingOrRecieving=0, ydsPassing=0,
                    rushOrRecieveTD40Plus=0, passingTD40Plus=0,
                    INT=0, fumbleLost=0):
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
        06 * rushOrRecieveTD +
        06 * kickoffOrPuntTD +
        06 * fumbleTD +
        04 * passingTD +
        02 * rushOrRecieve2PtConv +
        02 * passing2PtConv +
        01 * ydsRushingOrRecieving % 10 +
        01 * ydsPassing % 25 +
        02 * rushOrRecieveTD40Plus +
        02 * passingTD40Plus +
        -2 * INT +
        -2 * fumbleLost)
    return pts


def points_parse_kick(made=None, missed=None, PAT=0, twoPtConv=0):
    """Compute points for kicking events

    Parameters
    ----------
    made : list
        List of made kicks in yards
    missed : list
        List of missed kicks in yards
    PAT : int
        Number of point-after-touchdown kicks made
    twoPtConv : int
        Number of 2-pt conversions passed, ran, or caught

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

    for kick in missed:
        if kick < 40:
            pts += -2
        else:
            pts += -1

    pts += 1 * PAT
    pts += 2 * twoPtConv

    return pts


def points_parse_def(ptsAgainst=0, TD=0, INT=0, fumbleRecovery=0,
                     blockedKick=0, safety=0, sack=0):
    """Compute points for defensive events

    Parameters
    ----------
    ptsAgainst : int
        Number of points scored by opposing team (includes all points)
    TD : int
        Number of touchdowns scored
    INT : int
        Number of interceptions made
    fumbleRecovery : int
        Number of fumbles recovered
    blockedKick : int
        Number of field goals, punts, or PATs blocked
    safety : int
        Number of safeties
    sack : int
        Number of sacks

    Returns
    -------
    pts : int
        Number of points scored by defensive squad
    """
    # Check that points against has a reasonable value
    if ptsAgainst < 0 or ptsAgainst > 70:
        raise ValueError('Points against not between 0-70')

    pts = (
        3 * TD +
        2 * INT +
        2 * fumbleRecovery +
        2 * blockedKick +
        2 * safety +
        1 * sack)

    # point divisions for points scored against
    ptDivs = [2, 7, 14, 18, 22, 28, 35, 46]
    ptDivAllot = [10, 7, 4, 1, 0, -1, -4, -7, -10]

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
    elif ptsAgainst >= ptDivs[5] and ptsAgainst < ptDivs[6]:
        pts += ptDivAllot[6]
    elif ptsAgainst >= ptDivs[6] and ptsAgainst < ptDivs[7]:
        pts += ptDivAllot[7]
    elif ptsAgainst >= ptDivs[7]:
        pts += ptDivAllot[8]

    return pts

    '''
    ptsOff = [(6, 'Rush/Recieve TD'),
            (6, 'Return kick/punt TD'),
            (6, 'Return/recover for TD'),
            (4, 'Passing TD'),
            (2, 'Rush/recieve 2-pt conv.')
            (2, 'Passing 2-pt conv.'),
            (1, 'Pts/10 yds rush/recieve'),
            (1, 'Pts/25 yds passing'),
            (02, 'Rush/recieve TD of 40+ yds'),
            (02, 'Passing TD of 40+ yds'),
            (-2, 'Pass intercepted'),
            (-2, 'Fumble lost'),
            (05, '50+)
            '''
