import requests
import shutil
import numpy as np
import os
import cv2

def video(url, client, task_id):

    cap = cv2.VideoCapture("/Users/drstm/Documents/log/logan480.mp4")
    success, image = cap.read()
    count = 0
    success = True
    while success:
        success, image = cap.read()
        print 'Read a new frame: ', success
        cv2.imwrite("frame%d.jpg" % count, image)
        count += 1
        if count == 300:
            success = False

    colorize_frames()
    make_vid()

def colorize_frames():
    count = 0
    while True:
        print count
        r = requests.post(
            "https://api.deepai.org/api/colorizer",
            files={
                'image': open('/Users/drstm/Documents/log/frame' + str(count) + '.jpg', 'rb')
            },
            headers={'api-key': '2abb59e6-e201-424a-b136-e1a6c07a9579'}
        )
        response = r.json()
        colour_url = response["output_url"]
        response = requests.get(colour_url, stream=True)
        file_name = "/Users/drstm/Documents/log/render/file_" + str(count) + '.jpg'
        with open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        count += 1
        if count == 100:
            break

def make_vid():

    def frames_to_video(inputpath, outputpath, fps):
        image_array = []
        files = [f for f in os.listdir(inputpath) if f != ".DS_Store"]
        files.sort(key=lambda x: int(x[5:-4]))
        for i in range(len(files)):
            img = cv2.imread(inputpath + files[i])
            size = (img.shape[1], img.shape[0])
            img = cv2.resize(img, size)
            image_array.append(img)
        fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
        out = cv2.VideoWriter(outputpath, fourcc, fps, size)
        for i in range(len(image_array)):
            out.write(image_array[i])
        out.release()

    inputpath = '/Users/drstm/Documents/log/render/'
    outpath = '/Users/drstm/Documents/log/render/video.mp4'
    fps = 30
    frames_to_video(inputpath, outpath, fps)

def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return local_filename
