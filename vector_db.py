'''def vector_db_search(search_query):
    return "videos\Viva_La_Vida.mp4"'''
import pybase64 as base64
import os

def vector_db_search(video_path):
    video_path = 'videos/Viva_La_Vida.mp4'
    try:
        with open(video_path, 'rb') as video_file:
            video_data = video_file.read()
            # Encode the video data to base64
            video_base64 = base64.b64encode(video_data).decode('utf-8')
            return video_base64
    except Exception as e:
        print(f"Error loading video: {str(e)}")
        return None
