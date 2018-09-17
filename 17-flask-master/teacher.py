import flask
app = flask.Flask(__name__)

#This is our model
import pandas as pd 
import numpy as np 
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy 
from spacy import displacy

nlp = spacy.load('en')


@app.route('/page')
def page():
   with open("page2.html", 'r') as viz_file:
       return viz_file.read()

@app.route('/result', methods=['POST', 'GET'])
def result():
    '''Gets prediction using the HTML form'''
    if flask.request.method == 'POST':

       inputs = flask.request.form

       subject = inputs['subject'][0]
       comments = inputs['comments'][0]
       doc = nlp(comments)
       ren = displacy.render(doc, style='ent')
	   return comments