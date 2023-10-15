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
        api_key = fp.read()

    INDEX_ID = "652b15403c4a426cf3f4f61c"
    API_URL = "https://api.twelvelabs.io/v1.2"

    data = {
        "query": query,
        "index_id": INDEX_ID,
        "search_options": ["visual"],
    }

    response = requests.post(f"{API_URL}/search", headers={"x-api-key": api_key}, json=data)


    results = []

    # Getting thumbnail and relevant data
    for i in range(len(response.json()['data'])):
        score = response.json()['data'][i]['score']
        video_id = response.json()['data'][i]['video_id']
        thumbnail_url = response.json()['data'][i]['thumbnail_url']
        results.append({"score": score, "video_id": video_id, "thumbnail_url": thumbnail_url})

    return results
