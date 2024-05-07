from flask import Flask, render_template, abort, Response, jsonify
from flask_cors import CORS
from flask import request
from pymongo import MongoClient
import json
import uuid

import requests
import xmltodict

app = Flask(__name__)
CORS(app)

CONNECTION_STRING = "mongodb+srv://group49:1234@cs222.xsrjnch.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
db = client.db
collection = db.courses2
user_col = db.users

# Index API route to check if backend is running, will display HTML from templates/index.html
@app.route("/")
def index():
    print("Index page request")
    return render_template("index.html")

# Test API route to check if backend route displays to frontend
# Returns a JSON array of strings
@app.route("/test")
def test():
    return {"test": ["This", "is", "our", "Flask", "test", "route"]}

def convert_time_to_minutes(str):
    time = str.split()
    try:
        hour, minute = time[0].split(":")
    except:
        return "Bad format"
    else:
        try:
            hour = int(hour)
            minute = int(minute)
        except:
            return "Bad format"
        else:
            if hour == 12:
                hour = 0

            if len(time) == 1:
                return hour*60+minute

            if time[1].upper() == 'AM':
                return hour*60+minute
        
            return (hour+12)*60+minute


def filter(course, day, location, start, end, instructor, time):
    res = {'sections':{}, 'title': course['title']}
    for crn in course['sections']:
        mts = course['sections'][crn]["meetings"]["meeting"]

        if type(mts) != list:
            mts = [mts]

        for mt in mts:
            match_day = True
            match_loc = True
            match_start = True
            match_end = True
            match_intructor = True
            match_time = True
            if day:
                for d in day.upper():
                    if 'daysOfTheWeek' not in mt or d not in mt['daysOfTheWeek'].upper():
                        match_day = False
                        break
                    
            if location:
                if 'buildingName' not in mt or location.upper() not in mt['buildingName'].upper():
                    match_loc = False

            cur_start = -1
            cur_end = -1

            if 'start' in mt and mt['start']!="ARRANGED":
                cur_start = convert_time_to_minutes(mt['start'])
                
            if 'end' in mt and mt['end']!="ARRANGED":
                cur_end = convert_time_to_minutes(mt['end'])
                
            if start:
                if cur_start == -1 or convert_time_to_minutes(start) != cur_start:
                    match_start = False
                
            if end:
                if cur_end == -1 or convert_time_to_minutes(end) != cur_end:
                    match_end = False

            if time:
                if convert_time_to_minutes(time) == "Bad format":
                    return jsonify({ "error": "Time format should be <hr:min AM/PM>"}), 400
                else:
                    cur_time = convert_time_to_minutes(time)

                if cur_time < cur_start or cur_time > cur_end:
                    match_time = False

            if instructor:
                if 'instructors' not in mt or mt['instructors'] == None or'instructor' not in mt['instructors']:
                    match_intructor = False
                else:
                    cur_instructors = mt['instructors']['instructor']
                    if type(cur_instructors) == dict:
                        cur_instructors  = [cur_instructors ]
                        
                    match_intructor = False
                    for i in cur_instructors:
                        if instructor.upper() in i['#text'].upper():
                            match_intructor = True
                            break


            if match_day and match_loc and match_start and match_end and match_intructor and match_time:
                res['sections'][crn] = course['sections'][crn]
                break

    if res['sections'] == {}:
        res = {}
    return res


def add_course_to_schedule(subject, course_number, crn, user_id):
    user = user_col.find_one({ "_id": user_id })
    subject = subject.upper()
    subject_information = collection.find_one( {'subject_code': subject} )
    if subject_information is None:
        abort(404)

    courses = subject_information['courses']
    if course_number not in courses:
        abort(404)

    course = courses[course_number]
    if crn not in course['sections']:
        abort(404)
    
    section = course['sections'][crn]
    
    if subject not in user['courses']:
        user['courses'][subject]={}
    
    if course_number not in user['courses'][subject]:
        user['courses'][subject][course_number]={}
    
    user['courses'][subject][course_number][crn]=section
    user_col.update_one({'_id':user_id}, {"$set":{'courses':user['courses']}})
     

def delete_course_from_schedule(subject, course_number, crn, user_id):
    user = user_col.find_one({ "_id": user_id })
    subject = subject.upper()
    if subject not in user['courses'] or course_number not in user['courses'][subject] or crn not in user['courses'][subject][course_number]:
        abort(404)
    
    del user['courses'][subject][course_number][crn]
    if user['courses'][subject][course_number]=={}:
        del user['courses'][subject][course_number]
        if user['courses'][subject] == {}:
            del user['courses'][subject]

    user_col.update_one({'_id':user_id}, {"$set":{'courses':user['courses']}})
    

# Endpoint to return all information of courses given a subject
@app.route("/courses")
def courses():
    subject = request.args.get('subject')
    if subject is None:
        abort(400)

    subject_information = collection.find_one( {'subject_code': subject.upper()} )
    if subject_information is None:
        abort(404)

    courses = subject_information['courses']

    day = request.args.get('day')
    location = request.args.get('location')
    start = request.args.get('start')
    end = request.args.get('end')
    instructor = request.args.get('instructor')
    time = request.args.get('time')
    

    if not day and not location and not start and not end and not instructor and not time:
        courses_json = json.dumps(courses, indent=4)
        response = Response(courses_json, content_type="application/json")
        return response
    
    res = {}
    for course_code in courses:
        res[course_code] = filter(courses[course_code], day, location, start, end, instructor, time)
        if res[course_code] == {}:
            del res[course_code]
    courses_json = json.dumps(res, indent=4)
    response = Response(courses_json, content_type="application/json")
    return response


