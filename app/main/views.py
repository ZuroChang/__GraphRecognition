# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:27:47 2020

@author: ZuroChang
"""


import cv2
#import os
import numpy as np
from datetime import datetime

from flask import render_template,redirect,url_for,jsonify, send_from_directory
from flask import request,session,g
from . import main
from .forms import NameForm, UploadForm, SmoothForm, ExbedAxesForm
from werkzeug.utils import secure_filename

from .Config import FolderPath 
# from .. import db
# from ..models import User
from .Package_Parser import CurveRecognize, LockCurve, PadPixel, EmbedAxes


@main.route('/', methods=['GET','POST'])
def index():
    form=NameForm()
    if form.validate_on_submit():
        session['name']=form.name.data
        return redirect(url_for('.index'))
    
    return(
        render_template('index.html',form=form,name=session.get('name'))
    )


@main.route('/Recognise', methods=['GET','POST'])
def Recognise():
    Uploadform=UploadForm()
    Smoothform=SmoothForm()
    ExbedAxesform=ExbedAxesForm()
    
    if request.method=='GET':
        session['HSV']={"Hue":"0","Saturation":"0","Value":"0"}

        session['Picture']={
            'PaddingPixel':FolderPath._Import+'PaddingPixel.PNG',
            'Filter':FolderPath._Import+'Filter.PNG'
        }
        
        session['Location']={
            'Img':"/static/test.jpg",
            'Recognise':"/static/test.jpg",
            'Smooth':"/static/test.jpg"
        }
        
        session['Flag']={
            'Upload':False,
            'Smooth':False
        }
        
        return(
            render_template('Recognise.html',
                Uploadform=Uploadform,
                Smoothform=Smoothform,
                ExbedAxesform=ExbedAxesform,
                ImgLocation=session['Location']['Img'],
                RecogniseLocation=session['Location']['Recognise'],
                SmoothLocation=session['Location']['Smooth']
            )
        )
    if Uploadform.validate_on_submit() and Uploadform.submit_Upload.data:
        File=Uploadform.File.data
        FileName=secure_filename(File.filename)
        File.save(FolderPath._Import+FileName)
        
        session['Source']=FileName
        
        session['Location']={
            'Img':"/static/_Import/"+FileName,
            'Recognise':"/static/test.jpg",
            'Smooth':"/static/test.jpg"
        }
        
        session['Flag']={
            'Upload':True,
            'Smooth':False
        }
        
        return(
            render_template('Recognise.html',
                Uploadform=Uploadform,
                Smoothform=Smoothform,
                ExbedAxesform=ExbedAxesform,
                ImgLocation=session['Location']['Img'],
                RecogniseLocation=session['Location']['Recognise'],
                SmoothLocation=session['Location']['Smooth']
            )
        )
        
    if Smoothform.validate_on_submit() and Smoothform.submit_Smooth.data:
        LockFilter=LockCurve(Image=cv2.imread(session['Picture']['Filter']))
        
        PaddingPixel=PadPixel(Image=LockFilter,
            Magnifier=Smoothform.Magnifier.data,
            Kernel=np.ones((Smoothform.Kernel.data,Smoothform.Kernel.data),np.uint8),
            Iterations=Smoothform.Iterations.data
        )
        cv2.imwrite(session['Picture']['PaddingPixel'],PaddingPixel)
        
        
        Period=[20000101,20201231]
        Value=[1,LockFilter.shape[1]]
        Series=EmbedAxes(Image=LockFilter,Period=Period,Value=Value)
        SmoothSeries=EmbedAxes(Image=PaddingPixel,Period=Period,Value=Value)
        
        OutputSeries=Series['DataFrame'].merge(SmoothSeries['DataFrame'],on='Date',how='left')
        OutputSeries=OutputSeries.rename(columns={"Value_x":"PreSmooth","Value_y":"Smooth"})
        ax=OutputSeries.plot()
        fig=ax.get_figure()
        fig.savefig(FolderPath._Import+'Smoothing.png')
        
       
        
        session['Location']={
            'Img':"/static/_Import/"+session['Source'],
            'Recognise':"/static/_Import/Filter.png?{}".format(np.random.uniform()),
            'Smooth':"/static/_Import/Smoothing.png?{}".format(np.random.uniform())
        }
        
        session['Flag']={
            'Upload':True,
            'Smooth':True
        }
        
        return(
            render_template('Recognise.html',
                Uploadform=Uploadform,
                Smoothform=Smoothform,
                ExbedAxesform=ExbedAxesform,
                ImgLocation=session['Location']['Img'],
                RecogniseLocation=session['Location']['Recognise'],
                SmoothLocation=session['Location']['Smooth']
            )
        )
        
    if ExbedAxesform.validate_on_submit() and ExbedAxesform.submit_Exbed.data\
        and session['Flag']['Smooth']:
            
        Period=[ExbedAxesform.X_Start.data,ExbedAxesform.X_End.data]
        Value=[ExbedAxesform.Y_Start.data,ExbedAxesform.Y_End.data]
        
        Series=EmbedAxes(Image=LockCurve(Image=cv2.imread(session['Picture']['Filter'])),
            Period=Period,Value=Value)
        SmoothSeries=EmbedAxes(Image=cv2.imread(session['Picture']['PaddingPixel']),
            Period=Period,Value=Value)
        
        OutputSeries=Series['DataFrame'].merge(SmoothSeries['DataFrame'],on='Date',how='left')
        OutputSeries=OutputSeries.rename(columns={"Value_x":"PreSmooth","Value_y":"PostSmooth"})
        OutputSeries.to_excel(FolderPath._Import+'Series.xlsx',index=False)
        
        return send_from_directory(
            directory=FolderPath._Import,
            filename='Series.xlsx',
            as_attachment=True
        )
    if request.method=='POST' and session['Flag']['Upload']:
        def getIndicatorLocation(Form):
            posLeft=float(Form['posLeft'])
            posTop=float(Form['posTop'])
            picLeft=float(Form['picLeft'])
            picTop=float(Form['picTop'])
            picWidth=float(Form['picWidth'])
            picHeight=float(Form['picHeight'])
            
            return({'Row':(posTop-picTop)/picHeight,
                    'Col':(posLeft-picLeft)/picWidth})
        
        def getHSV(Image,Location):
            HSV=cv2.cvtColor(Image,cv2.COLOR_BGR2HSV)
            Row=round(Image.shape[0]*Location['Row'])
            Column=round(Image.shape[1]*Location['Col'])
            
            return(HSV[Row][Column])
       
        Image=cv2.imread(FolderPath._Import+session['Source'])
        
        IndicatorLocation=getIndicatorLocation(request.form)
        HSV=getHSV(Image,IndicatorLocation)
        
        Tolarence=0
        Filter=CurveRecognize(
            Image=Image,
            Hue=[max(0,HSV[0]-Tolarence),min(HSV[0]+Tolarence,255)],
            Saturation=[max(0,HSV[1]-Tolarence),min(HSV[1]+Tolarence,255)],
            Value=[max(0,HSV[2]-Tolarence),min(HSV[2]+Tolarence,255)],
            GrayFlag=1
        )
        cv2.imwrite(session['Picture']['Filter'],Filter)
        
        session['HSV']={
            "Hue":str(HSV[0]),
            "Saturation":str(HSV[1]),
            "Value":str(HSV[2])
        }
        
        return jsonify(session['HSV'])
    


