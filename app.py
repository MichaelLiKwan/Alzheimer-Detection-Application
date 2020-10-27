from flask import Flask, render_template, request, session, url_for, redirect

#Initialize the app from flask
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('design.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route("/login")
def login():
    render_template("login.html")

@app.route("/register")
def register():
    render_template("register.html")

if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)