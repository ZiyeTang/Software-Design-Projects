import requests
import xmltodict
from xml.parsers.expat import ExpatError
import pprint
from pymongo import MongoClient

def get_section_info(res, subject_id, course_id, section_retrievals_failed, subjects_failed, section):
    try:
        section_info = xmltodict.parse(requests.get(section['@href']).content)
    except ExpatError:
        section_retrievals_failed += 1
    except KeyboardInterrupt:
        pprint.pprint(res)
        exit(1)
    except requests.exceptions.ConnectionError:
        if subject_id not in subjects_failed:
            subjects_failed.append(subject_id)
        print(subject_id, ": ", course_id)
    else:
        if '@id' in section_info['ns2:section']:
            section_id = section_info['ns2:section']['@id']
            res['courses'][course_id]['sections'][section_id] = {}

            if 'sectionNumber' in section_info['ns2:section']:
                res['courses'][course_id]['sections'][section_id]['sectionNumber'] = section_info['ns2:section']['sectionNumber']
            if 'startDate' in section_info['ns2:section']:
                res['courses'][course_id]['sections'][section_id]['startDate'] = section_info['ns2:section']['startDate']
            if 'endDate' in section_info['ns2:section']:
                res['courses'][course_id]['sections'][section_id]['endDate'] = section_info['ns2:section']['endDate']
            if 'meetings' in section_info['ns2:section']:
                res['courses'][course_id]['sections'][section_id]['meetings'] = section_info['ns2:section']['meetings']

def getSubjects(year='2023', semester="fall"):
    CONNECTION_STRING = "mongodb+srv://group49:1234@cs222.xsrjnch.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(CONNECTION_STRING)
    db = client.db
    collection = db.courses2

    url = 'https://courses.illinois.edu/cisapp/explorer/schedule/' + year + '/'+ semester + '.xml'
    response = requests.get(url)
    subjects = xmltodict.parse(response.content)

    
    section_retrievals_failed = 0
    course_retrievals_failed = 0
    subjects_failed = []
    for subject in subjects['ns2:term']['subjects']['subject']:
        subject_id = subject['@id']
        res = {}
        res["subject_code"] = subject_id
        res["subject"] = subject['#text']
        res["courses"] = {}

        # if subject_id != "AAS":
        #     continue
        print(subject)
        subject_response = xmltodict.parse(requests.get(subject['@href']).content)

        for course in subject_response['ns2:subject']['courses']['course']:
            try:
                course_info = xmltodict.parse(requests.get(course['@href']).content)
            except ExpatError:
                # print("Failed to retrieve course information")
                print(course)
                course_retrievals_failed += 1
            except KeyboardInterrupt:
                pprint.pprint(res)
                exit(1)
            except TypeError:
                # Basque (1 course in the subject)
                print("Manually add Basque")
            else:
                course_id = course['@id']
                # print(course_id)
                res['courses'][course_id] = {}
                res['courses'][course_id]['sections'] = {}
                res['courses'][course_id]['title'] = course['#text']
                #pprint.pprint(course_info)

                # If there is more than 1 section (list of dicts)
                if type(course_info['ns2:course']['sections']['section']) == list:
                    for section in course_info['ns2:course']['sections']['section']:
                        if type(section) == dict:
                            get_section_info(res, subject_id, course_id, section_retrievals_failed, subjects_failed, section)
                # If there is only 1 section
                elif type(course_info['ns2:course']['sections']['section']) == dict:
                    section = course_info['ns2:course']['sections']['section']
                    get_section_info(res, subject_id, course_id, section_retrievals_failed, subjects_failed, section)

        collection.insert_one(res)           
    return course_retrievals_failed, section_retrievals_failed, subjects_failed


course_retrievals_failed, section_retrievals_failed, subjects_failed = getSubjects()
# pprint.pprint(res)
print(course_retrievals_failed)
print(section_retrievals_failed)
print(subjects_failed)
# CONNECTION_STRING = "mongodb+srv://group49:1234@cs222.xsrjnch.mongodb.net/?retryWrites=true&w=majority"
# client = MongoClient(CONNECTION_STRING)
# db = client.db
# collection = db.courses

# for x, y in res.items():
#     collection.insert_one({x: y})

# collection.insert_one(res)
# collection.delete_many({})

# url = 'https://courses.illinois.edu/cisapp/explorer/schedule/2023/fall/CS/225/35917.xml'
# response = requests.get(url)
# data = response.content
# print(data)
# pprint.pprint(data)
