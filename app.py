from flask import Flask, render_template, request, redirect, request, jsonify
from database import init_db,get_all_bugs, add_bug, update_bug, delete_bug



import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# returns json file from dictionary of bugs (might change?)
@app.route('/api/bugs',methods=['GET'])
def api_get_bugs():
    bugs = get_all_bugs()
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
        severity= bug.get('severity','Medium'),
        solution= bug.get('solution','')
        )

        return jsonify({'status': 'success add', 'bug_id': bug_id})
    
    except Exception as e:
        print(f"Unexpected Error occured: {e}")

# upadting bug given its bugID
@app.route('/api/bugs/<int:bug_id>', methods=['PUT'])
def api_update_bug(bug_id):
    bug_update = request.json
    try:
        bug_id = update_bug(
            bug_id=bug_id,
            title = bug_update['title'],
            description= bug_update.get('description',''),
            status= bug_update.get('status','Open'),
            severity= bug_update.get('severity','Medium'),
            solution= bug_update.get('solution','')
        )

        return jsonify({'status': 'success update', 'bug_id': bug_id})

    except Exception as e:
        print(f"Unexpected Error occured: {e}")

@app.route('/api/bugs/<int:bug_id>', methods=['DELETE'])
def api_delete_bug(bug_id):
    try:
        pass
        delete_bug(
            bug_id=bug_id
        )
    except Exception as e:
        print(f"Unexpected Error occured: {e}")


    
if __name__ == '__main__':
    init_db()
    app.run(debug=True)