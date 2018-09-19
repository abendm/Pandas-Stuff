import flask
app = flask.Flask(__name__)

#-------- MODEL GOES HERE -----------#
import pickle

with open('titanic_rfc.pkl', 'rb') as picklefile:
    PREDICTOR = pickle.load(picklefile)


import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB






#-------- ROUTES GO HERE -----------#


@app.route('/predict', methods=["GET"])
def predict():
    pclass = flask.request.args['pclass']
    sex = flask.request.args['sex']
    age = flask.request.args['age']
    fare = flask.request.args['fare']
    sibsp = flask.request.args['sibsp']

    item = np.array([pclass, sex, age, fare, sibsp]).reshape(-1,5)

    score = PREDICTOR.predict_proba(item)
    results = {'survival chances': score[0,1], 'death chances': score[0,0]}
    return flask.jsonify(results)

# This method takes input via an HTML page
@app.route('/page')
def page():
   with open("page.html", 'r') as viz_file:
       return viz_file.read()

@app.route('/result', methods=['POST', 'GET'])
def result():
    '''Gets prediction using the HTML form'''
    if flask.request.method == 'POST':

       inputs = flask.request.form

       pclass = inputs['pclass'][0]
       sex = inputs['sex'][0]
       age = inputs['age'][0]
       fare = inputs['fare'][0]
       sibsp = inputs['sibsp'][0]

       item = np.array([pclass, sex, age, fare, sibsp]).reshape(-1,5)
       score = PREDICTOR.predict_proba(item)
       results = {'survival chances': score[0,1], 'death chances': score[0,0]}
       return flask.jsonify(results)



if __name__ == '__main__':

    HOST = '127.0.0.1'
    PORT = 4000
    app.run(HOST, PORT)
