
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS class;
DROP TABLE IF EXISTS gpa;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE class
 (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  classname TEXT NOT NULL,
  classtype TEXT NOT NULL,
  length INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  grade TEXT NOT NULL,
  worth REAL NOT NULL,
  realworth REAL NOT NULL,

  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE gpa (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  gpa REAL NOT NULL,

FOREIGN KEY (user_id) REFERENCES user (id)
)