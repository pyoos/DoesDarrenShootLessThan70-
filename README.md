# DDS70

Quick ReadMe for KingKulk

A) List of files and information on them
  1. Quickstart.py:
    - This file is kinda useless, I might just remove it in the future
    - but basically it was the start of calling google drive API so that
    -  we could upload/download files from the google drive directly onto our computer.
  2. Googledrive.py:
    - This file is the main result from the Quickstart.py file above
    - basically you can use it to access the files in the DDS70 google drive and 
    - you should be able to download and upload files, it is conviently made
  3. kaggle1.py:
    - This is just a recreation of this kaggle link:
    - https://www.kaggle.com/code/stpeteishii/nba-tracking-by-yolov8#NBA-Tracking-by-YOLOv8
    - Only got through the first part but basically the code so far allows you to embed a video
    - It'll run the model and anntotate the input video and then can convert that original file from mp4 -> GIF
  4. sandbox.py
    - This file is what sam started working on initially to try and start training models via datasets from Roboflow
    - I think initial step here was to make sure object recognition was capable and then extract data in the form
    - of stats or something (you can check gdrive word docs for more info)
  5. real_time_tracking.py
    - File that I was working on, basically opens up your webcam and allows for real time obeject tracking so far
  6. index.html
    - Casual index file for Frontend to complement object_detector.py
    - Basically you can upload a file (right now its only image) and it should be able to
  7. object_detector.py
    - Right now this is just the backend to index file using Flask and Waitress as main hooked to index.html
  8. trainon10kdataset
    - This is the results of training the yolov8n.pt model on player_detect image dataset on roboflow
    - https://universe.roboflow.com/test-datset/player_detect-0spfb/dataset/1#

B) Additional info
  1. Using Roboflow to store and annotate datasets (max is 10k)
  2. Using Yolov8 as the model for object recognition

C) Goals and Objectives

* I think this part is kinda skewed because there is a lot of different things that we could
* individually be working on. Ref:https://docs.google.com/document/d/1pDzYFMRMvZSqZQ3SdJgpTsRecLP3V20EUDLnXgPnRg0/edit
* link should have a list of all of the projects we were thinking about working on.

  1. Image segmentation + Object detection
  2. Real time video capture + Object detection
  3. Extrapolating analysis from videos
  4. Website + iOS app integration
  5. LLM implementation for analysis + feedback
