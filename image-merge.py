#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 13:29:39 2020

@author: user
"""

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import numpy as np
import pandas as pd
from io import BytesIO
import requests

file = 'in.xlsx'

# Load spreadsheet
xl = pd.ExcelFile(file)
df = xl.parse('Sheet1')

count_row = df.shape[0]

WIDTH = 600
HEIGHT = 600

imgs = []
for i in range(0, count_row):
  response = requests.get(df['image'][i])
  img = Image.open(BytesIO(response.content))
  img = img.resize((WIDTH, HEIGHT))
  draw = ImageDraw.Draw(img)
  font = ImageFont.truetype("sans-serif.ttf", 40)
  msg = df['text'][i]
  w, h = draw.textsize(msg, font=font)
  draw.text(((WIDTH-w)/2, 50 ), msg, fill="black", font=font)
  imgs.append(img)


imgs_horizontal = []
for i in range(1, int(count_row/3) + 1):
  imgs_vertical = np.vstack([imgs[1+i], imgs[2+i], imgs[3+i]])
  imgs_vertical = Image.fromarray(imgs_vertical)

  imgs_horizontal.append(imgs_vertical)


imgs_horizontal = np.hstack(imgs_horizontal)
imgs_horizontal = Image.fromarray(imgs_horizontal)


imgs_horizontal.save('out.jpg')