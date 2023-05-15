#Import library
import pandas as pd    #to manipulate data in csv in row and column format
import numpy as np     #
import matplotlib as mpl
import matplotlib.pyplot as plt #
import pickle, sys, os
from sklearn.model_selection import train_test_split
import yaml

params = yaml.safe_load(open("params.yaml"))["preprocess"]

if len(sys.argv) != 4:
    sys.stderr.write("Check Arguments, there is error in usage:\n")
    sys.stderr.write("\t python prepare.py inputfile out1 out2 \n")
    sys.exit(1)

# Test data set split ratio
seed = params["seed"]
test_size = params["test_size"]

filename = sys.argv[1]
FileTrain= sys.argv[2]
FileTest = sys.argv[3]
#filename = 'data/cell_samples_for_svm.csv'
#FileTrain ='data/train.csv'
#FileTest = 'data/test.csv'


df = pd.read_csv(filename)
#display(df.head())
print("shape", df.shape)
print("Columns count=\n", df.count())
print("mode = \n", df['Class'].value_counts())
print("data types= \n", df.dtypes)

#Check for null values
print( df.isnull().sum() )



#From above we find there are no-null entry in the data set
#Also, we note that column='BareNuc' is non-numerical !!!
#Visualize Size and shape of benign and malignant cells
benign_df = df[df['Class']==2]
malignant_df = df[df['Class']==4]
axes_0 = benign_df.plot( x='Clump',y='UnifSize', 
                        color='blue', marker='o', markersize=10,linewidth=0,
                         label='Benign')
malignant_df.plot( x='Clump',y='UnifSize', linewidth=0,
                        color='red', marker='v',  markersize=15, markerfacecolor='none', label='Malignant', ax=axes_0)
axes_0.set_ylim(0,15)
axes_0.set_xlim(0,12)


#Identify unwanted rows
#Columns 'BareNuc' is non-numerical data
print(df.isnull().sum())
df_new = df[ pd.to_numeric(df['BareNuc'], errors='coerce').notnull() ]
df_new['BareNuc'] = df_new['BareNuc'].astype('int')
df_new.dtypes

#Create training data set by converting pandas data frame into numpy arrary
#which are input to SVM function
#Select all columns except ID and class
df_x = df_new.iloc[:,1:-1]
#display(df_x.head())

# independent variables as numpy array
X = np.asarray(df_x)
#display(X)

#dependent variables as numpy array
y = np.asarray(df_new['Class'])

#Import library for splitting data sets into training and test set
#from sklearn.model_selection import train_test_split

#Create train and test
df_train, df_test = train_test_split(df_new.iloc[:,1:], test_size=test_size, random_state=seed)
print(df_train.head())
df_train.to_csv(FileTrain, sep='\t', index=False)
df_test.to_csv(FileTest, sep='\t', index=False)
