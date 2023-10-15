# trash_webapp.py

from flask import Flask, request, render_template, jsonify, redirect, url_for
from vector_db import vector_db_search
from twelvelabs import search_trash, upload_video, search_video_single
import os
import base64

app = Flask(__name__)

# Store the uploaded video's video_id
uploaded_video_id = None

@app.route('/')
def index():
    return render_template('index.html', uploaded_video_id=uploaded_video_id)

@app.route('/upload', methods=['POST'])
def upload():
    global uploaded_video_id
    # Handle file upload logic here
    uploaded_file = request.files['video']
    
    if not uploaded_file:
        return "No video file provided"

    # Read the uploaded video data as bytes
    video_data = uploaded_file.read()

    # Encode the video data as base64
    video_base64 = base64.b64encode(video_data).decode('utf-8')

    # Upload the video and get the video_id
    uploaded_video_id = upload_video(uploaded_file.filename)

    return render_template('upload_video.html', video_base64=video_base64, uploaded_video_id=uploaded_video_id)

@app.route('/display_search_results', methods=['POST'])
def display_search_results():
    search_query = request.form['search_box']
    
    if not uploaded_video_id:
        return "No video uploaded"
    
    result = search_video_single(uploaded_video_id, search_query)
    
    return render_template('search_results_in_video.html', result=result)

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form['search_box']
    # Assuming vector_db_search returns the relative path to the video within the 'videos' folder
    video_result = vector_db_search(search_query)
    
    if video_result:
        video_path = os.path.join('videos', video_result)
        video_base64 = vector_db_search(video_path)
        return render_template('search_results_in_video.html', video_base64=video_base64, uploaded_video_id=uploaded_video_id)
    else:
        return render_template('search_results_in_video.html', video_base64=None, uploaded_video_id=uploaded_video_id)

@app.route('/query', methods=['POST'])
def query():
    search_query = request.form['query_box']
    results = search_trash(search_query)
    return render_template('query_results.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)