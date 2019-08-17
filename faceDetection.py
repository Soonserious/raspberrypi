# -*- coding: utf-8 -*-
"""
Created on Thu May 16 23:21:57 2019

@author: GatsbyHairWax
"""

from PIL import Image
import os, glob, numpy as np
from keras.models import load_model
import sys

import tensorflow as tf

seed = 5
tf.set_random_seed(seed)
np.random.seed(seed)

#caltech_dir = './test_imgs'


image_w = 224
image_h = 224

pixels = image_h * image_w * 3

X = []
filenames = []
print(sys.argv[1])
files = glob.glob(sys.argv[1])
for i, f in enumerate(files):
    img = Image.open(f)
    img = img.convert("RGB")
    img = img.resize((image_w, image_h))
    data = np.asarray(img)

    filenames.append(f)
    X.append(data)



X = np.array(X)
X = X.astype(float) / 255
model = load_model('./model/aa.h5')

print(model.predict(X))

prediction = model.predict(X)

print("aisdlfjalsdf")

#print(type(prediction))
#print(prediction.shape)




#print(prediction)


np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})
cnt = 0
#flag = 0 1
flag = 0
for i in prediction:
    print(i)
    if i >= 0.6:
        print("뒤집어진 상태입니다.")
        flag = 1
    else :
        print("앞모습 상태입니다.")
    cnt += 1
    
if flag == 1:
    sys.stdout.write("1")
else :
    sys.stdout.write("0")

#cnt = 0
#for i in prediction:
 #   print(i)
  #  if i>=0.6: sys.stdout.write("1")
   # else : sys.stdout.wirte("0")
    #cnt +=1


#sys.stdout.write('1')

#''' + filenames[cnt].split("\\")[2]  +'''
#''' + filenames[cnt].split("\\")[2] +'''
    
