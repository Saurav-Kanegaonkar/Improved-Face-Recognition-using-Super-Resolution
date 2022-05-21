from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_mail import Mail

mongo_teachers = PyMongo()
mongo_students = PyMongo()
mongo_forgot_passwords = PyMongo()
mongo_classroom = PyMongo()
mongo_sessions = PyMongo()
bcrypt = Bcrypt()
mail = Mail()