import pickle
import os
import sys
from flask import Flask, render_template, request, jsonify
from joblib import load 
import src.custom_function as customfunc

##Create flaskAPI instance
app = Flask(__name__)

@app.route('/',)
def welcome():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']  
    ans = NLP_twitter_sentiment(text)
    variableinput = "The input message was : "+ text
    return(render_template('index.html', variableinput=text,  variableoutput=ans))

# ''' 
##Load saved model pickle files
filename = 'preprocess/CountVectorizer.pickle'
vectorizer = pickle.load( open(filename,'rb') )

filename = 'eval/finalmodel.pickle'
classifier = pickle.load( open(filename,'rb') )

##### find the result for a given test sms
def predict_result(MyTwitterMessage):
    sms = [customfunc.text_process(MyTwitterMessage)]
    x_sms = vectorizer.transform(sms)
    ans = classifier.predict(x_sms)
    if ans ==-1:
        output = 'The message is Negative'
    if ans == 0:
        output = 'The message is Neutral'
    if ans == 1:
        output ='The message is Positive'
    print(output)
    return output 
#####

def NLP_twitter_sentiment(text):
    pred=text
    print('Amit The entered text is ', text)
    pred=predict_result(text)
    print('Amit The sentiment is ', pred)
    return pred 
# ''' 



if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=9000)
    

