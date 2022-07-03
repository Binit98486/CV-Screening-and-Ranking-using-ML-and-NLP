import logging
import os
from io import BytesIO
from sqlite3 import DatabaseError
from flask import Flask, flash, request, redirect, render_template,url_for,session,logging,request,send_file
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from constants import file_constants as cnst
from processing import resume_matcher
from utils import file_utils
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','docx'])
app = Flask(__name__)

db =SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = "secret key"

admin = Admin(app)


app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = cnst.UPLOAD_FOLDER

#user register and login database table
class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

#user resume database table
class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)  

admin.add_view(ModelView(user,Upload,db.session))

#for resume upload
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']

        upload = Upload(filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()

        return f'Uploaded: {file.filename}'
    return render_template('index.html')

@app.route('/download/<upload_id>')
def download(upload_id):
    upload = Upload.query.filter_by(id=upload_id).first()
    return send_file(attachment_filename=upload.filename, as_attachment=True)    

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route("/login",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        login = user.query.filter_by(username=uname, password=passw).first()
        if login is not None:
            flash('You have successfully logged in')
            return redirect(url_for("uploadcv")) 
    return render_template("login.html")   

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']

        signup = user(username = uname, email = mail, password = passw)
        db.session.add(signup)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("signup.html")    

@app.route('/logout/')
def logout():
    # Removing data from session by setting logged_flag to False.
    session['logged_in'] = False
    # redirecting to home page
    return redirect(url_for('index.html'))    

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')    

@app.route('/uploadcv')
def uploadcv():
    return render_template('uploadcv.html')


 

@app.route('/failure')
def failure():
   return 'No files were selected'

@app.route('/success/<name>')
def success(name):
   return 'Files %s has been selected' %name

@app.route('/uploadcv', methods=['POST', 'GET'])
def check_for_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'reqFile' not in request.files:
           flash('Requirements document can not be empty')
           return redirect(request.url)
        if 'resume_files' not in request.files:
           flash('Select at least one resume File to proceed further')
           return redirect(request.url)
        file = request.files['reqFile']
        if file.filename == '':
           flash('Requirement document has not been selected')
           return redirect(request.url)
        resume_files = request.files.getlist("resume_files")
        if len(resume_files) == 0:
            flash('Select atleast one resume file to proceed further')
            return redirect(request.url)
        if ((file and allowed_file(file.filename)) and (len(resume_files) > 0)):
           #filename = secure_filename(file.filename)
           abs_paths = []
           filename = file.filename
           req_document = cnst.UPLOAD_FOLDER+'\\'+filename
           file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
           for resumefile in resume_files:
               filename = resumefile.filename
               abs_paths.append(cnst.UPLOAD_FOLDER+'\\'+ filename)
               resumefile.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
           result = resume_matcher.process_files(req_document,abs_paths)
           for file_path in abs_paths:
               file_utils.delete_file(file_path)

           return render_template("resume_results.html", result=result)
        else:
           flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
           return redirect(request.url)

if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)
