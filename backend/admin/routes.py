from flask import Blueprint, request, session
from backend.extensions import mongo_students, mongo_teachers, mongo_classroom

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/register', methods=['POST'])
def register():
    # if session['user_role'] == 'Admin':
    name = request.json['name']
    college_id = request.json['college_id']
    email = request.json['email']
    role = request.json['role']

    if role == 'Teacher':
        teacher_collection = mongo_teachers.db.TEACHERS
        teacher_info = {}
        for doc in teacher_collection.find({"College ID": college_id}):
            teacher_info = doc
        if bool(teacher_info):
            return {"error": "Teacher already exist"}, 401
        
        new_teacher = teacher_collection.insert_one({"College ID":college_id, "Role": role, "Teacher Name": name, "Email ID": email})
        
        for doc in teacher_collection.find({"College ID": college_id}):
            teacher_info = doc
        return str(teacher_info)
        
    elif role == 'Student':
        student_collection = mongo_students.db.BTECH_COMPS_2018_2022
        student_info = {}
        for doc in student_collection.find({"College ID": college_id}):
            student_info = doc
        if bool(student_info):
            return {"error": "Student already exist"}, 401
        
        new_student = student_collection.insert_one({"College ID":college_id, "Role": role, "Student Name": name, "Email ID": email})
        
        for doc in student_collection.find({"College ID": college_id}):
            student_info = doc
        return str(student_info)
    
    else:
        # admin_collection = mongo_admins.db.ADMINS
        # admin = admin_collection.find({"id": id})
        pass
    return {"error": "Invalid Credentials"}, 401

def assign_batch_schedule(classroom_schedule):
    batch_dict = {}
    for schedule in classroom_schedule['timetable']:
        if schedule['batch'] not in batch_dict.keys():
            batch_dict[schedule['batch']] = {}
            if classroom_schedule['day'] not in batch_dict[schedule['batch']].keys():
                batch_dict[schedule['batch']][classroom_schedule['day']] = []
        batch_dict[schedule['batch']][classroom_schedule['day']].append({
                                                                    "teacher": schedule['teacher_name'], 
                                                                    "subject": schedule['subject'], 
                                                                    "startTime": schedule['startTime'], 
                                                                    "endTime": schedule['endTime'],
                                                                    "classroom" : classroom_schedule['classroom']
                                                                    })

    for batch in batch_dict.keys():
        batch_collection = mongo_students.db[batch]
        students_info = []
        for doc in batch_collection.find():
            students_info.append(doc)

        for student in students_info:
            timetable = {}
            if 'Timetable' in student.keys():
                timetable = student['Timetable']
                timetable[classroom_schedule['day']].extend(batch_dict[batch][classroom_schedule['day']])
            else:
                timetable[classroom_schedule['day']] = batch_dict[batch][classroom_schedule['day']]

            student_schedule = batch_collection.update_one({"College ID":student['College ID']},{"$set":{"Timetable":timetable}})
    return timetable


def update_batch_schedule(classroom_schedule):
    batch_dict = {}
    for schedule in classroom_schedule['timetable']:
        if schedule['batch'] not in batch_dict.keys():
            batch_dict[schedule['batch']] = {}
            if classroom_schedule['day'] not in batch_dict[schedule['batch']].keys():
                batch_dict[schedule['batch']][classroom_schedule['day']] = []
        batch_dict[schedule['batch']][classroom_schedule['day']].append({
                                                                    "teacher": schedule['teacher_name'], 
                                                                    "subject": schedule['subject'], 
                                                                    "startTime": schedule['startTime'], 
                                                                    "endTime": schedule['endTime'],
                                                                    "classroom" : classroom_schedule['classroom']
                                                                    })

    for batch in batch_dict.keys():
        batch_collection = mongo_students.db[batch]
        students_info = []
        for doc in batch_collection.find():
            students_info.append(doc)
     
        for student in students_info:
            timetable = student['Timetable'][classroom_schedule['day']]
            # timetable[classroom_schedule['day']].extend(batch_dict[batch][classroom_schedule['day']])
            updated_student_timetable = []
            for classes in timetable:
                if classes['classroom'] != classroom_schedule['classroom']:
                    updated_student_timetable.append(classes)
            updated_student_timetable.extend(batch_dict[batch][classroom_schedule['day']])
            query = "Timetable" + "." + classroom_schedule['day']
            student_schedule = batch_collection.update_one({"College ID":student['College ID']},{"$set":{query:updated_student_timetable}})
    return timetable


