"""Synthetic wearable teaching data and fold-safe preprocessing.
No samples or metrics in this module are from WESAD or Emognition.
"""
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import f1_score, balanced_accuracy_score, confusion_matrix

def make_wearable_windows(seed=42, subjects=8, examples_per_class=12, length=64):
    rng=np.random.default_rng(seed);windows=[];labels=[];groups=[]
    t=np.linspace(0,4,length,endpoint=False)
    for subject in range(subjects):
        offset=rng.normal(0,.5,size=3)
        for label in range(3):
            for example in range(examples_per_class):
                phase=rng.uniform(0,2*np.pi)
                x=np.stack([np.sin(2*np.pi*(1+.3*label)*t+phase),
                    .4*label+.2*np.sin(t+phase),
                    np.cos(2*np.pi*(.2+.1*label)*t+phase)],axis=-1)
                x=x+offset+rng.normal(0,.12,x.shape)
                x[rng.random(x.shape)<.01]=np.nan
                windows.append(x);labels.append(label);groups.append(subject)
    return np.asarray(windows,dtype=np.float32),np.asarray(labels),np.asarray(groups)

def feature_matrix(x):
    return np.concatenate([np.nanmean(x,axis=1),np.nanstd(x,axis=1),
        np.nanmax(x,axis=1)-np.nanmin(x,axis=1)],axis=1)

def fit_signal_scaler(train):
    p=make_pipeline(SimpleImputer(strategy='median'),StandardScaler())
    p.fit(train.reshape(-1,train.shape[-1]));return p

def transform_signals(p,x):
    return p.transform(x.reshape(-1,x.shape[-1])).reshape(x.shape).astype(np.float32)

def classification_report_values(y,pred):
    return {'macro_f1':float(f1_score(y,pred,average='macro',labels=[0,1,2],zero_division=0)),
            'balanced_accuracy':float(balanced_accuracy_score(y,pred))}
