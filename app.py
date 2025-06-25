from flask import Flask, render_template, request, redirect, request, jsonify

import sqlite3
import os

app = Flask(__name__)

BUG_FILE = 'bugs.db'

def init_dbs():
    conn = sqlite3.connect(BUG_FILE)
    c = conn.cursor()

    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(25) NOT NULL,
            description VARCHAR(255)
        )
        '''
    )
    # then populate the projects

    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag VARCHAR(15) NOT NULL UNIQUE
        )
        '''
    )
    # then populate the tags
    
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS bugs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(100) NOT NULL,
            description VARCHAR(255) NOT NULL,
            status TEXT DEFAULT 'Open',
            severity TEXT NOT NULL,
            solution VARCHAR(100),
            created DATE
        )
        '''
    )

#table relation for bugs and their tags
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS bugs_tags (
            bug_id INTEGER NOT NULL REFERENCES bugs(id),
            tag_id INTEGER NOT NULL REFERENCES tags(id)
            PRIMARY KEY (bug_id, tag_id)

        )
        '''
    )

# table for bugs and project associated if there is any
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS project_bugs (
            bug_id INTEGER NOT NULL REFERENCES bugs(id),
            project_id INTEGER NOT NULL REFERENCES projects(id)
            PRIMARY KEY (bug_id, project_id)
        )
        '''
    )

    conn.commit()
    conn.close()

