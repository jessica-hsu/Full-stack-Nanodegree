#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    curse = conn.cursor()
    sql = "DELETE FROM matches"
    curse.execute(sql)
    sql = "UPDATE players SET wins = 0, matches = 0"
    curse.execute(sql)
    conn.commit()
    curse.close()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    curse = conn.cursor()
    sql = "DELETE FROM players"
    curse.execute(sql)
    conn.commit()
    curse.close()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    curse = conn.cursor()
    sql = "SELECT count(id) AS num_players FROM players"
    curse.execute(sql)
    result = curse.fetchone()
    curse.close()
    conn.close()
    return result[0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    curse = conn.cursor()
    sql = "INSERT INTO players (full_name, wins, matches) VALUES (%s, %s, %s)"
    data = [name, 0, 0]
    curse.execute(sql, data)
    conn.commit()
    curse.close()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    conn = connect()
    curse = conn.cursor()
    sql = "SELECT id, full_name, wins, matches FROM players ORDER BY wins"
    curse.execute(sql)
    result = curse.fetchall()
    curse.close()
    conn.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    curse = conn.cursor()
    sql = "INSERT INTO matches (winner_id, loser_id) VALUES (%s, %s)"
    data = [winner, loser]
    curse.execute(sql, data)
    sql = "UPDATE players SET wins = wins + 1, matches = matches + 1 WHERE id = %s"
    data = [winner]
    sql_2 = "UPDATE players SET matches = matches + 1 WHERE id = %s"
    data_2 = [loser]
    curse.execute(sql, data)
    curse.execute(sql_2, data_2)
    conn.commit()
    curse.close()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    rankings = playerStandings()
    swiss = []
    for i in range(0,len(rankings)-1,2):
        tup = (rankings[i][0], rankings[i][1], rankings[i+1][0], rankings[i+1][1])
        swiss.append(tup)

    return swiss
