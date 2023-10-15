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
headers = {
    "accept": "application/json",
    "x-api-key": API_KEY,
    "Content-Type": "application/json"}
    
data = {
"query": "plastic",
"threshold": "high",
"search_options": ["conversation"],
"filter": { "id": ["652b199c43e8c47e4eb48083"] },
"index_id": INDEX_ID }


response = requests.post(f"{API_URL}/search", headers=headers, json=data)

print(response.json())
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


'''url = "https://api.twelvelabs.io/v1.1/indexes/652b15403c4a426cf3f4f61c/videos/652b199c43e8c47e4eb48083"

headers = {
    "accept": "application/json",
    "x-api-key": "tlk_1C43Q5J273MHH1223XMER1AEJW3J",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)'''
print(response.json()  )