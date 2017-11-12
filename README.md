# CAAS
Colorization As A Service

## What are we building?
Image and video restoration is a large industry. Image restoration in particular has 150 years of data that needs processing. In video restoration, years of old black and white movies have not been viewed by younger generations. CAAS aims to solve that using deep neural net libraries. Referring to [this](https://github.com/junyanz/interactive-deep-colorization) paper, we've built an infrastructure for colorizing old content.

## How does it work?
On our dashboard, we upload images and videos, which are then broken into frames. Each frame is run through the deep colorization library to produce colored frames. In case of an image, this frame is returned, for a video, these frames are merged together to re-contruct the movie

## CAAS vs Human Effort
Running CAAS at a concurrency of 8, it can colorize a 3 hour movie in 22 hours. Compare this with 3,65,000 hours required to colorize Mughal-e-Azam. As mentioned in the deep colorization paper, it is possible to add user inputs to enhance the output of the neural net. Given a few specialists re-color the output given by CAAS through their color inputs, we're still looking at a max of one week. The cognitive and compute efficiencies CAAS provides is simply too high to ignore

## Code Samples
```python
def photo(picture_url, client, task_id):
  req = requests.post('https://api.deepai.org/api/colorizer',
                     headers={'api-key': 'API-KEY'}, data={'image': picture_url})
  colour_url = response["output_url"]
  
def video(url, client, task_id):
  cap = cv2.VideoCapture("logan480.mp4")
  success, image = cap.read()
  count = 0
    success = True
    while success:
        success, image = cap.read()
        cv2.imwrite("frame%d.jpg" % count, image)
        count += 1
        if count == 300:
            success = False
  colorize_frames()
  make_vid()
```
