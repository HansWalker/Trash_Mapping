import cv2
import sys
import os
sys.path.insert(0, os.path.abspath('./detectron2'))
import numpy as np
import base64
from io import BytesIO
import tempfile
from roboflow import Roboflow
import os, shutil

def segment_video(file_name, API_KEY):
    print(file_name, file=sys.stderr)
    

    folder = 'temp'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    save_video(file_name)

    rf = Roboflow(api_key=API_KEY)
    project = rf.workspace("trash-detection-eka7g").project("aeriel-trash-detection")
    model = project.version('5').model
    i=0
    trash_amount = 0
    for path in os.listdir('temp'):
        pred = model.predict('temp/'+path, confidence=10, overlap=30).json()
        trash_amount += len(pred['predictions'])
        i+=1
    average_trash = trash_amount/i

    distance = ((i *3/(30*60)*5280/3)**(1/2))/(2*5280)

    if(file_name=='videos/IMG_6505.MOV'):
        lat= 37.487126764972146
        long = -122.22740600563932
    if(file_name=='videos/IMG_6506.MOV'):
        lat= 37.48685008465837
        long = -122.2219611213012
    if(file_name=='videos/IMG_6507.MOV'):
        lat= 37.48719694795838
        long = -122.23396634356635
    if(file_name=='videos/IMG_6508.MOV'):
        lat= 37.48509109970707
        long = -122.23295475236165
    if(file_name=='videos/IMG_6509.MOV'):
        lat= 37.484951308891674
        long = -122.23113531801874

    #append to the file trash_locations.txt
    with open('trash_locations.txt', 'a') as fp:
        fp.write('\n'+str(lat)+' '+str(long)+ ' ' + str(distance)+' '+str(average_trash))
    




    
def save_video(file_name):
    video_filename = file_name
    
    cap = cv2.VideoCapture(video_filename)

    # Check if video file exists
    if not os.path.exists(video_filename):
        print("File does not exist or wrong path provided.")
        exit()

    # Check if temp directory exists, if not, create it
    if not os.path.exists("temp"):
        os.mkdir("temp")

    # Open the video file
    cap = cv2.VideoCapture(video_filename)

    if not cap.isOpened():
        print("Error: Couldn't open the video file.")
        exit()

    frame_count = 0
    img_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1

        if frame_count % 30 == 0:
            img_count += 1
            img_filename = os.path.join("temp", f"frame_{img_count}.jpg")
            cv2.imwrite(img_filename, frame)

    cap.release()

def frames_to_video_file(frames, save_path, frame_rate=30.0):
    if not frames:
        raise ValueError("The frames list is empty!")

    height, width, layers = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(save_path, fourcc, frame_rate, (width, height), isColor=True)

    for frame in frames:
        out.write(frame)
    out.release()

def base64_to_cv2_video(base64_video):
    video_binary = base64.b64decode(base64_video)

    with tempfile.NamedTemporaryFile(delete=True, suffix=".mp4") as temp_video_file:
        temp_video_file.write(video_binary)
        temp_video_file.flush()

        cap = cv2.VideoCapture(temp_video_file.name)
        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)

        cap.release()

    return frames