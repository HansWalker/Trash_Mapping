import requests
import os
import cv2
import numpy as np
import sys
import json
import time
import random
INDEX_ID = "6551602e6e5e7fa6dac81837"
API_URL = "https://api.twelvelabs.io/v1.2"

#654027d439db8bc2adf7520d
def search_trash(query, API_KEY):

    data = {
        "query": query,
        "index_id": INDEX_ID,
        "search_options": ["visual"]
    }

    response = requests.post(f"{API_URL}/search", headers={"x-api-key": API_KEY}, json=data)

    response = response.json()


    results = []

    # Getting thumbnail and relevant data
    for i in range(len(response['data'])):
        score = response['data'][i]['score']
        video_id = response['data'][i]['video_id']
        video_location = Get_Video_Metadata(response['data'][i]['video_id'],API_KEY)['Location Type']
        thumbnail_url = response['data'][i]['thumbnail_url']
        results.append({"score": score,"video_location": video_location, "video_id": video_id, "thumbnail_url": thumbnail_url})

    return results

def search_video_single(video_id, query, API_KEY):


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

    
    TASKS_URL = f"{API_URL}/tasks"
    file_stream = open(file_path,"rb")

    data = {
        "index_id": INDEX_ID, 
        "language": "en"}

    file_param = [
        ("video_file", (os.path.splitext(file_path)[0], file_stream, "application/octet-stream"))]
    
    response = requests.post(TASKS_URL, headers={"x-api-key": API_KEY}, data=data, files=file_param)


    if '_id' in response.json().keys():
        return response.json()['_id']
    else:
        return None

def classify_latest_video(id, file_name, API_KEY):
    classify_url = f"{API_URL}/classify"
    file_name = file_name.split('.')[0]

    video_list = get_video_list(API_KEY)
    time_initiated = time.time()
    video_uploaded=True
    video_index = 0
    for i, next_video in enumerate(video_list):
        if(next_video['metadata']['filename']==file_name):
            video_uploaded=False
            video_index = i
            break
    while(video_uploaded):
        time.sleep(60)
        video_list = get_video_list(API_KEY)
        for i, next_video in enumerate(video_list):
            print(next_video['metadata']['filename'],"   ",file_name)
            if(next_video['metadata']['filename']==file_name):
                video_uploaded=False
                video_index = i
                break
    
    id = video_list[video_index]["_id"]

    meta_url = f"{API_URL}/indexes/{INDEX_ID}/videos/{id}"

    print("\n\nStarting Metadata",time.time()-time_initiated,"\n\n", file=sys.stderr)
    payload = {
        "page_limit": 10,
        "include_clips": False,
        "threshold": {
            "min_video_score": 15,
            "min_clip_score": 15,
            "min_duration_ratio": 0.5
        },
        "show_detailed_score": False,
        "options": ["conversation"],
        "conversation_option": "semantic",
        "classes": [
            {
                "prompts": ["This video is taken in an urban enviorment", "This means a dense environment", "Lots of people, cars and buildings"],
                "options": ["visual"],
                "conversation_option": "semantic",
                "name": "Urban"
            },
            {
                "prompts": ["This video is taken in a suburban enviorment", "There should be buildings, roads", "Everything should be a lot more spread out", "The majority of the space should be developed"],
                "options": ["visual"],
                "conversation_option": "semantic",
                "name": "Suburban"
            },
            {
                "prompts": ["This video was taken in a rural enviorment", "There shouldn't be a ton of human development", "Buildings should be extremly spread out", "Should mostly be nature", "Very few humans around"],
                "options": ["visual"],
                "conversation_option": "semantic",
                "name": "Rural"
            }
        ],
        "video_ids": [id]
    }
    headers = {
        "accept": "application/json",
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(classify_url, json=payload, headers=headers)
    response = response.json()
    
    print(response, file=sys.stderr)
    video_class = response['data'][0]['classes'][0]['name']

    payload = { "metadata": { "Location Type": video_class } }
    headers = {
        "accept": "application/json",
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.put(meta_url, json=payload, headers=headers)

def get_video_list(API_KEY):
    retrieve_url = url = f"{API_URL}/indexes/{INDEX_ID}/videos/"
    headers = {
        "accept": "application/json",
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.get(retrieve_url, headers=headers)

    return response.json()['data']

def Get_Video_Metadata(video_id, API_KEY):
    url = f"{API_URL}/indexes/{INDEX_ID}/videos/{video_id}"

    headers = {
        "accept": "application/json",
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    return response.json()['metadata']
