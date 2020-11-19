import os
from flask import Flask, render_template, request, session, url_for, redirect, session, send_from_directory
import pymysql.cursors
import requests, json
from functools import wraps

#Initialize the app from flask
app = Flask(__name__)
app.secret_key = "super secret key"

ALLOWED_EXTENSIONS = {'txt', 'pdf'}

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',

                       password='',
                       db='alzheimersDetectionProject',

                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

def login_required(f):
    @wraps(f)
    def dec(*args, **kwargs):
        if not "username" in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return dec

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login/<error>")
def login_err(error):
    return render_template('login.html', error=error)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register/<error>")
def register_err(error):
    return render_template('register.html', error=error)


@app.route('/loginAuth', methods = ['GET','POST'])
def loginAuth():
    username = request.form['username']
    password = request.form['password']

    #cursor used to send queries
    cursor = conn.cursor()
    query = 'SELECT username, role FROM users WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    cursor.close()
    error = None
    if result == None:
        error = 'Invalid login or username'
        return redirect(url_for("login_err", error=error))
    else:
        cursor = conn.cursor()
        query = 'SELECT username, firstName, lastName, phoneNumber, email, role \
                 FROM users WHERE username = %s'
        cursor.execute(query, (username))
        result = cursor.fetchone()
        cursor.close()
        session['username'] = result['username']
        session['firstName'] = result['firstName']
        session['lastName'] = result['lastName']
        session['phoneNumber'] = result['phoneNumber']
        session['email'] = result['email']
        session['role'] = result['role']
        return redirect(url_for("home"))

@app.route('/registerAuth', methods = ['GET','POST'])
def registerAuth():
    username = request.form['username']
    password = request.form['password']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    phoneNumber = request.form['phoneNumber']
    email = request.form['email']
    role = request.form['role']

    #cursor used to send queries
    cursor = conn.cursor()
    query = 'SELECT * FROM users WHERE username = %s'
    cursor.execute(query, (username))
    data = cursor.fetchone()
    cursor.close()
    error = None
    if (data):
        # If the previous query returns data, then user exists
        error = "This user already exists"
        # return render_template('register.html', error=error)
        return redirect(url_for("register_err", error=error))
    else:
        cursor = conn.cursor()
        ins = 'INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, password, firstName, lastName, phoneNumber, email, role))
        conn.commit()
        cursor.close()
        return redirect(url_for("hello"))

# redirect from home.html
@app.route('/medicalReportMenu')
@login_required
def medicalReportMenu():
    return render_template('report_menu.html')

@app.route('/viewReport')
@login_required
def view_report():
    username = session['username']
    if session['role'] == 'caretaker':
        cursor = conn.cursor()
        query = 'SELECT patient_user, report_name FROM reports WHERE caretaker_user=%s'
        cursor.execute(query, (username))
        results = cursor.fetchall()
        cursor.close()
    else:
        cursor = conn.cursor()
        query = 'SELECT caretaker_user, report_name FROM reports WHERE patient_user=%s'
        cursor.execute(query, (username))
        results = cursor.fetchall()
        cursor.close()
        print(results)
    return render_template('view_report.html', results=results)

@app.route('/viewReport/<caretaker>/<patient>/<report>')
@login_required
def view_report_serve(caretaker, patient, report):
    parent = "data/reports/"
    path = (caretaker, patient)
    path = "/".join(path)
    path = parent + path
    upload_folder = path
    app.config['UPLOAD_FOLDER'] = upload_folder
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               report)

@app.route('/uploadReport')
@login_required
def upload_report():
    return render_template('upload_report.html')

@app.route('/uploadReport/<message>')
@login_required
def upload_report_message(message):
    return render_template('upload_report.html', message=message)

@app.route('/uploadReportHandler', methods=['GET', 'POST'])
@login_required
def upload_report_handler():
    patient_username = request.form['patient']
    caretaker_username = session['username']
    upload_folder = "data/reports/%s/%s" % (caretaker_username, patient_username)
    try:
        os.makedirs(upload_folder) 
    except OSError as error:
        pass
    app.config['UPLOAD_FOLDER'] = upload_folder
    message = "Error: An unknown error has occured"

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            message = "Error: You have to upload a file"
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            message = "Error: You did not choose a file to upload"
        # if file upload is well formed
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            message = "Report successfully uploaded"

            # Check against db if filename exists
            # If not add, else no change.
            cursor = conn.cursor()
            query = 'SELECT * FROM reports WHERE caretaker_user=%s AND patient_user=%s AND report_name=%s'
            cursor.execute(query, (session['username'], patient_username, filename))
            data = cursor.fetchone()
            cursor.close()
            error = None
            if (data):
                pass
            else:
                try:
                    cursor = conn.cursor()
                    ins = 'INSERT INTO reports VALUES(%s, %s, %s)'
                    cursor.execute(ins, (session['username'], patient_username, filename))
                    conn.commit()
                    cursor.close()
                except:
                    message = "An error occured when inserting into database. Check if your patient username is correct."
    return redirect(url_for("upload_report_message", message=message))


if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)