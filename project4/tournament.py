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
    conn = connect() # get database connection
    cursor = conn.cursor()
    sql = "DELETE FROM matches"
    cursor.execute(sql)
    # commit is used to make sure database changes are actually made
    conn.commit()
    # close cursor and database connection
    cursor.close()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    sql = "DELETE FROM players"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    sql = "SELECT count(id) AS num_players FROM players"
    cursor.execute(sql)
    # grab the first row of the result from sql query
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    # result[0] refers to the first column, num_players
    return result[0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    sql = "INSERT INTO players (full_name) VALUES (%s)"
    data = [name] # name as passed param
    cursor.execute(sql, data) # the proper way of passing variables to SQL queries in python
    conn.commit()
    cursor.close()
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
    cursor = conn.cursor()
    # order results by number of wins. Default is DESCENDING so highest number of wins is first row
    # case statement added to make num matches 0 when player did not play any games yet
    sql = "SELECT p.id, full_name, count(winner_id) as wins, \
    CASE WHEN (SELECT COUNT(*) FROM matches WHERE winner_id = p.id \
     OR loser_id = p.id) = 0 THEN 0 ELSE COUNT(*) END AS matches \
    FROM players p FULL JOIN matches m \
    ON p.id = m.winner_id \
    GROUP BY full_name, p.id \
    ORDER BY wins DESC";
    cursor.execute(sql)
    # fetchall() takes all the results and returns them as a list of tuples
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    sql = "INSERT INTO matches (winner_id, loser_id) VALUES (%s, %s)"
    data = [winner, loser]
    cursor.execute(sql, data)
    conn.commit()
    cursor.close()
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
    # get full list of players and where they stand in terms of wins
    rankings = playerStandings()
    # create empty list to hold all the pairings
    swiss = []
    for i in range(0,len(rankings)-1,2):
        # rankings return a list of players already in order so just grab them by two's to get each pairing
        tup = (rankings[i][0], rankings[i][1], rankings[i+1][0], rankings[i+1][1])
        # add pairing to end of list
        swiss.append(tup)

    #return list of pairings
    return swiss
