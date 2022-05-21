from flask import ( Blueprint , request )
from backend.extensions import mongo_students, mongo_teachers
import datetime
from backend.auth.routes import teacher_required
import json

teach = Blueprint('teach', __name__, url_prefix='/teach')

def add_attendance_section(teacher_info):
    teacher_collection = mongo_teachers.db.TEACHERS
    dates = {
        'Monday':["2022-04-18", "2022-04-25", "2022-05-02", "2022-05-09", "2022-05-16", "2022-05-23"],
        'Tuesday':["2022-04-19", "2022-04-26", "2022-05-03", "2022-05-10", "2022-05-17", "2022-05-24"],
        'Wednesday':["2022-04-20", "2022-04-27", "2022-05-04", "2022-05-11", "2022-05-18", "2022-05-25"],
        'Tursday':["2022-04-21", "2022-04-28", "2022-05-05", "2022-05-12", "2022-05-19", "2022-05-26"],
        'Friday':["2022-04-22", "2022-04-29", "2022-05-06", "2022-05-13", "2022-05-20", "2022-05-27"],
    }

    for day in teacher_info['Timetable'].keys():
        for lecture_index in range(len(teacher_info['Timetable'][day])):
            if 'Attendance' not in teacher_info['Timetable'][day][lecture_index].keys():
                teacher_info['Timetable'][day][lecture_index]['Attendance'] = []
                student_collection = mongo_students.db[teacher_info['Timetable'][day][lecture_index]['batch']]
                students_info = []
                for doc in student_collection.find():
                    student_info = {
                                    "studentID": doc["College ID"],
                                    "studentName": doc["Student Name"],
                                    "isPresent" : False,                                    
                                    }
                    students_info.append(student_info)
                
                attendance = []
                for date in dates[day]:
                    attendance.append({"Date": date, "Student_List": students_info})
                query_key = "Timetable." + day + "." + str(lecture_index) + "." + "Attendance"
                teacher_schedule = teacher_collection.update_one({"College ID":teacher_info['College ID'],},{"$set":{query_key:attendance}})

@teach.route('/<int:college_id>/lectures', methods=['GET'])
@teacher_required
def lectures(college_id):
    teacher_collection = mongo_teachers.db.TEACHERS
    teacher_info = {}
    for doc in teacher_collection.find({"College ID": college_id}):
        teacher_info = doc
    # add_attendance_section(teacher_info)
    lectures = []
    for day in teacher_info['Timetable'].keys():
        for class_lectures in teacher_info['Timetable'][day]:
            for class_lecture in class_lectures['Attendance']:
                if datetime.datetime.strptime(class_lecture['Date'], "%Y-%m-%d").date() <= datetime.date.today():
                    class_lecture['batch'] = class_lectures['batch']
                    class_lecture['subject'] = class_lectures['subject']
                    class_lecture['classroom'] = class_lectures['classroom']
                    class_lecture['startTime'] = class_lectures['startTime']
                    class_lecture['endTime'] = class_lectures['endTime']
                    lectures.append(class_lecture)

    lectures = sorted(lectures, key = lambda i: (i['Date'], i['startTime']))
    return json.dumps(lectures)
    # return render_template('teacher/index.html', lectures=lectures)

def student_attendance_stud(batch, date, startTime, student_attendance):
    student_collection = mongo_students.db[batch]
    students_info = []
    for doc in student_collection.find():
        students_info.append(doc)

    for student_info in students_info:
        for day in student_info['Timetable'].keys():
            for lecture in range(len(student_info['Timetable'][day])):
                if student_info['Timetable'][day][lecture]['startTime'] == startTime:
                    for attendance in range(len(student_info['Timetable'][day][lecture]["Attendance"])):
                        if student_info['Timetable'][day][lecture]["Attendance"][attendance]['Date'] == date:
                            for student in student_attendance:
                                if student_info['College ID'] == student['studentID']:
                                    query_key = "Timetable." + day + "." + str(lecture) + "." + "Attendance" + "." + str(attendance) + "." + "isPresent"
                                    updated_student = student_collection.update_one({"College ID":student_info['College ID']},{"$set":{query_key:student['isPresent']}})
                            

    
