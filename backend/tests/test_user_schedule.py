import pytest
from pymongo import MongoClient
import sys


sys.path.append('../')
from app import add_course_to_schedule
from app import delete_course_from_schedule

CONNECTION_STRING = "mongodb+srv://group49:1234@cs222.xsrjnch.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client.db
collection = db.courses2
user_col = db.users

test_data = [
    ("cs", "225", "65054", "607a3e07d33e4e10bdab1c16c624bd45"),
    ("cs", "225", "61264", "607a3e07d33e4e10bdab1c16c624bd45"),
    ("CS", "341", "76768", "607a3e07d33e4e10bdab1c16c624bd45"),
    ("Math", "441", "32116", "607a3e07d33e4e10bdab1c16c624bd45"),
    ("math", "441", "32118", "607a3e07d33e4e10bdab1c16c624bd45"),
    ("math", "241", "47037", "607a3e07d33e4e10bdab1c16c624bd45"),
]

@pytest.mark.parametrize(
    "subject, number, crn, user_id",
    test_data
)
def test_schedule_add(subject, number, crn, user_id):
    subject = subject.upper()
    add_course_to_schedule(subject, number, crn, user_id)
    user = user_col.find_one({ "_id": user_id })
    assert subject in user['courses'] and number in user['courses'][subject] and crn in user['courses'][subject][number]
    assert user['courses'][subject][number][crn] != {}

@pytest.mark.parametrize(
    "subject, number, crn, user_id",
    test_data
)
def test_schedule_delete(subject, number, crn, user_id):
    subject = subject.upper()
    delete_course_from_schedule(subject, number, crn, user_id)
    user = user_col.find_one({ "_id": user_id })
    pass_case1 = subject not in user['courses']
    pass_case2 = subject in user['courses'] and number not in user['courses'][subject]
    pass_case3 = subject in user['courses'] and number in user['courses'][subject] and crn not in user['courses'][subject][number]
    assert pass_case1 or pass_case2 or pass_case3