-- Check if tournament db exists. If YES, drop database. If NO, create database.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

-- connect to tournament database so tables will be created in the correct db
\c tournament

-- Drop/Create players table w/columns (id, name)
-- this table also holds the wins/matches record for each player
DROP TABLE IF EXISTS players CASCADE; --CASCADE needed to remove dependency
CREATE TABLE players (
	id serial not null,
	full_name text not null,
	PRIMARY KEY(id)
);

-- Drop/Create matches table w/columns (winner id, loser id)
-- winner id and loser id refers to the id in the players table
DROP TABLE IF EXISTS matches;
CREATE TABLE matches (
	id serial not null,
	winner_id int references players(id) not null,
	loser_id int references players(id) not null,
	PRIMARY KEY(id)
);
