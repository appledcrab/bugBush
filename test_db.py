# test_database.py
import sqlite3
import pytest
from database import init_db, add_bug, get_all_bugs, get_bug, delete_all_bugs

@pytest.fixture
def setup_db():
    """Fixture to initialize and clean up the database"""
    init_db()
    yield  # this is where the test runs
    # Clean up after tests that deletes all the bugs added here
    delete_all_bugs()

def test_add_and_get_bug(setup_db):
    # Test adding a bug
    bug_id = add_bug(
        title="Test Bug",
        description="This is a test bug",
        status="Open",
        severity="Low"
    )
    
    # Verify we got an ID back
    assert isinstance(bug_id, int)
    assert bug_id > 0
    
    # Test retrieving the bug
    bugs = get_all_bugs()
    assert len(bugs) == 1
    assert bugs[0]['title'] == "Test Bug"
    assert bugs[0]['description'] == "This is a test bug"
    assert bugs[0]['status'] == "Open"
    assert bugs[0]['severity'] == "Low"
    
    # Test get_bug
    single_bug = get_bug(bug_id)
    assert single_bug is not None
    assert single_bug['id'] == bug_id

def test_get_nonexistent_bug(setup_db):
    # Test getting a bug that doesnt exist
    assert get_bug(999) is None

def test_get_all_bugs_empty(setup_db):
    # Test getting bugs when none exist
    assert get_all_bugs() is None

def test_add_multiple_bugs(setup_db):
    # Adding  multiple bugs
    add_bug("Bug 1", "First bug")
    add_bug("Bug 2", "Second bug")
    add_bug("Bug 3", "Third bug")
    
    bugs = get_all_bugs()
    assert len(bugs) == 3
    assert {bug['title'] for bug in bugs} == {"Bug 1", "Bug 2", "Bug 3"}