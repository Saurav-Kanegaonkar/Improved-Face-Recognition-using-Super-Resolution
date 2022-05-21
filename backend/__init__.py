from flask import Flask, jsonify
from flask_cors import CORS
from .config import ApplicationConfig
from .extensions import mongo_students, mongo_teachers, bcrypt, mail, mongo_forgot_passwords, mongo_classroom, mongo_sessions
from .auth.routes import auth
from .teacher.routes import teach
from .admin.routes import admin
from .student.routes import student
from .regionOfInterest.region_of_interest import roi 
import sys
import os

directory = os.getcwd() +  "/backend/face_rec"
directory.replace("\\","/")
sys.path.insert(0, directory)

directory = os.getcwd() +  "/backend/dlib_face_det"
directory.replace("\\","/")
sys.path.insert(1,directory)

directory = os.getcwd() +  "/backend/SRGAN"
directory.replace("\\","/")
sys.path.insert(2,directory)

from face_rec import face_rec
from dataset import run

my_json = ''

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(auth)
    app.register_blueprint(teach)
    app.register_blueprint(admin)
    app.register_blueprint(student)
    app.config.from_object(ApplicationConfig)
    mail.init_app(app)

    mongo_teachers.init_app(app, uri = 'mongodb://localhost:27017/FYP_TEACHERS')
    mongo_students.init_app(app, uri = 'mongodb://localhost:27017/FYP_STUDENTS')
    mongo_forgot_passwords.init_app(app, uri = 'mongodb://localhost:27017/FYP_FORGOT_PASSWORDS')
    mongo_classroom.init_app(app, uri = 'mongodb://localhost:27017/FYP_CLASSROOM')
    mongo_sessions.init_app(app, uri = 'mongodb://localhost:27017/FYP_SESSIONS')
    bcrypt.init_app(app)

    @app.route('/')
    def welcome():
        return "I'm Lelouch Vi Britannia of the Royal Family, 99th Emperor of this realm. I command you to obey me. OBEY ME SUBJECTS, OBEY ME WORLD."

    @app.route('/updateAttendance')
    def updateAtt():
        roi()
        run()
        global my_json
        my_json = face_rec()
        return my_json

    @app.route('/hello')
    def hello():
        global my_json
        print("HELLO", my_json)
        return my_json
    
    return app