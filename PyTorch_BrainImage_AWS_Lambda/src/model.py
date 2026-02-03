#PyTorch model definition for VGG16 architectures and 4 layers CNN model:
import torchvision
import torch
import torch.nn as nn
import src.model_attention as model_attention

def get_model(model_name, num_classes) -> nn.Module:
    
    if model_name == 'vgg16_pretrained_true':
        model = get_vgg16_torchvision(model_name, num_classes)

    if model_name == 'vgg16_pretrained_false':
        model = get_vgg16_torchvision(model_name, num_classes)
        
    if model_name == 'vgg16_custom':
        model = get_vgg16_custom(num_classes)
        
    if model_name == 'cnn_4layers_custom':
        model = get_cnn_4layers_custom(num_classes)
        
    if model_name == 'cnn_with_attention' or model_name == 'only_attention' :
        model = model_attention.get_model_with_attention(model_name, num_classes)

    return model

def get_vgg16_torchvision(model_name,num_classes) -> nn.Module:
    if model_name == 'vgg16_pretrained_true':
        model = torchvision.models.vgg16_bn(pretrained=True)
        #file = '/Users/amitkumar/Research/Download_Model'
        #model_file1='/Users/amitkumar/Research/Download_Model/vgg16_bn-6c64b313.pth'
        #model_file2='/Users/amitkumar/Research/Download_Model/vgg16-397923af.pth'
        #model = torch.load(model_file1)
        #from torch_model import Model as mdl
        #model = nn.Module()
        #checkpoint = torch.load(model_file1)
        #model.load_state_dict(checkpoint['model'])
        #model.load_state_dict(checkpoint['check_point'])
        #model.load_state_dict(torch.load(model_file1))
        for param in model.parameters():
            param.requires_grad = False # Freeze all the layers and 
        for param in model.classifier.parameters():
            param.requires_grad = True  # unFreeze all classifier layers for fine tunning 
        model.classifier[6] = nn.Linear(4096, num_classes) #Modify the number of output classes 
    else:
        model = torchvision.models.vgg16_bn(pretrained=False, num_classes=num_classes)
    return model
        
def get_vgg16_custom(num_classes) -> nn.Module:
    model = vgg16_custom(num_classes)
    return model

def get_cnn_4layers_custom( num_classes) -> nn.Module:
    model = cnn_4layers_custom(num_classes)
    return model
    
##################################################################################################
######################## VGG16 model --architecture----#########################################
#################################################################################################
class vgg16_custom(nn.Module):
    def __init__(self, num_classes):
        super(vgg16_custom, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU())
        self.layer2 = nn.Sequential(
            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(), 
            nn.MaxPool2d(kernel_size = 2, stride = 2))
        self.layer3 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU())
        self.layer4 = nn.Sequential(
            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size = 2, stride = 2))
        self.layer5 = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU())
        self.layer6 = nn.Sequential(
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU())
        self.layer7 = nn.Sequential(
            nn.Conv2d(256, 256, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size = 2, stride = 2))
        self.layer8 = nn.Sequential(
            nn.Conv2d(256, 512, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU())
        self.layer9 = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU())
        self.layer10 = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size = 2, stride = 2))
        self.layer11 = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU())
        self.layer12 = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU())
        self.layer13 = nn.Sequential(
            nn.Conv2d(512, 512, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size = 2, stride = 2))

        self.adaptivepool = torch.nn.AdaptiveAvgPool2d(output_size=(7,7))
        
        self.fc1 = nn.Sequential(
            nn.Linear(7*7*512, 4096),
            nn.ReLU(),
            nn.Dropout(0.5))     
        self.fc2 = nn.Sequential(
            nn.Linear(4096, 4096),
            nn.ReLU(),
            nn.Dropout(0.5))
        self.fc3= nn.Sequential(
            nn.Linear(4096, num_classes))
        
    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = self.layer5(out)
        out = self.layer6(out)
        out = self.layer7(out)
        out = self.layer8(out)
        out = self.layer9(out)
        out = self.layer10(out)
        out = self.layer11(out)
        out = self.layer12(out)
        out = self.layer13(out)
        out = self.adaptivepool(out)
        out = torch.flatten(out,1)
        #out = out.reshape(out.size(0), -1)
        out = self.fc1(out)
        out = self.fc2(out)
        out = self.fc3(out)
        return out


##############################################################################
########################----4 layers CNN network-----##########################
###############################################################################
class cnn_4layers_custom(nn.Module):
    def __init__(self, num_classes):
        super(cnn_4layers_custom, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU())
        self.layer2 = nn.Sequential(
            nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(), 
            nn.MaxPool2d(kernel_size = 2, stride = 2))
        self.layer3 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU())
        self.layer4 = nn.Sequential(
            nn.Conv2d(128, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size = 2, stride = 2))

        self.adaptivepool = torch.nn.AdaptiveAvgPool2d(output_size=(7,7))

        self.fc1 = nn.Sequential(
            nn.Linear(7*7*128, 896),
            nn.ReLU(),
            nn.Dropout(0.5))
        
        self.fc2= nn.Sequential(
            nn.Linear(896, num_classes))

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = self.adaptivepool(out)
        out = torch.flatten(out,1)
        #out = out.reshape(out.size(0), -1)
        out = self.fc1(out)
        out = self.fc2(out)
        return out
