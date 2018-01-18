-- Check if tournament db exists. If YES, drop database. If NO, create database.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

-- Drop/Create players table w/columns (id, name)
DROP TABLE IF EXISTS players CASCADE; --CASCADE needed to remove dependency
CREATE TABLE players {
	id serial not null,
	name varchar(30) not null,
	PRIMARY KEY(id)
};

-- Drop/Create matches table w/columns (winner id, loser id)
DROP TABLE IF EXISTS matches;
CREATE TABLE matches {
	winner_id serial references players(id) not null,
	loser_id serial references players(id) not null
};

-- Drop/Create standings table w/columns (id, wins, matches)
DROP TABLE IF EXISTS standings;
CREATE TABLE standings {
	id serial references players(id) not null,
	wins int,
	matches int
};