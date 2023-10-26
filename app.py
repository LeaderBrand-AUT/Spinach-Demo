from flask import Flask, render_template, redirect, request, url_for, flash
from model import classifySpinach
import json

from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'C:\\Users\\PC\\Documents\\GitHub\\RnD\\Spinach-Demo\\spinach_test'  # Replace with your image folder path
app.secret_key = 'leaderbrand'

@app.route('/')
@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))

    return render_template('login.html', title='Login')

@app.route('/dashboard')
def dashboard(): 
    return render_template('dashboard.html', title='Dashboard')

@app.route('/reports')
def reports():
    # read file
    with open('./dummydata/reports.json', 'r') as myfile:
        dummydata = json.load(myfile)

    for report in dummydata:
        print(report)
    return render_template('reports.html', reports=dummydata, backButton='dashboard')

@app.route('/view_report')
def view_report():
    with open('./dummydata/reports.json', 'r') as myfile:
        dummydata = json.load(myfile)

    return render_template('view_report.html', report=dummydata[0], backButton='reports')

@app.route('/live_data')
def live_data():
    return render_template('live_data.html', backButton='dashboard')


@app.route('/classifier', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            spinach = classifySpinach(filename)  
            flash(spinach)
            return redirect(request.url)
    return render_template('classifier.html')  

if __name__ == '__main__':
    app.run(debug=True)




app.run(host='0.0.0.0', port=81)