"""Data loading and preprocessing for the independent fast.ai solutions."""
from pathlib import Path
import numpy as np,pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
CONT=['Age','SibSp','Parch','LogFare']
CAT=['Sex','Pclass','Embarked']

def load_titanic():
    original=Path('data/titanic/train.csv')
    if original.exists():
        frame=pd.read_csv(original)
        print('Using original Kaggle Titanic train.csv supplied locally.')
    else:
        raw=pd.read_csv('data/titanic_seaborn.csv')
        frame=raw.rename(columns={'survived':'Survived','sex':'Sex','age':'Age',
            'sibsp':'SibSp','parch':'Parch','fare':'Fare','pclass':'Pclass','embarked':'Embarked','deck':'Deck'}).copy()
        print('Using the public seaborn Titanic teaching copy (891 rows); not a Kaggle account download.')
    return frame

def add_features(frame):
    d=frame.copy();d['LogFare']=np.log1p(d.Fare.clip(lower=0))
    d['Family']=d.SibSp+d.Parch+1
    d['Alone']=(d.Family==1).astype(int)
    if 'Cabin' in d:d['Deck']=d.Cabin.str[0]
    if 'Name' in d:d['Title']=d.Name.str.extract(r',\s*([^.]*)\.',expand=False)
    return d

def split_and_prepare():
    frame=add_features(load_titanic())
    tr,va=train_test_split(np.arange(len(frame)),test_size=.2,random_state=42,stratify=frame.Survived)
    processor=ColumnTransformer([
        ('continuous',make_pipeline(SimpleImputer(strategy='median',add_indicator=True),StandardScaler()),CONT),
        ('categorical',make_pipeline(SimpleImputer(strategy='most_frequent'),
            OneHotEncoder(handle_unknown='ignore',sparse_output=False)),CAT)])
    processor.fit(frame.iloc[tr][CONT+CAT])
    features=processor.transform(frame[CONT+CAT]).astype(np.float32)
    target=frame.Survived.to_numpy(dtype=np.float32)
    return frame,tr,va,processor,features,target
