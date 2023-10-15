import pprint
import requests

# Declare the `headers` dictionary containing your API key
headers = {
    "x-api-key": "tlk_1C43Q5J273MHH1223XMER1AEJW3J"
}

INDEX_NAME = "trash"
API_KEY = "tlk_1C43Q5J273MHH1223XMER1AEJW3J"
API_URL = "https://api.twelvelabs.io/v1.2"
INDEX_ID = "652b15403c4a426cf3f4f61c"
INDEXES_URL = f"{API_URL}/indexes"
SEARCH_URL = f"{API_URL}/search"
data = {
    "query": "plastic trash",
    "index_id": INDEX_ID,
    "search_options": ["visual"],
}

response = requests.post(SEARCH_URL, headers={"x-api-key": API_KEY}, json=data)
total_count = response.json()['search_pool']['total_count']
'''results = []

# Getting thumbnail and relevant data
print(len(response.json()['data']))
for i in range(total_count):
    print(i)
    score = response.json()['data'][i]['score']
    video_id = response.json()['data'][i]['video_id']
    thumbnail_url = response.json()['data'][i]['thumbnail_url']
    results.append({"score": score, "video_id": video_id, "thumbnail_url": thumbnail_url})
print(results)

#response2 = requests.get("/v1.1/indexes/index_id/videos/video_id/thumbnail", headers={"x-api-key": API_KEY})
print (f"Status code: {response.status_code}")
print (response.json())'''