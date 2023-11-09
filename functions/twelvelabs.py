import requests
import os
import cv2
import numpy as np
import sys
import json
INDEX_ID = "6531831cd61fd7c0a2b3e2a1"
#654027d439db8bc2adf7520d
def search_trash(query, API_KEY):

    API_URL = "https://api.twelvelabs.io/v1.2"

    data = {
        "query": query,
        "index_id": INDEX_ID,
        "search_options": ["visual"]
    }

    response = requests.post(f"{API_URL}/search", headers={"x-api-key": API_KEY}, json=data)


    results = []

    # Getting thumbnail and relevant data
    for i in range(len(response.json()['data'])):
        score = response.json()['data'][i]['score']
        video_id = response.json()['data'][i]['video_id']
        thumbnail_url = response.json()['data'][i]['thumbnail_url']
        results.append({"score": score, "video_id": video_id, "thumbnail_url": thumbnail_url})

    return results

def search_video_single(video_id, query, API_KEY):

    API_URL = "https://api.twelvelabs.io/v1.2"


    headers = {
    "accept": "application/json",
    "x-api-key": API_KEY,
    "Content-Type": "application/json"}
    
    data = {
    "query": query,
    "search_options": ["visual", "conversation", "text_in_video", "logo"],
    "threshold": "high",
    "filter": { "id": [video_id] },
    "index_id": INDEX_ID }


    response = requests.post(f"{API_URL}/search", headers=headers, json=data)

    results = []

    for i in range(len(response.json()['data'])):
        score = response.json()['data'][i]['score']
        video_id = response.json()['data'][i]['video_id']
        results.append({"score": score, 'start_time':response.json()['data'][i]['start'], 
                        'end_time':response.json()['data'][i]['end']})
    
    return results


def upload_video(file_path, API_KEY):
    file_path = 'videos/'+file_path

    API_URL = "https://api.twelvelabs.io/v1.2"
    TASKS_URL = f"{API_URL}/tasks"
    file_stream = open(file_path,"rb")

    data = {
    "index_id": INDEX_ID, 
    "language": "en"}
    file_param = [
        ("video_file", (os.path.splitext(file_path)[0], file_stream, "application/octet-stream"))]
    
    response = requests.post(TASKS_URL, headers={"x-api-key": API_KEY}, data=data, files=file_param)

    
    print(response.json(), file=sys.stderr)
    if '_id' in response.json().keys():
        return response.json()['_id']
    else:
        return None
