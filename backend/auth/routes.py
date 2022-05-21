from flask import ( Blueprint, flash, g, redirect, render_template, request, url_for, session )
from backend.extensions import mongo_students, mongo_teachers, bcrypt, mail, mongo_forgot_passwords, mongo_sessions
from bson.objectid import ObjectId
from flask_mail import Message
from password_generator import PasswordGenerator
import datetime
import functools
import json

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    if request.method=='POST':
        college_id = int(request.json['college_id'])
        password = request.json['password']
        role = request.json['role']
        if role == 'Teacher':
            teacher_collection = mongo_teachers.db.TEACHERS
            teacher_info = {}
            for doc in teacher_collection.find({"College ID": college_id}):
                teacher_info = doc
            if not bool(teacher_info):
                print("Teacher does not exist")
                return json.dumps({"error": "Teacher does not exist"}), 401
            
            if "password" not in teacher_info.keys():
                print("Teacher has not registered, please register.")
                return json.dumps({"error": "Teacher has not registered, please register"}), 401
            
            if not bcrypt.check_password_hash(teacher_info["password"], password):
                print("Incorrect password")
                return json.dumps({"error": "Incorrect password"}), 401
            
            del teacher_info['_id']
            del teacher_info['password']
            session_collection = mongo_sessions.db.SESSIONS
            result = session_collection.delete_many({})
            session_collection.insert_one(
                                            {
                                                "user_id": teacher_info["College ID"],
                                                "user_name" : teacher_info["Teacher Name"],
                                                "user_role" : teacher_info["Role"]
                                            }
                                        )
            return json.dumps(teacher_info), 200

        elif role == 'Student':
            student_collection = mongo_students.db.BTECH_COMPS_2018_2022
            student_info = {}
            for doc in student_collection.find({"College ID": college_id}):
                student_info = doc
            if not bool(student_info):
                print("Student does not exist")
                return json.dumps({"error": "Student does not exist"}), 401

            if "password" not in student_info.keys():
                print("Student has not registered, please register.")
                return json.dumps({"error": "Student has not registered, please register"}), 401
            
            if not bcrypt.check_password_hash(student_info["password"], password):
                print("Incorrect password")
                return json.dumps({"error": "Incorrect password"}), 401
            
            del student_info['_id']
            del student_info['password']
            session_collection = mongo_sessions.db.SESSIONS
            result = session_collection.delete_many({})
            session_collection.insert_one(
                                            {
                                                "user_id": student_info["College ID"],
                                                "user_name" : student_info["Student Name"],
                                                "user_role" : student_info["Role"]
                                            }
                                        )
            return json.dumps(student_info), 200
        else:
            # admin_collection = mongo_admins.db.ADMINS
            # admin = admin_collection.find({"id": id})
            pass
        return {"error": "Invalid Credentials"}, 401
    


@auth.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        college_id = int(request.json['college_id'])
        password = request.json['password']
        role = request.json['role']

        if role == 'Teacher':
            teacher_collection = mongo_teachers.db.TEACHERS
            teacher_info = {}
            for doc in teacher_collection.find({"College ID": college_id}):
                teacher_info = doc
            if not bool(teacher_info):
                print("Teacher does not exist")
                return json.dumps({"error": "Teacher does not exist"}), 401
            
            if "password" in teacher_info.keys():
                print("Teacher is already registered, please login.")
                return json.dumps({"error": "Teacher is already registered, please login"}), 401
            
            hashed_password = bcrypt.generate_password_hash(password)
            updated_teacher = teacher_collection.update_one({"College ID":college_id},{"$set":{"password":hashed_password}})

            session_collection = mongo_sessions.db.SESSIONS
            result = session_collection.delete_many({})
            session_collection.insert_one(
                                            {
                                                "user_id": teacher_info["College ID"],
                                                "user_name" : teacher_info["Teacher Name"],
                                                "user_role" : teacher_info["Role"]
                                            }
                                        )
            
            for doc in teacher_collection.find({"College ID": college_id}):
                teacher_info = doc
            del teacher_info['_id']
            del teacher_info['password']
            return json.dumps(teacher_info), 200
            
        elif role == 'Student':
            student_collection = mongo_students.db.BTECH_COMPS_2018_2022
            student_info = {}
            for doc in student_collection.find({"College ID": college_id}):
                student_info = doc
            if not bool(student_info):
                print("Student does not exist")
                return json.dumps({"error": "Student does not exist"}), 401

            if "password" in student_info.keys():
                print("Student is already registered, please login.")
                return json.dumps({"error": "Student is already registered, please login"}), 401
            
            hashed_password = bcrypt.generate_password_hash(password)
            updated_student = student_collection.update_one({"College ID":college_id},{"$set":{"password":hashed_password}})

            session_collection = mongo_sessions.db.SESSIONS
            result = session_collection.delete_many({})
            session_collection.insert_one(
                                            {
                                                "user_id": student_info["College ID"],
                                                "user_name" : student_info["Student Name"],
                                                "user_role" : student_info["Role"]
                                            }
                                        )
            
            for doc in student_collection.find({"College ID": college_id}):
                student_info = doc
            del student_info['_id']
            del student_info['password']
            return json.dumps(student_info), 200
        
        else:
            # admin_collection = mongo_admins.db.ADMINS
            # admin = admin_collection.find({"id": id})
            pass
        return {"error": "Invalid Credentials"}, 401

    return render_template('auth/register.html')

