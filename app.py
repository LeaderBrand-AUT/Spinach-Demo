from flask import Flask, render_template

app = Flask(__name__)

# Variable to keep track of whether user is logged in. Will be implemented properly one day
isLoggedIn = False

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Produce Scanner')

@app.route('/login')
def login():
    if (not isLoggedIn):
        return render_template('login.html')

app.run(host='0.0.0.0', port=81)