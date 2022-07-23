from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.image import Image
import urllib.request
import os
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=["POST"])
def register():
    data = {
            'username':request.form['username'],
            'email':request.form['email'],
            'password':request.form['password'],
            'confirm':request.form['confirm']
        }
    if User.validate(data) == True:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data.update({'password':pw_hash})
        user = User.add_user(data)
        session['user_id'] = user
        return redirect('/dashboard')
    else:
        return redirect('/')

@app.route('/log_in', methods=["POST"])
def log_in():
    data={
        'email':request.form['email']
    }
    user = User.log_in(data)
    if not user:
        flash("Invalid email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Bad Email","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        session.clear()
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    user = User.get_user_by_id(data)
    return render_template('dashboard.html', user = user, img = Image.get_user_image(data))


@app.route("/uploadPic")
def upload():
    if "user_id" not in session:
        return redirect("/logout")
    image_data = {
        "user_id": session["user_id"],
    }
    return render_template("uploadPic.html", img = Image.get_user_image(image_data))



@app.route("/add/image", methods = ["POST"])
def add_image():
    if "user_id" not in session:
        return redirect("/logout")
    
    if "file" not in request.files:
        flash("No file part") #ensures that an extension is selected eg .png or .jpg
        return redirect("/uploadPic")
    file = request.files["file"]
    if file.filename == "":  #ensures that the file is not empty
        flash("No image selected for uploading")  
        return redirect("/uploadPic")
    
    if file and allowed_file(file.filename):  #if a file is selected and it meets the .png, .jpeg, jpg or .gif requirements
        filename = secure_filename(file.filename) #allows the filename to be safely stored
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #this joins the file name and our upload folder together (our upload folder will be our static/img folder)
        
        data = {
            "file" : filename,
            "user_id": session["user_id"],
        }
        Image.add_image(data)
        flash("Image uploaded successfully")
        return redirect("/uploadPic")
    else:
        flash("Allowed image types are - png, jpg, jpeg, gif")
        return redirect("/uploadPic")


@app.route('/log_out')
def log_out():
    session.clear()
    return redirect('/')

