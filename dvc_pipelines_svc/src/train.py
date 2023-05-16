#Import library
import pandas as pd    #to manipulate data in csv in row and column format
import numpy as np     #
import matplotlib as mpl
import matplotlib.pyplot as plt #
import pickle, os, sys

import yaml
from sklearn import svm

params = yaml.safe_load(open("params.yaml"))["train"]

if len(sys.argv) != 3:
    sys.stderr.write("Check Arguments, there is error in usage:\n")
    sys.stderr.write("\t python train.py inputfile outfile \n")
    sys.exit(1)

InputFileName = sys.argv[1]
SaveFileName = sys.argv[2]
KernelName = params["kernel"]
Gamma = params["gamma"]
c0 = params["c0"]
poly_deg = params["poly_deg"]


df_train = pd.read_csv(InputFileName)

X_train =  np.asarray(df_train.iloc[:,:-1])
y_train = np.asarray(df_train.iloc[:,-1])
print(y_train) 
if KernelName =="linear":
    classifier = svm.SVC(kernel=KernelName, gamma=Gamma, C=c0, probability=True)
if KernelName == "poly":
    classifier = svm.SVC(kernel=KernelName, degree=poly_deg, probability=True)
if KernelName == "rbf":
    classifier = svm.SVC(kernel=KernelName, gamma=Gamma, C=c0, probability=True)
if KernelName == "sigmoid":
    classifier = svm.SVC(kernel=KernelName, gamma=Gamma, C=c0, probability=True)
# penality parameter=C and gamma are tunning parameters


classifier.fit(X_train, y_train)
y_predict = classifier.predict(X_train)

pickle.dump(classifier, open(SaveFileName,'wb') )
