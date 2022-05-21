from datetime import timedelta

class ApplicationConfig:
    JWT_SECRET_KEY= "please-remember-to-change-me"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    SECRET_KEY = "vjvkgGHJVGlHVHkHVJvLJv"
    MAIL_SERVER ='smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'svkanegaonkar_b18@ce.vjti.ac.in'
    MAIL_PASSWORD = 'Shy@123456'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True