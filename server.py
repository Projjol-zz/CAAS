import json
import os
import boto3
import uuid
import shutil
import requests

from flask import Flask, request, jsonify
from botocore.client import Config

from utils.photo_upload import photo
from utils.video_upload import video

app = Flask(__name__)


class Switcher(object):
    def dispatch(self, media_type, picture_url, client, task_id):
        """Dispatch method"""
        # prefix the method_name with 'number_' because method names
        # cannot begin with an integer.
        method_name = str(media_type)
        # Get the method from 'self'. Default to a lambda.
        try:
            method = getattr(self, method_name)
        except AttributeError:
            return jsonify({'error': 'no such endpoint'})
        # Call the method as we return it
        return method(picture_url, client, task_id)

    def photo(self, picture_url, client, task_id):
        photo_resp = photo(picture_url, client, task_id)
        return jsonify(photo_resp)

    def video(self, picture_url, client, task_id):
        video_resp = video(picture_url, client, task_id)
        return jsonify(video_resp)


@app.route('/upload', methods=['POST'])
def upload_hook():
    print "entered upload"
    print request.form
    req_data = request.form
    picture_url = req_data["url"]
    media_type = req_data["media"]
    task_id = req_data["task_id"]

    # response = requests.get(picture_url, stream=True)
    # unique_id = uuid.uuid1()
    # unique_id = str(unique_id).split('-')[0]
    # file_name = "file_" + unique_id + '.jpg'
    # with open(file_name, 'wb') as out_file:
    #     shutil.copyfileobj(response.raw, out_file)

    session = boto3.session.Session()
    client = session.client('s3',
                            region_name='nyc3',
                            endpoint_url='https://nyc3.digitaloceanspaces.com',
                            aws_access_key_id='SMNL5ZMKSQTWUCEHG7SN',
                            aws_secret_access_key='YnFIqP6T3BNjNImOHGK8u/hczB/zhiMVNuNlu4BOHpw',
                            config=Config(signature_version='s3'))

    # client.upload_file(file_name, 'do-hack', 'photo_upload/'+file_name)
    switch = Switcher()
    print "dispatched"
    return switch.dispatch(media_type, picture_url, client, task_id)

@app.route('/', methods=['POST'])
def yolo():
    req_data = request.form
    print req_data["s3_url"]
    return jsonify({"status":200})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(host='0.0.0.0', debug=True, port=port)