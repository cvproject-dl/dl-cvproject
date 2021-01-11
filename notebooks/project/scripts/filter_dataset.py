# -*- coding: utf-8 -*-
"""combine_dataset.ipynb

Automatically generated by Colaboratory.

"""

import torch
import torch.nn as nn
from torchvision import transforms, models
import os
from shutil import copy
from PIL import Image

def car_ex(result):
  tensr = result.xyxy[0]
  output = dict()
  listofpredictions = list()
  cars = 0
  for detection in tensr:
      coordinates = []
      if int(detection[-1]) == 2 or int(detection[-1]) == 7:
          return True
  return False

def get_results(fileloc):
    img = Image.open(fileloc)
    yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    yolo_model.autoshape()
    yolo_model.cuda()
    imgs = [img]
    result = yolo_model(imgs, size=700)
    return car_ex(result)

STANFORD_PATH = '/content/drive/MyDrive/kaggle/car_data/car_data'
SF_TEST = os.path.join(STANFORD_PATH,'test')
SF_TRAIN = os.path.join(STANFORD_PATH,'train')

IND_PATH  = '/content/drive/MyDrive/Indcars'
IND_TEST = os.path.join(IND_PATH,'test')
IND_TRAIN = os.path.join(IND_PATH,'train')

NEW_DATA = '/content/drive/MyDrive/newdata'
NEW_TEST = os.path.join(NEW_DATA,'test')
NEW_TRAIN = os.path.join(NEW_DATA,'train')

IND_CAR_LIST = os.listdir(IND_TEST)
INDCARS = IND_CAR_LIST.copy()
for car in IND_CAR_LIST:
  if 'Audi' in car or 'BMW' in car:
    INDCARS.remove(car)

for car in INDCARS:
  cars = os.listdir(os.path.join(IND_TEST,car))
  dest_path = os.path.join(NEW_TEST,car)
  try:
    os.mkdir(dest_path)
  except:
    continue
  for c in cars:
    car_path = os.path.join(IND_TEST,car,c)
    print(car_path)
    if get_results(car_path):
      copy(car_path,dest_path)

for car in INDCARS:
  cars = os.listdir(os.path.join(IND_TRAIN,car))
  dest_path = os.path.join(NEW_TRAIN,car)
  try:
    os.mkdir(dest_path)
  except:
    pass
  for c in cars:
    car_path = os.path.join(IND_TRAIN,car,c)
    print(car_path)
    if get_results(car_path):
      copy(car_path,dest_path)

