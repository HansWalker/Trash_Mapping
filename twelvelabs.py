import requests
import os
def search_trash(query):
    # Check if api key file exists
    if not os.path.exists('api_key.txt'):
        print("Error: api_key.txt not found")
        with open('api_key.txt', 'w') as fp:
            pass
        return None

    # Check if api key file is empty
    if os.stat("api_key.txt").st_size == 0:
        print("Error: api_key.txt is empty")
        return None

    # Read api key from file
    with open('api_key.txt', 'r') as fp:
        API_KEY = fp.read()

    INDEX_ID = "652b15403c4a426cf3f4f61c"
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

def search_video_single(video_id,query):
    # Check if api key file exists
    if not os.path.exists('api_key.txt'):
        print("Error: api_key.txt not found")
        with open('api_key.txt', 'w') as fp:
            pass
        return None

    # Check if api key file is empty
    if os.stat("api_key.txt").st_size == 0:
        print("Error: api_key.txt is empty")
        return None

    # Read api key from file
    with open('api_key.txt', 'r') as fp:
        API_KEY = fp.read()

    INDEX_ID = "652b15403c4a426cf3f4f61c"
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


def upload_video(file_path):
    file_path = 'videos/'+file_path
     # Check if api key file exists
    if not os.path.exists('api_key.txt'):
        print("Error: api_key.txt not found")
        with open('api_key.txt', 'w') as fp:
            pass
        return None

    # Check if api key file is empty
    if os.stat("api_key.txt").st_size == 0:
        print("Error: api_key.txt is empty")
        return None

    # Read api key from file
    with open('api_key.txt', 'r') as fp:
        API_KEY = fp.read()

    API_URL = "https://api.twelvelabs.io/v1.2"
    TASKS_URL = f"{API_URL}/tasks"
    file_stream = open(file_path,"rb")
    INDEX_ID = "652b15403c4a426cf3f4f61c"

    data = {
    "index_id": INDEX_ID, 
    "language": "en"}
    file_param = [
        ("video_file", (os.path.splitext(file_path)[0], file_stream, "application/octet-stream"))]
    
    response = requests.post(TASKS_URL, headers={"x-api-key": API_KEY}, data=data, files=file_param)

    return response.json()['_id']