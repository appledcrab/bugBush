# database.py

# all the information/functions relating to sqlite 

import sqlite3
import os

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

    conn.commit()
    conn.close()

# Selects all the bugs from bugs table
# => returns a dictionary of them
def get_bugs():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT id, title, description, status, severity, created FROM bugs")
    bugs = [dict(id=row[0], title=row[1], description=row[2], status=row[3], severity=row[4], created=row[5]) for row in c.fetchall()]
    conn.close()
    return bugs

# Given title, descr, status, and severity, adds bug to the table 
#  => returns lastrowid / primary key

# will need to go into more detail of adding a connected project, adding more tags, and possibly
# add a solution to it at addition if it was a past bug
# would then also need to then to add an edit 
def add_bug(title, description, status, severity):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO bugs (title, description, status, severity, created) VALUES (?, ?, ?, ?, date('now'))",
              (title, description, status, severity))
    conn.commit()
    conn.close()
    return c.lastrowid