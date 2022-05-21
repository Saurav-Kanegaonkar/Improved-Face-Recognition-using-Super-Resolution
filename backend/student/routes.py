from flask import Blueprint, request, session
from backend.extensions import mongo_students
import datetime

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