# Endpoint to return information of a select course given a subject and course
@app.route("/course")
def course():
    subject = request.args.get('subject')
    course_number = request.args.get('number')
    if subject is None or course_number is None:
        abort(400)
    
    subject_information = collection.find_one( {'subject_code': subject.upper()} )
    if subject_information is None:
        abort(404)

    courses = subject_information['courses']
    if course_number not in courses:
        abort(404)

    course = courses[course_number]

    day = request.args.get('day')
    location = request.args.get('location')
    start = request.args.get('start')
    end = request.args.get('end')
    instructor = request.args.get('instructor')
    time = request.args.get('time')

    if not day and not location and not start and not end and not instructor and not time:
        course_json = json.dumps(course, indent=4)
        response = Response(course_json, content_type="application/json")
        return response
    
    res = filter(course, day, location, start, end, instructor, time)

    courses_json = json.dumps(res, indent=4)
    response = Response(courses_json, content_type="application/json")
    return response


# Endpoint to return information of a section given subject, course, and CRN
@app.route("/section")
def section():
    subject = request.args.get('subject')
    course_number = request.args.get('number')
    crn = request.args.get('crn')
    if subject is None or course_number is None or crn is None:
        abort(400)
    
    subject_information = collection.find_one( {'subject_code': subject.upper()} )
    if subject_information is None:
        abort(404)

    courses = subject_information['courses']
    if course_number not in courses:
        abort(404)

    course = courses[course_number]
    if crn not in course['sections']:
        abort(404)
    section = course['sections'][crn]

    section_json = json.dumps(section, indent=4)
    response = Response(section_json, content_type="application/json")

    return response


@app.route('/users', methods=['POST', 'GET'])
def user_create():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if email is None or password is None:
            return jsonify({ "error": "Missing email or password" }), 400

        user = {
            "_id": uuid.uuid4().hex,
            "email": email,
            "password": password,
            "courses": {}
        }

        if user_col.find_one({ "email": user['email'] }):
            return jsonify({ "error": "Email address is already in use"}), 400
        
        if user_col.insert_one(user):
            return jsonify(user), 200

        return jsonify({ "error": "Failed to create new user"}), 400
    
    elif request.method == 'GET':
        email = request.args.get('email')
        password = request.args.get('password')

        if email is None:
            return jsonify({ "error": "Missing email" }), 400
        if password is None:
            return jsonify({ "error": "Missing password" }), 400

        user = user_col.find_one({ "email": email, "password": password })

        if user:
            return jsonify(user), 200
        else:
            return jsonify({ "error": "User not found" }), 404

    else:
        abort(405)

@app.route('/users/<user_id>', methods=['GET', 'PATCH', 'DELETE'])
def user(user_id):
    if request.method == 'GET':
        user = user_col.find_one({ "_id": user_id })

        if user is None:
            return jsonify({ "error": "User id was not found"}), 404
        
        return jsonify(user), 200
    elif request.method == 'PATCH':
        user = user_col.find_one({ "_id": user_id })

        if user is None:
            return jsonify({ "error": "User id was not found" }), 404
        
        old_email = user['email']
        old_password = user['password']
        old_courses = user['courses']
        
        data = request.get_json()
        input_email = data.get('email')
        input_password = data.get('password')
        input_courses = data.get('courses')
        
        if input_email is None:
            input_email = old_email
        if input_password is None:
            input_password = old_password
        if input_courses is None:
            input_courses = old_courses

        # if new email, check if there exists a user with that email
        if input_email != old_email and user_col.find_one({ "email": input_email }):
            return jsonify({ "error": "Email address is already in use"}), 400
        
        if user_col.update_one({'_id': user_id}, {"$set":{'email': input_email, 'password': input_password, 'courses': input_courses}}):
            return jsonify({ "completed": "Successfully patched new user information"}), 200

        return jsonify({ "error": "Failed to create new user"}), 400
        
    elif request.method == 'DELETE':
        user = user_col.find_one({ "_id": user_id })

        if user is None:
            return jsonify({ "error": "User id was not found"}), 404
        
        user_col.delete_one({ "_id": user_id})
        return jsonify({ "completed": "User was successfully deleted"}), 200
    else:
        abort(405)


@app.route('/users/<user_id>/schedule', methods=['GET', 'POST', 'DELETE'])
def user_schedule(user_id):    
    user = user_col.find_one({ "_id": user_id })
    if user is None:
        return jsonify({ "error": "User id was not found"}), 404

    if request.method == 'GET': 
        return jsonify(user['courses']), 200
        
    else:
        data = request.get_json()
        subject = data.get('subject').upper()
        course_number = data.get('number')
        crn = data.get('crn')
        if subject is None or course_number is None or crn is None:
            return jsonify({ "error": "Missing subject or course number or CRN" }), 400
        
        if request.method == 'POST':
            add_course_to_schedule(subject, course_number, crn, user_id)
            return jsonify({ "completed": "section was successfully added"}), 200   
        
        elif request.method == 'DELETE':
            delete_course_from_schedule(subject, course_number, crn, user_id)
            return jsonify({ "completed": "section was successfully deleted"}), 200
        
        else:
            abort(405)

if __name__ == "__main__":
    app.run(port = 8080)