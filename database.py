# database.py

# all the information/functions relating to sqlite 

import sqlite3
# import os
from typing import List, Dict, Optional

DB_FILE = 'bugs.db'

def get_db_connection():
    return sqlite3.connect(DB_FILE)

# Inserts into tables projects and tags with example ones if they are empty
def insert_example():
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM projects")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO projects (title, description) VALUES (?, ?)", [
            ('Web App', 'A sample frontend-backend project'),
            ('Game Mod', 'Fun experimental mod'),
            ('Portfolio Site', 'Personal website project')
        ])


    c.execute("SELECT COUNT(*) FROM tags")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO tags (tag) VALUES (?)", [
            ('UI',),
            ('Backend',),
            ('Crash',),
            ('Performance',),
            ('Learning',),
            ('SQLite',),
            ('Python',),
            ('JavaScript',),
            ('Java',)
        ])
    
    conn.commit()
    conn.close()

def init_db():
    conn = get_db_connection()
    # enables foreign key constraints that are for some reason disabled by default
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()

    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(25) NOT NULL,
            description VARCHAR(255)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag VARCHAR(15) NOT NULL UNIQUE
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS bugs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(100) NOT NULL,
            description VARCHAR(255) NOT NULL,
            status TEXT DEFAULT 'Open',
            severity TEXT NOT NULL,
            solution VARCHAR(100),
            created DATE
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS bugs_tags (
            bug_id INTEGER NOT NULL REFERENCES bugs(id),
            tag_id INTEGER NOT NULL REFERENCES tags(id),
            PRIMARY KEY (bug_id, tag_id)
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS project_bugs (
            bug_id INTEGER NOT NULL REFERENCES bugs(id),
            project_id INTEGER NOT NULL REFERENCES projects(id),
            PRIMARY KEY (bug_id, project_id)
        )
    ''')

    insert_example()

    conn.commit()
    conn.close()

# Selects a single bug from the table given an ID
# => returns a dictionary of the the specific bug
def get_bug(bug_id: int) -> Optional[Dict] :
    conn = get_db_connection()
    try:
        conn.row_factory=sqlite3.Row # this would allow for easier/readable testing as it will be structured like the table itself.
        c = conn.cursor()
        c.execute("SELECT * FROM bugs WHERE id = ?",(bug_id,))
        row = c.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()
    
# Returns all bugs 
# => returns dictionary of all of the bugs
def get_all_bugs() -> List[Dict] :
    conn = get_db_connection()
    try:
        conn.row_factory=sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM bugs")
        rows = c.fetchall()
        # prev issue: dict(rows) would try to turn entire rows into a dict instead of
        # each row into a dict like we want
        return [dict(row) for row in rows ]if rows else None
    finally:
        conn.close()




# Returns all bugs with specific filters (Project, tags, Open,etc)



# Given title, descr, status, and severity, adds bug to the table 
#  => returns lastrowid / primary key

# will need to go into more detail of adding a connected project, adding more tags, and possibly
# add a solution to it at addition if it was a past bug
# would then also need to then to add an edit 
def add_bug(title: str, description: str, status = 'Open', severity= 'Medium') -> int:
    conn = get_db_connection()
    try:
        c = conn.cursor()
        c.execute("INSERT INTO bugs (title, description, status, severity, created) VALUES (?, ?, ?, ?, date('now'))",
                (title, description, status, severity))
        conn.commit()
        return c.lastrowid
    finally:
        conn.close()


# Mostly for testing purposes
def delete_all_bugs():
    conn = get_db_connection()
    try:
        c = conn.cursor()
        c.execute("DELETE FROM bugs")
        conn.commit()
    finally:
        conn.close()

def delete_bug(bug_id: int):
    conn = get_db_connection()
    try:
        c = conn.cursor()
        c.execute("DELETE FROM bugs WHERE id = ?",(bug_id,))
        conn.commit()
    finally:
        conn.close()