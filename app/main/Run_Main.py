# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 14:10:36 2020

@author: ZuroChang
"""


import cv2
import numpy as np
import json

import Package_Parser as Parser
from Config import FolderPath as FP

FP._Output="F:/Project/NTU_2020Semester01/GraphRecognization/app/static/_Output/"
Image=cv2.imread("F:/Project/NTU_2020Semester01/GraphRecognization/app/static/_Import/"+'SP500.PNG')

Hue=[0,30]
Saturation=[200,255]
Value=[200,255]

Filter=Parser.CurveRecognize(
    Image=Image,
    Hue=Hue,
    Saturation=Saturation,
    Value=Value,
    GrayFlag=1
)
cv2.imwrite(FP._Output+'Filter.PNG',Filter)

Location=[200,0]
Shape=[100,625]

ErasedFilter=Parser.Eraser(
    Image=Filter,
    Location=Location,
    Shape=Shape
)
cv2.imwrite(FP._Output+'ErasedFilter.PNG',ErasedFilter)


LockFilter=Parser.LockCurve(Image=ErasedFilter)
cv2.imwrite(FP._Output+'LockFilter.PNG',LockFilter)


Magnifier=2
Kernel=(10,10)
Iterations=10

PaddingPixel=Parser.PadPixel(Image=LockFilter,
    Magnifier=Magnifier,
    Kernel=np.ones(Kernel,np.uint8),
    Iterations=Iterations
)
cv2.imwrite(FP._Output+'PaddingPixel.PNG',PaddingPixel)


Period=[20161021,20201020]
Value=[1500,3500]

Series=Parser.EmbedAxes(
    Image=LockFilter,
    Period=Period,
    Value=Value,
)
Series['DataFrame'].to_csv(FP._Output+'Series.csv',index=0)
with open(FP._Output+'Series.json','w') as f:
    json.dump(Series['json'],f)

SmoothSeries=Parser.EmbedAxes(
    Image=PaddingPixel,
    Period=Period,
    Value=Value,
)

SmoothSeries['DataFrame'].to_csv(FP._Output+'SmoothSeries.csv',index=0)
with open(FP._Output+'SmoothSeries.json','w') as f:
    json.dump(SmoothSeries['json'],f)

