from flask import Flask, render_template, request, redirect, request, jsonify
from database import init_db, insert_example, get_bugs, add_bug

import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# returns json file from dictionary of bugs (might change?)
@app.route('/api/bugs',methods=['GET'])
def api_get_bugs():
    bugs = get_bugs()
    return jsonify(bugs)

# adds bug calling add_bug. adds the default '', Open and Medium if left null.
@app.route('/api/bugs',methods=['POST'])
def api_add_bug():
    # bug_key = add_bug(b_title,b_desc,b_status,b_sever)
    bug = request.json
    try:
        bug_id = add_bug(
        title = bug['title'],
        description= bug.get('description',''),
        status= bug.get('status','Open'),
        severity= bug.get('severity','Medium')
        )

        return jsonify({'status': 'success', 'bug_id': bug_id})
    
    except Exception as e:
        print(f"Unexpected Error occured: {e}")
    
    
if __name__ == '__main__':
    init_db()
    app.run(debug=True)