from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def add_user(cls,data):
        query="INSERT INTO users(username,email,password) VALUES (%(username)s,%(email)s,%(password)s)"
        return connectToMySQL('projects-group').query_db( query, data)

    @classmethod
    def validate(cls,data):
        valid = True
        query="SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('projects-group').query_db( query, data )
        if len(results) >= 1:
            flash("Email already taken.","register")
            valid = False
        if len(data['username']) < 3:
            flash("Username must be at least 3 characters","register")
            valid =  False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email","register")
            valid=False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters","register")
            valid =  False
        if data['password'] != data['confirm']:
            flash("Passwords don't match","register")
            valid = False
        return valid

    @classmethod
    def log_in(cls,data):
        query="SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('projects-group').query_db( query, data )
        return cls(results[0])
        
    @classmethod
    def get_user_by_id(cls,data):
        query="SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL('projects-group').query_db( query, data )
        return results[0]