def assign_teacher_schedule(classroom_schedule):
    teacher_dict = {}
    for schedule in classroom_schedule['timetable']:
        if schedule['teacher_id'] not in teacher_dict.keys():
            teacher_dict[schedule['teacher_id']] = {}
            if classroom_schedule['day'] not in teacher_dict[schedule['teacher_id']].keys():
                teacher_dict[schedule['teacher_id']][classroom_schedule['day']] = []
        teacher_dict[schedule['teacher_id']][classroom_schedule['day']].append({
                                                                    "batch": schedule['batch'], 
                                                                    "subject": schedule['subject'], 
                                                                    "startTime": schedule['startTime'], 
                                                                    "endTime": schedule['endTime'],
                                                                    "classroom" : classroom_schedule['classroom']
                                                                    })
    
    teacher_collection = mongo_teachers.db.TEACHERS
    for key in teacher_dict.keys():
        teacher_info = {}
        for doc in teacher_collection.find({"College ID":key}):
            teacher_info = doc
        timetable = {}
        if 'Timetable' in teacher_info.keys():
            timetable = teacher_info['Timetable']
            timetable[classroom_schedule['day']].extend(teacher_dict[key][classroom_schedule['day']])
        else:
            timetable[classroom_schedule['day']] = teacher_dict[key][classroom_schedule['day']]

        teacher_schedule = teacher_collection.update_one({"College ID":key},{"$set":{"Timetable":timetable}})
    return teacher_dict

def update_teacher_schedule(classroom_schedule):
    teacher_dict = {}
    for schedule in classroom_schedule['timetable']:
        if schedule['teacher_id'] not in teacher_dict.keys():
            teacher_dict[schedule['teacher_id']] = {}
            if classroom_schedule['day'] not in teacher_dict[schedule['teacher_id']].keys():
                teacher_dict[schedule['teacher_id']][classroom_schedule['day']] = []
        teacher_dict[schedule['teacher_id']][classroom_schedule['day']].append({
                                                                    "batch": schedule['batch'], 
                                                                    "subject": schedule['subject'], 
                                                                    "startTime": schedule['startTime'], 
                                                                    "endTime": schedule['endTime'],
                                                                    "classroom" : classroom_schedule['classroom']
                                                                    })

    teacher_collection = mongo_teachers.db.TEACHERS
    for key in teacher_dict.keys():
        teacher_info = {}
        for doc in teacher_collection.find({"College ID":key}):
            teacher_info = doc
        timetable_day = teacher_info['Timetable'][classroom_schedule['day']]
        updated_timetable = []
        for classes in range(len(timetable_day)):
            if timetable_day[classes]['classroom'] != classroom_schedule['classroom']:
                updated_timetable.append(timetable_day[classes])
        updated_timetable.extend(teacher_dict[key][classroom_schedule['day']])
        
        key_day = "Timetable." + classroom_schedule['day'] + ""
        teacher_schedule = teacher_collection.update_one({"College ID":key},{"$set":{key_day:updated_timetable}})
    print(updated_timetable)     

@admin.route('/upload_classroom_schedule', methods=['POST'])
def upload_classroom_schedule():
    classroom_schedule = {
        "timetable" : request.json['timetable'],
        "day" : request.json['day'],
    }
    mongo_classroom_collection = mongo_classroom.db[request.json['classroom']]
    classroom_info = []
    
    classroom_day_check = {}
    for doc in mongo_classroom_collection.find({"day": classroom_schedule['day']}):
        classroom_day_check = doc
    if bool(classroom_day_check):
        return {"error": "Timetable for " + classroom_schedule['day'] + " already exists"}, 401
    
    classroom_insert = mongo_classroom_collection.insert_one(classroom_schedule)
    for doc in mongo_classroom_collection.find():
        classroom_info.append(doc)
    
    classroom_schedule["classroom"] = request.json['classroom']
    assign_teacher_schedule(classroom_schedule)
    assign_batch_schedule(classroom_schedule)
    return str(classroom_info)


@admin.route('/update_classroom_schedule/<classroom>', methods=['GET', 'POST'])
def update_classroom_schedule(classroom):
    if request.method == 'GET':
        mongo_classroom_collection = mongo_classroom.db[classroom]
        classroom_info = []
        for doc in mongo_classroom_collection.find():
            classroom_info.append(doc)
        return str(classroom_info)
    
    elif request.method == 'POST':
        mongo_classroom_collection = mongo_classroom.db[classroom]
        classroom_schedule = {
            "timetable" : request.json['timetable'],
            "day" : request.json['day'],
        }
        updated_classroom_schedule = mongo_classroom_collection.update_one({"day":classroom_schedule['day']},{"$set":{"timetable":classroom_schedule['timetable']}})
        classroom_info = {}
        for doc in mongo_classroom_collection.find({"day":classroom_schedule['day']}):
            classroom_info = doc
        
        classroom_schedule["classroom"] = classroom
        update_teacher_schedule(classroom_schedule)
        update_batch_schedule(classroom_schedule)
        return str(classroom_info)
    else:
        return {"error": "Invalid Request"}, 403
