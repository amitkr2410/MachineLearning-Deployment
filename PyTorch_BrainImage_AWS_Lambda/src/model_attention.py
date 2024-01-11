#Model definition for self-attention with positional encoding
import torchvision
import torch
import torch.nn as nn
import math
#import matplotlib.pyplot as plt
def get_model_with_attention(model_name, num_classes) -> nn.Module:
    d_model= 512 #512 dimension embedding vector in Attention research paper
    num_heads=2
    # Ensure that the model dimension (d_model) is divisible by the number of heads
    assert d_model % num_heads == 0, "d_model must be divisible by num_heads"
    if model_name == 'cnn_with_attention':
        print(' You have called cnn with attention module: ')
        model = cnn_with_attention_head(num_classes, d_model, num_heads)

    if model_name == 'only_attention':
        print(' You have called model with basic vision transformer: ')
        model = basic_vision_transformer(num_classes, d_model, num_heads)
    return model 

#### Model class with basic Vision Transformer (only self-attention with position encoding)
class basic_vision_transformer(nn.Module):
    def __init__(self, num_classes, d_model, num_heads):   
        super(basic_vision_transformer, self).__init__()
        self.d_model = d_model
        self.num_heads = num_heads 
        self.adaptivepool = torch.nn.AdaptiveAvgPool2d(output_size=(200,200))
        #flatten size is (50, 128, 14, 14)
        self.patch_embedding_layer = torch.nn.Linear(3*100, d_model)
        #self attention
        self.sa = SelfAttention(d_model, num_heads)
        self.fc= nn.Sequential( nn.Linear(d_model*20*20, num_classes))

    def forward(self, x):
        out = self.adaptivepool(x)
        #print('Size of x after adaptive pooling = ', out.size() )
        
        # size after adaptive pooling is [50,128,14,14]
        patches = out.view(-1, 3, 20*20, 10, 10) 
        # size after reshaping is [50, 128, 7*7, 2,2]
        patches = patches.transpose(1, 2).contiguous()
        # size after transpose [50, 7*7, 128,2,2]
        #print('Patches : ', patches.size())
        patches = torch.flatten(patches,2)
        #print('Patches after flatenning: ', patches.size())
        patches = self.patch_embedding_layer(patches)
        #print('Patches after embedding : ', patches.size())
        out=patches
        max_seq_length = out.size(dim=1)
        pe = positional_encoding(self.d_model, max_seq_length)  
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        pe = pe.to(device)
        #print('size of positional encoding is ', pe.size())
        out = out + pe
        #out = torch.flatten(out,2)
        #print('Flaten only the image pixel 7x7 , so new size = ',out.size())
        #out = out.reshape(out.size(0), -1)
        out = self.sa(out, out, out)
        #print('The size of image tensor after Attention=',out.size() )
        out = torch.flatten(out,1)
        #print('The size of image tensor after flatenning ',out.size() )
        out = self.fc(out)        
        #print('last output tensor is ', out.size() )

        return out 

#### Model class CNN with Attention module for classification ####
class cnn_with_attention_head(nn.Module):
    def __init__(self, num_classes, d_model, num_heads):
        super(cnn_with_attention_head, self).__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        #self.pe = None
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

        self.adaptivepool = torch.nn.AdaptiveAvgPool2d(output_size=(14,14))
        #flatten size is (50, 128, 14, 14)
        self.patch_embedding_layer = torch.nn.Linear(128*4, d_model)
        #self attention
        self.sa = SelfAttention(d_model, num_heads)
        self.fc= nn.Sequential( nn.Linear(d_model*7*7, num_classes))

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = self.adaptivepool(out)
        #print('Size of x after adaptive pooling = ', out.size() )
        '''
        tensor_plot = out
        x_input = x[0]
        x_input = tensor_plot[0]
        print('x_input is ', x_input.size() )
        x_input = x_input.squeeze(0)
        print('x_input is ', x_input.size() )
        x_input = torch.sum(x_input,0)
        print('x_input is ', x_input.size() )
        # image_tensor.permute(1,2,0) # To alter the indices of tensor
        plt.imshow( x_input.detach().numpy()) #convert your tensor to another tensor that isn't requiring a gradient in addition to its actual value definition. This other tensor can be converted to a numpy array. 
        plt.show()
        '''
        # size after adaptive pooling is [50,128,14,14]
        patches = out.view(-1, 128, 7*7, 2, 2) 
        # size after reshaping is [50, 128, 7*7, 2,2]
        patches = patches.transpose(1, 2).contiguous()
        # size after transpose [50, 7*7, 128,2,2]
        #print('Patches : ', patches.size())
        patches = torch.flatten(patches,2)
        #print('Patches after flatenning: ', patches.size())
        patches = self.patch_embedding_layer(patches)
        #print('Patches after embedding : ', patches.size())
        out=patches
        max_seq_length = out.size(dim=1)
        pe = positional_encoding(self.d_model, max_seq_length)  
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        pe = pe.to(device)
        #print('size of positional encoding is ', pe.size())
        out = out + pe
        #out = torch.flatten(out,2)
        #print('Flaten only the image pixel 7x7 , so new size = ',out.size())
        #out = out.reshape(out.size(0), -1)
        out = self.sa(out, out, out)
        #print('The size of image tensor after Attention=',out.size() )
        out = torch.flatten(out,1)
        #print('The size of image tensor after flatenning ',out.size() )
        out = self.fc(out)        
        #print('last output tensor is ', out.size() )

        return out     
