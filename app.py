import base64
from io import BytesIO
from PIL import Image
from flask import Flask, Response, render_template, redirect, request, url_for, flash
import json
import cv2
from camera import gen_frames, get_frame
from scripts.classifier import classifyFrame
from scripts.database import db
import scripts.preprocessing.image_resize as resize_frame
import scripts.preprocessing.white_balance as white_balance

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://leaderbrand:password@localhost:5342/report_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    try:
        db.create_all()
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")

@app.route('/')
@app.route('/login', methods=('GET', 'POST'))
def login():
    # print("Creating database tables...")
    # db.create_all()
    # print("Database tables should be created.")
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

@app.route('/generate_report')
def generate_report():
    frame = get_frame()
    resized_frame = resize_frame.resize_frame(frame)
    white_balanced = white_balance.white_balancing(resized_frame)
    
    report = classifyFrame(white_balanced)

    # Encode image data as base64-encoded string
    resized_frame_buffer = BytesIO()
    Image.fromarray(cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB), mode='RGB').save(resized_frame_buffer, format="JPEG")
    resized_frame_base64 = base64.b64encode(resized_frame_buffer.getvalue()).decode("utf-8")

    white_balanced_buffer = BytesIO()
    Image.fromarray(cv2.cvtColor(white_balanced, cv2.COLOR_BGR2RGB), mode='RGB').save(white_balanced_buffer, format="JPEG")
    white_balanced_base64 = base64.b64encode(white_balanced_buffer.getvalue()).decode("utf-8")

    classification = {
        "resized_image": resized_frame_base64,
        "white_balanced_image": white_balanced_base64,
        "report": report
    }

    return classification
    
@app.route('/live_data')
def live_data():
    return render_template('live_data.html', backButton='dashboard')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(host='0.0.0.0', port=81)