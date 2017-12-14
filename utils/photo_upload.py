import requests
import shutil
import uuid
import os

def photo(picture_url, client, task_id):
    print "entered photo"

    print "before post"
    picture_url = picture_url.encode('ascii', 'ignore')
    req = requests.post('https://api.deepai.org/api/colorizer',
                     headers={'api-key': '2abb59e6-e201-424a-b136-e1a6c07a9579'}, data={'image': picture_url})
    print req.json()
    response = req.json()
    # print response
    colour_url = response["output_url"]
    # return {"status":200}


    response = requests.get(colour_url, stream=True)
    unique_id = uuid.uuid1()
    unique_id = str(unique_id).split('-')[0]
    file_name = "file_" + unique_id + '.jpg'
    with open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    client.upload_file(file_name, 'do-hack', 'photo_upload/' + file_name)
    url = client.generate_presigned_url(ClientMethod='get_object',
                                        Params={'Bucket': 'do-hack',
                                                'Key': 'photo_upload/' + file_name},
                                        ExpiresIn=3600)
    r = requests.post('http://localhost:8000/api/v1/colourized_url', data={'url': url, 'task_id': task_id})
    print "posted"
    os.remove(file_name)
    return {"file_name": file_name}
