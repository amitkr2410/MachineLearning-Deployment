import pickle
import os
import sys
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from mangum import Mangum
import src.custom_function as customfunc

##Load saved model pickle files
filename = 'preprocess/CountVectorizer.pickle'
vectorizer = pickle.load( open(filename,'rb') )

filename = 'eval/finalmodel.pickle'
classifier = pickle.load( open(filename,'rb') )

##### find the result for a given test sms
def predict_result(MyTwitterMessage):
    #sms = [customfunc.text_process(MyTwitterMessage)]
    #x_sms = vectorizer.transform(sms)
    #ans = classifier.predict(x_sms)
    ans=0
    if ans ==-1:
        output = 'The message is Negative'
    if ans == 0:
        output = 'The message is Neutral'
    if ans == 1:
        output ='The message is Positive'
    print(output)
    return output 
#####

##Create flaskAPI instance
app = FastAPI()
handler=Mangum(app)

@app.get('/')
#def read_root():
#    return {'Hello':'world'}

def NLP_twitter_sentiment(text:str):
    pred=text
    print('The entered text is ', text)
    pred=predict_result(text)
    return JSONResponse( {'The sentiment of the entered text is ':pred} )

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=9000)

