from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='',
                       db='alzheimersPatients',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route('/loginAuth', methods = ['GET','POST'])
def loginAuth():
    username = request.form['username']
    password = request.form['password']

    #cursor used to send queries
    cursor = conn.cursor()
    query = 'SELECT role FROM users WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
    role = cursor.fetchone()
    cursor.close()
    error = None
    if role['role'] == 'patient':
        cursor = conn.cursor()
        query = 'SELECT * FROM users WHERE username = %s and password = %s and role = %s'
        cursor.execute(query, (username, password, 'patient'))
        data = cursor.fetchone()
        print(data)
        cursor.close()
        return render_template('home.html', data=data)
        #return render_template('patientHome.html', data=data)
    elif role == 'caretaker':
        cursor = conn.cursor()
        query = 'SELECT * FROM users WHERE username = %s and password = %s and role = %s'
        cursor.execute(query, (username, password, 'caretaker'))
        data = cursor.fetchone()
        cursor.close()
        return render_template('home.html', data=data)
        #return render_template('caretakerHome.html', data=data)
    elif role == 'admin':
        cursor = conn.cursor()
        query = 'SELECT * FROM users WHERE username = %s and password = %s and role = %s'
        cursor.execute(query, (username, password, 'admin'))
        data = cursor.fetchone()
        cursor.close()
        return render_template('home.html', data=data)
        #return render_template('adminHome.html', data=data)
    else:
        error = 'Invalid login or username'
        return render_template('login.html', error=error)

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
        return render_template('register.html', error=error)
    else:
        ins = 'INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, password, firstName, lastName, phoneNumber, email, role))
        conn.commit()
        cursor.close()
        return render_template('design.html')














if __name__ == "__main__":
    app.run('127.0.0.1', 4000, debug = True)