@auth.route('/logout', methods=['GET'])
def logout():
    session_collection = mongo_sessions.db.SESSIONS
    result = session_collection.delete_many({})
    return {"success": "Successfully Logged out"}, 200
    

@auth.route('/profile', methods=['GET'])
def profile():
    session_collection = mongo_sessions.db.SESSIONS
    session_info = {}
    for doc in session_collection.find():
        session_info = doc

    
    if not bool(session_info):
        return {"error": "Unauthorized, Please login :)"}, 401

    if session_info["user_role"] == "teacher":
        teacher_collection = mongo_teachers.db.TEACHERS
        teacher_info = {}
        for doc in teacher_collection.find({"College ID": session_info["user_id"]}):
            teacher_info = doc
        del teacher_info['_id']
        del teacher_info['password']
        return json.dumps(teacher_info)

    elif session_info["user_role"] == "student":
        student_collection = mongo_students.db.BTECH_COMPS_2018_2022
        student_info = {}
        for doc in student_collection.find({"College ID": session_info["user_id"]}):
            student_info = doc
        del student_info['_id']
        del student_info['password']
        return json.dumps(student_info)

    else:
        pass

@auth.route('/send_forgot_password_email', methods=["POST"])
def send_forgot_password_email():
    msg = Message('OTP For Password Change', sender = 'svkanegaonkar_b18@ce.vjti.ac.in', recipients = [request.json['email']])
    pwo = PasswordGenerator()
    OTP_PASSWORD = pwo.generate()
    OTP_MAIL = request.json['email']
    msg.body = "Hello, your otp for password change is " + OTP_PASSWORD
    mail.send(msg)
    
    forgot_passwords_collection = mongo_forgot_passwords.db.OTP_CREDENTIALS
    credential = {"OTP": OTP_PASSWORD, "User":OTP_MAIL, "Timestamp": str(datetime.datetime.now())}
    user_info = {}
    for doc in forgot_passwords_collection.find({"User": OTP_MAIL}):
        user_info = doc
    if bool(user_info):
        updated_user = forgot_passwords_collection.update_one({"User": OTP_MAIL}, {"$set":{"Timestamp":credential['Timestamp'], "OTP":credential['OTP']}})
    else:
        new_user = forgot_passwords_collection.insert_one(credential)

    return str(credential)

@auth.route('/change_password', methods=["POST"])
def change_password():
    new_password = request.json['new_password']
    email = request.json['email']
    otp = request.json['otp']
    role = request.json['role']
    
    forgot_passwords_collection = mongo_forgot_passwords.db.OTP_CREDENTIALS
    user_info = {}
    for doc in forgot_passwords_collection.find({"User": email}):
        user_info = doc
    if not bool(user_info):
        return {"error": "OTP for the user does not exist, please click on forgot password"}, 401
    
    current_timestamp = datetime.datetime.now()
    previous_timestamp = datetime.datetime.strptime(user_info["Timestamp"], "%Y-%m-%d %H:%M:%S.%f")
    time_difference = current_timestamp - previous_timestamp

    if otp == user_info['OTP'] and email == user_info['User'] and time_difference.seconds <= 600:
        if role == 'Teacher':
            teacher_collection = mongo_teachers.db.TEACHERS
            teacher_info = {}
            for doc in teacher_collection.find({"Email ID": email}):
                teacher_info = doc
            if not bool(teacher_info):
                flash("Teacher does not exist, please ask the admin to setup your account")
                return redirect(url_for("auth.login"))

            hashed_password = bcrypt.generate_password_hash(new_password)
            updated_teacher = teacher_collection.update_one({"Email ID":email},{"$set":{"password":hashed_password}})

            session["user_id"] = teacher_info["College ID"]
            session["user_name"] = teacher_info["Teacher Name"]
            session["user_role"] = teacher_info["Role"]

            for doc in teacher_collection.find({"College ID": teacher_info["College ID"]}):
                teacher_info = doc
            return redirect(url_for("teach.lectures", college_id=teacher_info["College ID"]))

        elif role == 'Student':
            student_collection = mongo_students.db.BTECH_COMPS_2018_2022
            student_info = {}
            for doc in student_collection.find({"Email ID": email}):
                student_info = doc
            if not bool(student_info):
                flash("Student does not exist, please ask the admin to setup your account")
                return redirect(url_for("auth.login"))

            hashed_password = bcrypt.generate_password_hash(new_password)
            updated_teacher = student_collection.update_one({"Email ID":email},{"$set":{"password":hashed_password}})

            session["user_id"] = student_info["College ID"]
            session["user_name"] = student_info["Student Name"]
            session["user_role"] = student_info["Role"]

            for doc in student_collection.find({"College ID": student_info["College ID"]}):
                student_info = doc
            return str(student_info)
        else:
            pass
    else:
        return {"error": "Unauthorized, Please login :)"}, 401

# @auth.before_app_request
# def load_logged_in_user():
#     g.user_name = session.get('user_name')
#     g.user_id = session.get('user_id')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        session_collection = mongo_sessions.db.SESSIONS
        session_info = {}
        for doc in session_collection.find():
            session_info = doc
        if not bool(session_info):
            return {"error": "Unauthorized, Please login :)"}, 401

        return view(**kwargs)

    return wrapped_view

def teacher_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        session_collection = mongo_sessions.db.SESSIONS
        session_info = {}
        for doc in session_collection.find():
            session_info = doc
        if not bool(session_info) or session_info['user_role'] != 'teacher':
            return {"error": "Teacher Authentication Required"}, 401

        return view(**kwargs)

    return wrapped_view