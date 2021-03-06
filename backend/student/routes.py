from flask import Blueprint, request, session
from backend.extensions import mongo_students
import datetime
import json

student = Blueprint('student', __name__, url_prefix='/student')

@student.route('/add_attendance_section')
def add_attendance_section():
    student_collection = mongo_students.db.BTECH_COMPS_2018_2022
    dates = {
        'Monday':["2022-04-18", "2022-04-25", "2022-05-02", "2022-05-09", "2022-05-16", "2022-05-23"],
        'Tuesday':["2022-04-19", "2022-04-26", "2022-05-03", "2022-05-10", "2022-05-17", "2022-05-24"],
        'Wednesday':["2022-04-20", "2022-04-27", "2022-05-04", "2022-05-11", "2022-05-18", "2022-05-25"],
        'Tursday':["2022-04-21", "2022-04-28", "2022-05-05", "2022-05-12", "2022-05-19", "2022-05-26"],
        'Friday':["2022-04-22", "2022-04-29", "2022-05-06", "2022-05-13", "2022-05-20", "2022-05-27"],
    }

    students_info = []
    for doc in student_collection.find():
        students_info.append(doc)
    
    for student in students_info:
        for day in student['Timetable'].keys():
            i = -1
            for lecture in student['Timetable'][day]:
                i = i + 1
                if 'attendance' not in lecture.keys():
                    query = "Timetable" + "." + day + "." + str(i) + "." + "Attendance"
                    attendance = []
                    for date in dates[day]:
                        attendance.append({"Date":date, "isPresent":False})
                    student_schedule = student_collection.update_one({"College ID":student['College ID']},{"$set":{query:attendance}})
    return "hi"



@student.route('/<int:college_id>/student_dashboard')
def student_dashboard(college_id):
    student_collection = mongo_students.db.BTECH_COMPS_2018_2022
    students_info = {}
    for doc in student_collection.find({"College ID": college_id}):
        students_info = doc
    
    student_lectures = []
    for keys in students_info['Timetable'].keys():
        for lecture in students_info['Timetable'][keys]:
            for attendance in lecture['Attendance']:
                mini_lecture = {}
                mini_lecture['teacher'] = lecture['teacher']
                mini_lecture['subject'] = lecture['subject']
                mini_lecture['startTime'] = lecture['startTime']
                mini_lecture['endTime'] = lecture['endTime']
                mini_lecture['classroom'] = lecture['classroom']
                mini_lecture['Date'] = attendance['Date']
                mini_lecture['isPresent'] = attendance['isPresent']
                student_lectures.append(mini_lecture)

    student_lectures = sorted(student_lectures, key = lambda i: (i['Date'], i['startTime']))
    print(student_lectures)
    return json.dumps(student_lectures)


@student.route('/<int:college_id>/attendance', methods=['GET'])
def charts(college_id):
    student_collection = mongo_students.db.BTECH_COMPS_2018_2022
    students_info = {}
    for doc in student_collection.find({"College ID": college_id}):
        students_info = doc

    single_lectures = []
    for keys in students_info['Timetable'].keys():
        for lecture in students_info['Timetable'][keys]:
            for attendance in lecture['Attendance']:
                mini_lecture = {}
                mini_lecture['subject'] = lecture['subject']
                mini_lecture['Date'] = attendance['Date']
                mini_lecture['isPresent'] = 1 if attendance['isPresent'] else 0
                single_lectures.append(mini_lecture)

    single_lectures_dict = {}
    for lecture in single_lectures:
        if lecture['subject'] not in single_lectures_dict.keys():
            single_lectures_dict[lecture['subject']] = []
        single_lectures_dict[lecture['subject']].append(lecture)

    for keys in single_lectures_dict.keys():
        single_lectures_dict[keys] = sorted(single_lectures_dict[keys], key=lambda x: x['Date'])

    monthly_lectures = {}
    for lecture in single_lectures:
        key = lecture['subject'] + datetime.datetime.strptime(lecture['Date'], "%Y-%m-%d").date().strftime("%B")
        if key not in monthly_lectures.keys():
            monthly_lectures[key] = {}
            monthly_lectures[key]['Month'] = datetime.datetime.strptime(lecture['Date'], "%Y-%m-%d").date().strftime("%B")
            monthly_lectures[key]['Subject'] = lecture['subject']
            monthly_lectures[key]['Presentees'] = 1 if lecture['isPresent'] == 1 else 0
            monthly_lectures[key]['Absentees'] = 1 if lecture['isPresent'] == 0 else 0
        else:
            if lecture['isPresent'] == 1:
                monthly_lectures[key]['Presentees'] += 1
            else:
                monthly_lectures[key]['Absentees'] += 1

    monthly_lectures_dict = {}
    for key in monthly_lectures.keys():
        if monthly_lectures[key]['Subject'] not in monthly_lectures_dict.keys():
            monthly_lectures_dict[monthly_lectures[key]['Subject']] = []
        monthly_lectures_dict[monthly_lectures[key]['Subject']].append(monthly_lectures[key])
    
    return json.dumps({"monthly_lectures":monthly_lectures_dict, "single_lectures": single_lectures_dict})