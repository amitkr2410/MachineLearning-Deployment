#Code to process the input image file and use the ML model to predict the status of tumor:
#import numpy as np
import torch
from torch import nn
from torch import optim
from torchvision import datasets, transforms, models
import src.model as model_script
# from pathlib import Path
import os
import PIL

# Function for preprocessing the input image
def Transform_Image(input_image):
    test_predict_transforms = transforms.Compose([transforms.Resize((7*32,7*32)),
                                            transforms.ToTensor(),
                                            transforms.Normalize([0.5, 0.5, 0.5],
                                                                 [0.3, 0.3, 0.3])])

    pil_input_image = PIL.Image.open(input_image, mode='r').convert('RGB')
    image = test_predict_transforms(pil_input_image)
    return image
# Function to evaluate the model for the given input image
def Make_prediction(model, input_image, device):
    model.eval() #De-activates dropout, batchnormalization layers
    #Since the model expects an input with 4 dimension 
    # .. which corresponds to BxCxHxW =(Batch x Channel X Height X Width) 
    # ..we need to add one more dimension. As we are testing with one image, we are missing
    # ..the Batch (B) dimension
    # To solve this, we can add this dimension by using unsqueeze
    valid_image = input_image.unsqueeze(0) 
    valid_image = valid_image.to(device)
    print('image:' , type(valid_image), valid_image)
    outputs = model.forward(valid_image)
    print(outputs)
    outputs_class = torch.argmax(outputs, dim=1)
    outputs_class = outputs_class.item() #Convert torch tensor into scalar number
    #outputs_class =0
    return outputs_class

def main_predict(ImageName, model_name):
    print('######### Start of prediction step ##### ')
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print('Device is ', device)
    cwd = os.getcwd()
    if model_name == 'vgg16_pretrained_false':
        model_filename = cwd + '/final_model/vgg16_pretrained_false_Run49.pth'
    if model_name == 'cnn_4layers_custom':
        model_filename = cwd + '/final_model/cnn_4layers_results_Run21.pth'
    if model_name == 'cnn_with_attention':
        model_filename = cwd + '/final_model/cnn_with_attention_Run101.pth'
    if model_name == 'only_attention':
        model_filename = cwd + '/final_model/only_attention_Run151.pth'

    #model_filename = cwd + '/final_model/only_attention_Run151.pth'
    #input_image_name = cwd + '/data/test/yes/y0.jpg'

    input_image_name = cwd + '/static/cnn_image/' + ImageName + '.jpg'
    input_image_name2 = '/static/cnn_image/' + ImageName + '.jpg'
    
    num_classes=2
    #model_name='only_attention'
    model = model_script.get_model(model_name, num_classes)
    model.to(device)
    model.eval()
    if torch.cuda.is_available() :    
        model.load_state_dict(torch.load(model_filename))
    else:
        model.load_state_dict(torch.load(model_filename,map_location=torch.device('cpu')))

    #print('amit: the model is ', str(model))
    model_details_string = str(model ).replace('\n', ' <br> ')
    input_image = Transform_Image(input_image_name)
    ans_class = Make_prediction(model, input_image, device)
    #print('The input image corresponds to the following class:', ans_class)
    ans ='yes'
    if ans_class==0:
        ans = 'no'
    print('######### End of evaluation step ##### ')
    return input_image_name2, model_details_string, ans
