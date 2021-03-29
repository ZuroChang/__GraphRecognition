# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:39:20 2020

@author: ZuroChang
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField #,FileRequired


class NameForm(FlaskForm):
    name=StringField('What is your name?',validators=[DataRequired()])
    submit=SubmitField('Submit')

class UploadForm(FlaskForm):
    File = FileField('')
    submit_Upload=SubmitField('Submit')


class SmoothForm(FlaskForm):
    Magnifier=IntegerField('Magnifier',default=2)
    Kernel=IntegerField('Kernel',default=10)
    Iterations=IntegerField('Iteration',default=3)
    
    submit_Smooth=SubmitField('Smoothing')
    
class ExbedAxesForm(FlaskForm):
    X_Start=IntegerField('Date Start(yyyymmdd):')
    X_End=IntegerField('Date End(yyyymmdd):')
    Y_Start=FloatField('Value Minminum')
    Y_End=FloatField('Value Maximum')
    submit_Exbed=SubmitField('Download')
    