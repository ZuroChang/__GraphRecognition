# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 13:59:12 2020

@author: ZuroChang
"""


import cv2
import numpy as np
import pandas as pd

# Location=[0.25666666666666665,0.8633333333333333]
# Image=cv2.imread('F:/Project/NTU_2020Semester01/GraphRecognization/app/static/_Import/SP500.PNG')
# Hsv=cv2.cvtColor(Image,cv2.COLOR_BGR2HSV)


# Row=round(Image.shape[0]*Location[0])
# Col=round(Image.shape[1]*Location[1])

# ColorHsv=Hsv[Row,Col]
# Color=Image[Row,Col]
# Curve=np.ones([Image.shape[0],Image.shape[1]])*255
# for i in range(Image.shape[0]):
#     for j in range(Image.shape[1]):
#         if not np.array_equal(Image[i][j],Color):
#             Curve[i][j]=0
#         else:
#             print(i,j)



def getColorCode(Image,Location):
    HSV=cv2.cvtColor(Image,cv2.COLOR_BGR2HSV)
    

def Eraser(Image,Location=[250,0],Shape=[30,625]):
    Filter=Image.copy()
    Filter[
        min(Location[0],Filter.shape[0]):min(Location[0]+Shape[0]+1,Filter.shape[0]),
        min(Location[1],Filter.shape[1]):min(Location[1]+Shape[1]+1,Filter.shape[1])
    ]=0
    
    return(Filter)

def CurveRecognize(Image,Hue,Saturation,Value,GrayFlag=1):
    HSV=cv2.cvtColor(Image,cv2.COLOR_BGR2HSV)
    
    LowerBound=np.array([Hue[0],Saturation[0],Value[0]])
    UpperBound=np.array([Hue[1],Saturation[1],Value[1]])
    mask=cv2.inRange(HSV,LowerBound,UpperBound)
    
    Curve=cv2.bitwise_and(Image,Image,mask=mask)
    if GrayFlag:
        Curve=cv2.cvtColor(Curve,cv2.COLOR_BGR2GRAY)
        Curve=np.piecewise(Curve,[Curve<=0,Curve>0],[0,255])
        Curve=Curve.astype('uint8')
        return(Curve)
    else:
        return(Curve)

def LockCurve(Image):
    Location=np.where(Image==255)
    return(
        Image[
            min(Location[0]):max(Location[0])+1,
            min(Location[1]):max(Location[1])+1
        ]
    )

def EmbedAxes(Image,Period,Value):
    def outputAxes(Shape,Period,YRange):
        def GenerateCalenderDays(Period):
            Start=str(Period[0])
            Start=f"{Start[:4]}-{Start[4:6]}-{Start[6:8]}"
            
            End=str(Period[1])
            End=f"{End[:4]}-{End[4:6]}-{End[6:8]}"
            
            DateSeries=[]
            for entry in pd.date_range(Start,End):
                DateSeries.append(entry.strftime("%Y%m%d"))
            
            return(DateSeries)
        
        CalendarDays=GenerateCalenderDays(Period)
        
        return(
            {'Date':[CalendarDays[round(entry/(Shape[1]-1)*(len(CalendarDays)-1))] for entry in range(Shape[1])],
             'Value':[YRange[1]-entry/(Shape[0]-1)*(YRange[1]-YRange[0]) for entry in range(Shape[0])]
            }
        )
       
    def embedAxes(Image,XSeries,YSeries):
        Location=np.where(Image==255)
        
        Transformation={}
        for entry in range(len(Location[1])):
            if XSeries[Location[1][entry]] in Transformation.keys():
                Transformation[XSeries[Location[1][entry]]].append(YSeries[Location[0][entry]])
            else:
                Transformation[XSeries[Location[1][entry]]]=[YSeries[Location[0][entry]]]
        
        return(Transformation)

    Axes=outputAxes(Image.shape,Period,Value)
    Transformation=embedAxes(Image=Image,XSeries=Axes['Date'],YSeries=Axes['Value'])
    Series=[
        {'Date':entry,'Value':np.mean(Transformation[entry])} 
        for entry in sorted(Transformation.keys())
    ]
    
    return({'DataFrame':pd.DataFrame(Series),'json':Series})

def PadPixel(Image,Magnifier,Kernel,Iterations):
    Resize=cv2.resize(Image,dsize=None,fx=Magnifier,fy=Magnifier)
    retval,Resize=cv2.threshold(Resize,0,255,cv2.THRESH_BINARY)
    
    
    Closed=cv2.morphologyEx(Resize,cv2.MORPH_CLOSE, Kernel,iterations=Iterations)
    
    return(cv2.resize(Closed,dsize=None,fx=1/Magnifier,fy=1/Magnifier))