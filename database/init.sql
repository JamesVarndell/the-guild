DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS characters;
DROP TABLE IF EXISTS enemies;
DROP TABLE IF EXISTS encounters;
DROP TABLE IF EXISTS user_encounter;
DROP TABLE IF EXISTS encountered_enemy;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS inventories;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE characters (
  user__id INTEGER PRIMARY KEY REFERENCES users,
  vitals TEXT NOT NULL,
  attributes TEXT NOT NULL,
  skills TEXT NOT NULL,
  buffs TEXT NOT NULL,
  abilities TEXT,
  stances TEXT,
  effects TEXT,
  inventory TEXT,
  body TEXT
);

CREATE TABLE enemies (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  description TEXT NOT NULL,
  vitals TEXT NOT NULL,
  attributes TEXT NOT NULL,
  skills TEXT,
  buffs TEXT,
  abilities TEXT,
  effects TEXT,
  drops TEXT,
  body TEXT
);

CREATE TABLE encounters (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  image TEXT,
  text TEXT,
  area TEXT,
  weight INTEGER,
  options TEXT,
  enemy__name TEXT REFERENCES enemies
);

CREATE TABLE user_encounter (
  user__id INTEGER PRIMARY KEY REFERENCES users,
  encounter__id INTEGER REFERENCES encounters,
  text TEXT NOT NULL,
  image TEXT,
  state TEXT,
  options TEXT,
  turns INTEGER,
  started TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE encountered_enemy (
  user__id INTEGER PRIMARY KEY REFERENCES users,
  enemy__id INTEGER REFERENCES enemies,
  vitals TEXT NOT NULL,
  buffs TEXT,
  effects TEXT
);

CREATE TABLE items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  description TEXT NOT NULL,
  image TEXT NOT NULL,
  type TEXT NOT NULL,
  properties TEXT NOT NULL
);

CREATE TABLE inventories (
  user__id INTEGER PRIMARY KEY REFERENCES users,
  contents TEXT
);