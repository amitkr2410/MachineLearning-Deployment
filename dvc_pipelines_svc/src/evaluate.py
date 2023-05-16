import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn import tree
from dvclive import Live
import matplotlib as mpl
import matplotlib.pyplot as plt 
import json
import math
import pickle, sys, os 

EVAL_PATH = "eval"

if len(sys.argv) != 3:
    sys.stderr.write("Check Arguments, there is error in usage:\n")
    sys.stderr.write("\t python evaluate.py model/model.pickle data \n")
    sys.exit(1)

model_file = sys.argv[1]
train_file = os.path.join(sys.argv[2], "train.csv")
test_file = os.path.join(sys.argv[2], "test.csv")
model = pickle.load(open(model_file,'rb'))


def EvaluationChart(model, input_data_name, split_label, dvc_live):
    df = pd.read_csv(input_data_name)
    X =  np.asarray(df.iloc[:,:-1])
    y = np.asarray(df.iloc[:,-1])
    y_pred = model.predict(X)
    y_pred_prob = model.predict_proba(X)[:,1]

    # We use dvclive to log metrics and score
    avg_prec = metrics.average_precision_score(y, y_pred_prob)
    roc_auc = metrics.roc_auc_score(y, y_pred_prob)
    if not dvc_live.summary:
        dvc_live.summary = {"avg_prec": {}, "roc_auc": {}}
    dvc_live.summary["avg_prec"][split_label] = avg_prec
    dvc_live.summary["roc_auc"][split_label] = roc_auc

    precision, recall, prc_thresholds = \
            metrics.precision_recall_curve(y, y_pred_prob)
    dvc_live.log_sklearn_plot("roc", y, y_pred_prob, name=f"roc_{split_label}.json")
    dvc_live.log_sklearn_plot("confusion_matrix", 
                          y, y_pred, name=f"cm_{split_label}.json")
    

#Now let's call our function to save scores and metrics in dvc-live
# for both train set and test set
dvc_live = Live(os.path.join(EVAL_PATH, "live"), dvcyaml=False)

EvaluationChart(model, train_file, "train", dvc_live)
EvaluationChart(model, test_file, "test", dvc_live)

dvc_live.make_summary()