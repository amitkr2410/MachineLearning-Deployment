#Flask application with serverless_wsgi: a Serverless Framework plugin 
# It's primary function is to host serverless application
# In this code, we integrate Flask app with html and css elements together
# to  create aesthetically beautiful application
import os, sys
#import numpy as np
from flask import Flask, render_template, request, jsonify
import serverless_wsgi
import src.eval as pr_cnn

HOME = os.path.abspath(".")

##Create flaskAPI instance
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.pdf']

#BrainImagesList=['Test1_yes','Test2_yes','Test3_no', 'Test4_no', 'Test5_no']
#NNModelList=['vgg16_pretrained_false', 'cnn_4layers_custom', 'cnn_with_attention', 'only_attention']

@app.route('/',)
def welcome():
    #return render_template('index.html', BrainImagesList=BrainImagesList, NNModelList=NNModelList)
    return render_template('index.html')
                          

@app.route('/', methods=['POST'])
def my_form_post():

    if "submit_cnn" in request.form:
        ImageName = request.form.get('select_cnn_image')
        ModelName = request.form.get('select_cnn_model')

        cnn_image_file, model_details_string, ans = pr_cnn.main_predict(ImageName, ModelName)
        
        print('Amit: output ans is ', ans, ', and image name:', cnn_image_file, "\n", ModelName)
        
        return(render_template('index.html', 
                               variableinputBT=cnn_image_file,
                               variablemodeldetails=model_details_string, 
                                 variableoutputBT=ans
                                     ))


# ''' 
#for AWS Lambda handler function
def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)

#if __name__ == "__main__":
#     app.run( debug=True)
#    app.run(host='0.0.0.0', port=5000, debug=True)


