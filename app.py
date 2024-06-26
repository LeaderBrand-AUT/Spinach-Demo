import base64
from io import BytesIO
from PIL import Image
from flask import Flask, Response, jsonify, render_template, redirect, request, url_for, abort
import json

from sqlalchemy import desc
import cv2
import live_feed
import video_from_file
from scripts.classifier import classifyFrame
from scripts.database import db
from scripts.report import Report
from scripts.constants import IMAGE_HEIGHT, IMAGE_WIDTH, CURRENT_MODEL, STREAM_FPS
import scripts.preprocessing.image_resize as resize_frame
import scripts.preprocessing.white_balance as white_balance
import scripts.preprocessing.get_least_blurry as get_least_blurry
from scripts.visualize_reports import get_all_reports
from scripts.visualize_reports import count_moisture_levels

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

# Requires a 'source' URL param with either 'live_feed' or 'from_file' as the value.
@app.route('/generate_report')
def generate_report():
    source = request.args.get('source')

    # use URL param to get clip from relevant source
    if (source == 'live_feed'):
        clip = live_feed.get_clip()
    elif (source == 'from_file'):
        clip = video_from_file.get_clip()
    else:
        abort(400, 'Invalid URL params: source parameter equal "live_feed" or "from_file"')

    if clip is None:
        abort(500, 'Unable to retrieve frame from source')
    
    # save gif of clip to be displayed on frontend
    # to be implemented

    # get least blurry frame from clip
    frame = get_least_blurry.get_least_blurry(clip)
    if frame is None:
        abort(500, 'Failed to get least blurry frame, please try again')
    
    least_blurry_frame = frame
    resized_frame = resize_frame.resize_frame(frame)
    white_balanced = white_balance.white_balancing(resized_frame)
    
    report = classifyFrame(white_balanced)

    # Encode image data as base64-encoded string
    least_blurry_frame_buffer = BytesIO()
    Image.fromarray(cv2.cvtColor(least_blurry_frame, cv2.COLOR_BGR2RGB), mode='RGB').save(least_blurry_frame_buffer, format="JPEG")
    least_blurry_frame_base64 = base64.b64encode(least_blurry_frame_buffer.getvalue()).decode("utf-8")

    resized_frame_buffer = BytesIO()
    Image.fromarray(cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB), mode='RGB').save(resized_frame_buffer, format="JPEG")
    resized_frame_base64 = base64.b64encode(resized_frame_buffer.getvalue()).decode("utf-8")

    white_balanced_buffer = BytesIO()
    Image.fromarray(cv2.cvtColor(white_balanced, cv2.COLOR_BGR2RGB), mode='RGB').save(white_balanced_buffer, format="JPEG")
    white_balanced_base64 = base64.b64encode(white_balanced_buffer.getvalue()).decode("utf-8")

    classification = {
        "least_blurry_frame": least_blurry_frame_base64,
        "resized_image": resized_frame_base64,
        "white_balanced_image": white_balanced_base64,
        "report": report
    }

    return classification
    
# Live video feed
@app.route('/demo_live_feed')
def demo_live_feed():
    return render_template('demo_live_feed.html', backButton='dashboard')

@app.route('/live_video_feed')
def live_video_feed():
    return Response(live_feed.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# Example video feed from file
@app.route('/demo_from_file')
def demo_from_file():
    return render_template('demo_from_file.html', backButton='dashboard')

@app.route('/file_video_feed')
def file_video_feed():
    return Response(video_from_file.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Get report data from DB
@app.route('/get_report_data')
def get_report_data():
    rows = request.args.get('rows')
    data = db.session.query(Report).order_by(desc(Report.time)).limit(rows).all()

    reports = [report.to_dict() for report in data]

    return jsonify(reports)
    
@app.route('/visuals', methods=['GET'])
def visuals():
    count_dict = count_moisture_levels()
    data = {
        "labels": list(count_dict.keys()),
        "data": list(count_dict.values())
    }
    return render_template('visuals.html', data=data, backButton='reports')

# Show information about current build
print(f"Current model: {CURRENT_MODEL}")
print(f"Input image shape: {IMAGE_WIDTH}px x {IMAGE_HEIGHT}px")
print(f"Stream FPS: {STREAM_FPS}")

app.run(host='0.0.0.0', port=81)