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


# need to reexecute 
    c.execute("SELECT COUNT(*) FROM tags")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO tags (tag) VALUES (?)", [
            ('ui',),
            ('backend',),
            ('crash',),
            ('performance',),
            ('learning',),
            ('sqlite',),
            ('python',),
            ('javascript',),
            ('java',)
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
            emoji TEXT,
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

# def bug_exists(bug_id)
    
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

# will need to go into more detail of adding a connected project, adding more tags
# would then also need to then to add an edit 
def add_bug(title: str, description: str, emoji='🐞', solution = '', status='Open', severity='Medium') -> int:
    conn = get_db_connection()
    try:
        c = conn.cursor()
        c.execute("INSERT INTO bugs (title, description, emoji, status, severity, solution, created) VALUES (?, ?, ?, ?, ?, ?, date('now'))",
                (title, description, emoji, status, severity, solution))
        conn.commit()
        return c.lastrowid
    finally:
        conn.close()

def update_bug(bug_id: int, title: str, description: str, emoji='🐞',solution: str = '', status: str = 'Open', severity: str = 'Medium') -> bool:
    conn = get_db_connection()
    try:
        c = conn.cursor()
        c.execute(
            "UPDATE bugs "
            "SET title = ?, description = ?, solution = ?, emoji = ?, status = ?, severity = ? "
            "WHERE id = ?",
            (title, description, solution, emoji, status, severity, bug_id)
        )
        conn.commit()
        return True 
    except sqlite3.Error as e:
        print(f"Database Error: {e}")
        return False  
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

# Mostly for testing purposes but can be kept as a reset
def delete_all_bugs():
    conn = get_db_connection()
    try:
        c = conn.cursor()
        c.execute("DELETE FROM bugs")
        conn.commit()
    finally:
        conn.close()



# tags table

"""
getting tag text based on tag id
returns string of what the tag is
"""
def get_tag(tag_id: int):
    conn = get_db_connection()
    try:
        c = conn.cursor()
        c.execute("SELECT tag FROM tags WHERE id = ?",(tag_id))
        row = c.fetchone()
        if not row:
            raise ValueError(f"Tag with ID {tag_id} does not exist.")
        return row[1]

    finally:
        conn.close()

"""
# given bug id and tag,
use check and add tag
# then use that tag id and given bug id to add relationship to tags table
"""
def add_tag_bug_relationship(tag_text: str, bug_id: int):
    conn = get_db_connection()
    try:
        tag_id = check_and_add_tag(tag_text=tag_text)
        # additionally should check that the bug_id exists. get_bug returns a dict of the bug if found
        bug = get_bug(bug_id=bug_id)
        if not bug:
            raise ValueError(f"Bug with ID {bug_id} does not exist.")
        
        c = conn.cursor()
        c.execute("INSERT INTO bugs_tags (bug_id, tag_id) VALUES (?, ?)",(bug_id,tag_id))

    finally:
        c.close()

"""
given tag text, check if it exists already in tag table, if not, add it
return tag id

"""
def check_and_add_tag(tag_text: str):
    conn = get_db_connection()
    try:
        tag_text = tag_text.lower()
        # using lower case so UI and ui are the same
        c = conn.cursor()
        c.execute("SELECT id FROM tags WHERE tag = ?",(tag_text))
        row = c.fetchone()
        if row:
            return row[0]
        else:
            c.execute("INSERT INTO tags (tag) VALUES (?)",(tag_text))
            conn.commit()
            return c.lastrowid
    finally:
        conn.close()
"""
"getting the relationship so it can be accessed - read"
"needs to go through the relationship, get the tag ids and check them in the tag table"

returns empty array og tags if none found
"""


def get_bug_tags(bug_id:int):
    conn = get_db_connection()
    try:
        c = conn.cursor()
        c.execute("SELECT tag_id FROM bugs_tags WHERE bug_id = ?",(bug_id))
        rows = c.fetchall()
        if not rows:
            return []
            # possibility for bug id to not exist in table -> having no bugs
        
        # now needs to go through tag table
        # and adding it to list?
        tags = []
        for (tag_id,) in rows:
            try:
                tags.append(get_tag(tag_id))
            except ValueError as e:
                print(f"Warning: {e}")
        return tags
        

    finally:
        conn.close()
