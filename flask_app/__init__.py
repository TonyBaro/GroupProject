from flask import Flask
app = Flask(__name__)
app.secret_key = "My Secret Key! SHHHHH!"
UPLOAD_FOLDER = 'flask_app\static\img'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024