#############################################    
######### Class for self-attention ##########
#############################################    
class SelfAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super(SelfAttention, self).__init__()
        # Ensure that the model dimension (d_model) is divisible by the number of heads
        assert d_model % num_heads == 0, "d_model must be divisible by num_heads"
        
        # Initialize dimensions
        self.d_model = d_model # Model's dimension
        self.num_heads = num_heads # Number of attention heads
        self.d_k = d_model // num_heads # Dimension of each head's key, query, and value
        
        # Linear layers for transforming inputs
        self.W_q = nn.Linear(d_model, d_model) # Query transformation
        self.W_k = nn.Linear(d_model, d_model) # Key transformation
        self.W_v = nn.Linear(d_model, d_model) # Value transformation
        self.W_o = nn.Linear(d_model, d_model) # Output transformation
        
    def scaled_dot_product_attention(self, Q, K, V, mask=None):
        # Calculate attention scores
        attn_scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        
        # Apply mask if provided (useful for preventing attention to certain parts like padding)
        if mask is not None:
            attn_scores = attn_scores.masked_fill(mask == 0, -1e9)
        
        # Softmax is applied to obtain attention probabilities
        attn_probs = torch.softmax(attn_scores, dim=-1)
        
        # Multiply by values to obtain the final output
        output = torch.matmul(attn_probs, V)
        return output
        
    def split_heads(self, x):
        # Reshape the input to have num_heads for multi-head attention
        #print('Size of x: ', x.size())
        batch_size, seq_length, d_model = x.size()
        return x.view(batch_size, seq_length, self.num_heads, self.d_k).transpose(1, 2)
        
    def combine_heads(self, x):
        # Combine the multiple heads back to original shape
        batch_size, _, seq_length, d_k = x.size()
        return x.transpose(1, 2).contiguous().view(batch_size, seq_length, self.d_model)
        
    def forward(self, Input_Q, Input_K, Input_V, mask=None):
        # Apply linear transformations and split heads
        #print('Size of Input for Q K V is =', Q.size(), K.size(), V.size())
        Q = self.split_heads(self.W_q(Input_Q))
        K = self.split_heads(self.W_k(Input_K))
        V = self.split_heads(self.W_v(Input_V))
        
        # Perform scaled dot-product attention
        attn_output = self.scaled_dot_product_attention(Q, K, V, mask)
        #print('Size of Vector Q, K, V = ', Q.size(), K.size(), V.size())
        #print('Attention output size =', attn_output.size() )
        # Combine heads and apply output transformation
        output = self.W_o(self.combine_heads(attn_output))
        #print('Attention output size after combining heads =', output.size() )

        return output
    

def positional_encoding(d_model, max_seq_length):    
    pe = torch.zeros(max_seq_length, d_model)
    position = torch.arange(0, max_seq_length, dtype=torch.float).unsqueeze(1)
    div_term = torch.exp(torch.arange(0, d_model, 2).float() * -(math.log(10000.0) / d_model))
    # set the even index values (columns)
    pe[:, 0::2] = torch.sin(position * div_term)
    # set the odd index values (columns)
    pe[:, 1::2] = torch.cos(position * div_term)
    # add a dimension for broadcasting across sequences
    pe = pe.unsqueeze(0)
    #self.register_buffer('pe', pe)
    return pe 