@teach.route('/<int:college_id>/lectures/<batch>/<date>/<startTime>', methods=['GET','POST'])
# @teacher_required
def student_attendance(college_id, batch, date, startTime):
    if request.method == 'POST':
        # return request.form
        student_attendance = request.json
        if student_attendance is None: 
            return {"error" : "Empty list bruh"}
        
        print(student_attendance)
        student_attendance_stud(batch, date, startTime, student_attendance)
        teacher_collection = mongo_teachers.db.TEACHERS
        teacher_info = {}
        for doc in teacher_collection.find({"College ID": college_id}):
            teacher_info = doc
        for day in teacher_info['Timetable'].keys():
            i=-1
            for class_lectures in teacher_info['Timetable'][day]:
                i=i+1
                if class_lectures['batch'] == batch and class_lectures['startTime'] == startTime:
                    j=-1
                    for class_lecture in class_lectures['Attendance']:
                        j=j+1
                        if class_lecture['Date'] == date:
                            query_key = "Timetable." + day + "." + str(i) + "." + "Attendance" + "." + str(j) + "." + "Student_List"
                            teacher_schedule = teacher_collection.update_one({"College ID":teacher_info['College ID'],},{"$set":{query_key:student_attendance}})
                            return json.dumps({"success": "Student Attendance Updated Successfully"}), 200
    
    if request.method == 'GET':
        teacher_collection = mongo_teachers.db.TEACHERS
        teacher_info = {}
        for doc in teacher_collection.find({"College ID": college_id}):
            teacher_info = doc
        # add_attendance_section(teacher_info)
        student_attendance = {}
        for day in teacher_info['Timetable'].keys():
            for class_lectures in teacher_info['Timetable'][day]:
                for class_lecture in class_lectures['Attendance']:
                    if class_lectures['batch'] == batch and class_lectures['startTime'] == startTime and class_lecture['Date'] == date:
                        student_attendance = class_lecture['Student_List']
        student_attendance = sorted(student_attendance, key=lambda i: i['studentID'])
        return json.dumps(student_attendance)


@teach.route('/<int:college_id>/attendance', methods=['GET'])
def charts(college_id):
    teacher_info = {}
    teacher_collection = mongo_teachers.db.TEACHERS
    for doc in teacher_collection.find({"College ID": college_id}):
        teacher_info = doc

    # Lecture wise attendance : pie chart
    single_lectures = []
    for day in teacher_info['Timetable'].keys():
        for class_lectures in teacher_info['Timetable'][day]:
            for class_lecture in class_lectures['Attendance']:
                if datetime.datetime.strptime(class_lecture['Date'], "%Y-%m-%d").date() <= datetime.date.today():
                    lecture = {}
                    lecture['Date'] = class_lecture['Date']
                    lecture['Subject'] = class_lectures['subject']
                    lecture['Batch'] = class_lectures['batch']
                    presentees = 0
                    absentees = 0
                    for students in class_lecture['Student_List']:
                        if students['isPresent'] == True:
                            presentees += 1
                        else:
                            absentees += 1
                    lecture["isPresent"] = presentees
                    lecture['isAbsent'] = absentees
                    single_lectures.append(lecture)
    print(single_lectures)
    
    # Weekly-Lecture wise attendance : bar chart - subject vs weekdays & pie chart : total presentees vs total absentees for that subject on that week
    bar_chart_data = {}
    for day in teacher_info['Timetable'].keys():
        for class_lectures in teacher_info['Timetable'][day]:
            for class_lecture in class_lectures['Attendance']:
                if datetime.datetime.strptime(class_lecture['Date'], "%Y-%m-%d").date() <= datetime.date.today():
                    day_of_month = datetime.datetime.strptime(class_lecture['Date'], "%Y-%m-%d").date().day
                    week_number = (day_of_month - 1) // 7 + 1
                    # key = 

    # Monthly-Lecture wise attendance
    monthly_lectures = {}
    for day in teacher_info['Timetable'].keys():
        for class_lectures in teacher_info['Timetable'][day]:
            for class_lecture in class_lectures['Attendance']:
                if datetime.datetime.strptime(class_lecture['Date'], "%Y-%m-%d").date() <= datetime.date.today():
                    key = class_lectures['subject'] + "_" + class_lectures['batch'] + "_" + datetime.datetime.strptime(class_lecture['Date'], "%Y-%m-%d").date().strftime("%B")
                    if key not in monthly_lectures.keys():
                        monthly_lectures[key] = {}
                        monthly_lectures[key]['Month'] = datetime.datetime.strptime(class_lecture['Date'], "%Y-%m-%d").date().strftime("%B")
                        monthly_lectures[key]['Subject'] = class_lectures['subject']
                        monthly_lectures[key]['Batch'] = class_lectures['batch']
                        presentees = 0
                        absentees = 0
                        for students in class_lecture['Student_List']:
                            if students['isPresent'] == True:
                                presentees += 1
                            else:
                                absentees += 1
                        monthly_lectures[key]["isPresent"] = presentees
                        monthly_lectures[key]['isAbsent'] = absentees
                    else:
                        presentees = 0
                        absentees = 0
                        for students in class_lecture['Student_List']:
                            if students['isPresent'] == True:
                                presentees += 1
                            else:
                                absentees += 1
                        monthly_lectures[key]["isPresent"] += presentees
                        monthly_lectures[key]['isAbsent'] += absentees

    print(monthly_lectures)

    return json.dumps({"monthly_lectures":monthly_lectures, "single_lectures": single_lectures})