import pytest
from pymongo import MongoClient
import sys

sys.path.append('../')
from app import filter

CONNECTION_STRING = "mongodb+srv://group49:1234@cs222.xsrjnch.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client.db
collection = db.courses2


test_data = [ 
        ("JAPN", None, None, None, "10:00", None, None, None, {"31767", "49687"}),
        ("japn", None, None, "Gregory", "9:00 am", None, None, None, {"45827"}),
        ("Japn", None, None, "Literatures", "9:00", None, None, None, {"31757", "30461", "42882"}),
        ("JAPN", None, "mw", None, None, None, "hirata", None, {"45827", "31767", "31763", "31766"}),
        ("japn", None, None, "gregory", None, None, "Nozaki", None, set()),
        ("turk", None, "mw", None, None, "9:50", None, None, {"47985"}),
        ("CS", None, "TR", "campus", None,  None, "Ringer", "12:45 PM", {"65907", "65906"}),
        ("cs", None, None, None, None, None, "Gunter", "2:11 PM", {"40087", "30128"}),
        ("stat", None, None, "natural", None, None, None, "10:15", {"51802"}),
        ("stat", None, None, "natural", None, None, None, "11:00", set()),
        ("phys", "101", None, None, None, "11:50", None, None, {"43197", "34835", "34854"}),
        ("Phys", "101", "w", None, "10:00", None, None, None, {"34835"}),
        ("PHYS", "101", None, "Noyes", None, None, "mueller", None, {"34850"}),
        ("phys", "101", "M", None, None, None, "Gulian", None, set()),
        ("phys", "101", "R", None, None, None, "gulian", None, {"34854"})
    ]


def get_all_crn(res):
    if 'sections' in res:
        return set(list(res['sections'].keys()))
    
    l = []
    for num in res:
        l+=list(res[num]['sections'])
    return set(l)


@pytest.mark.parametrize(
    "subject, number, day, location, start, end, instructor, time, answer",
    test_data
)
def test_filter(subject, number, day, location, start, end, instructor, time, answer):
    subject_information = collection.find_one( {'subject_code': subject.upper()} )
    assert subject_information is not None
        
    query = subject_information['courses']
    if number:
        assert number in query
        query = {number:query[number]}

    res = {}
    for course_code in query:
        res[course_code] = filter(query[course_code], day, location, start, end, instructor, time)
        if res[course_code] == {}:
            del res[course_code]
    assert get_all_crn(res) == answer

