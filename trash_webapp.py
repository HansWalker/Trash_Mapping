# trash_webapp.py

from flask import Flask, request, render_template,  send_file, jsonify
from functions.twelvelabs import search_trash, upload_video, search_video_single
from functions.segment_video import segment_video
import os
import base64
import sys
import json
from Utils import get_trash_locations

app = Flask(__name__)

# Store the uploaded video's video_id
uploaded_video_id = None
file_name_global = None

@app.route('/')
def index():
    # Load API keys
    api_keys = json.load(open('api_keys.json'))
    return render_template('index.html', uploaded_video_id=uploaded_video_id, google_maps_api_key=api_keys["Google Maps"])

@app.route('/upload', methods=['POST'])
def upload():
    global uploaded_video_id
    global video_base64
    global file_name

    # Handle file upload logic here
    uploaded_file = request.files['video']

    if not uploaded_file:
        return "No video file provided"

    # Read the uploaded video data as bytes
    video_data = uploaded_file.read()
    
    #get api keys
    api_keys = json.load(open('api_keys.json'))

    # Encode the video data as base64
    video_base64 = base64.b64encode(video_data).decode('utf-8')

    # Upload the video and get the video_id
    uploaded_video_id = upload_video(uploaded_file.filename, api_keys["12 Labs"])
    
    file_name_global = uploaded_file.filename

    # Automatically segment the video after uploading
    video_filename = f"segmentation.mp4"
    save_path = os.path.join("videos", video_filename)

    # Call the segment_video function and specify the save path
    segment_video("videos/"+uploaded_file.filename, api_keys["Roboflow"])
    # Upload the segmented video
    uploaded_video_id = upload_video(video_filename, api_keys["12 Labs"])

    return render_template('upload_video.html', video_base64=video_base64, uploaded_video_id=uploaded_video_id)

@app.route('/get_trash_data', methods=['POST'])
def get_trash_data():
    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude'])

    trash_data = get_trash_locations(latitude, longitude)
    print(trash_data, file=sys.stderr)
    return jsonify(trash_data)

@app.route('/segment_video', methods=['POST'])
def segment_uploaded_video():
    global uploaded_video_id
    global video_base64
    if not uploaded_video_id:
        return "No video uploaded"

    # Define a unique save path in /videos directory using uuid
    video_filename = f"segmentation.mp4"
    save_path = os.path.join("videos", video_filename)

    # Call the segment_video function and specify the save path
    segment_video(video_base64, save_path)  # Assuming segment_video now saves to the provided path

    # Load API keys
    api_keys = json.load(open('api_keys.json'))

    # Upload the segmented video
    uploaded_video_id = upload_video(video_filename, api_keys["12 Labs"])


    return render_template('upload_video.html', video_base64=video_base64, uploaded_video_id=uploaded_video_id)  # Redirecting to upload page as an example

@app.route('/videos/<filename>')
def serve_video(filename):
    video_path = os.path.join(os.getcwd(), 'videos', filename)
    print(f"Attempting to serve: {video_path}", file=sys.stderr)
    return send_file(video_path, mimetype='video/mp4')

@app.route('/display_search_results', methods=['POST'])
def display_search_results():
    search_query = request.form['search_box']
    
    if not uploaded_video_id:
        return "No video uploaded"
    
    # Load API keys
    api_keys = json.load(open('api_keys.json'))

    result = search_video_single(uploaded_video_id, search_query, api_keys["12 Labs"])
    
    return render_template('search_results_in_video.html', result=result)

@app.route('/query', methods=['POST'])
def query():
    search_query = request.form['query_box']
    # Load API keys
    api_keys = json.load(open('api_keys.json'))

    results = search_trash(search_query, api_keys["12 Labs"])
    return render_template('query_results.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)