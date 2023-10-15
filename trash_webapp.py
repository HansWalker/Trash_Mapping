from flask import Flask, request, render_template, redirect, url_for, jsonify
from vector_db import vector_db_search
from twelvelabs import search_trash, upload_video, search_video_single
import os
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Handle file upload logic here
    uploaded_file = request.files['video']
    # Process the uploaded file (e.g., analyze it, etc.)

    # Read the uploaded video data as bytes
    video_data = uploaded_file.read()

    # Encode the video data as base64
    video_base64 = base64.b64encode(video_data).decode('utf-8')

    video_id = upload_video(uploaded_file.filename)

    return render_template('upload_video.html', video_base64=video_base64)

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form['search_box']
    # Assuming vector_db_search returns the relative path to the video within the 'videos' folder
    video_result = vector_db_search(search_query)
    
    if video_result:
        video_path = os.path.join('videos', video_result)
        video_base64 = vector_db_search(video_path)
        return render_template('search_results.html', video_base64=video_base64)
    else:
        return render_template('search_results.html', video_base64=None)

@app.route('/query', methods=['POST'])
def query():
    search_query = request.form['query_box']
    results = search_trash(search_query)
    return render_template('query_results.html', results=results)

# Route to handle the AJAX request for search_video_single
@app.route('/search_video_single/<video_id>')
def search_video_single_route(video_id):
    # Call the search_video_single function with the provided video_id
    result = search_video_single(video_id)

    # Return the result as JSON
    return jsonify(result)
if __name__ == '__main__':
    app.run(debug=True)