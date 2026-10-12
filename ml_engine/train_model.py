from pathlib import Path
import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,accuracy_score
import joblib
try:
    from .feature_engineering import FEATURE_NAMES
except ImportError:  # Support direct execution: python ml_engine/train_model.py
    from feature_engineering import FEATURE_NAMES
ROOT=Path(__file__).parent
def main():
 df=pd.read_csv(ROOT/'training_data.csv'); X=df[FEATURE_NAMES]; y=df.strategy_label
 stratify = y if y.value_counts().min() >= 2 else None
 Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,random_state=17,stratify=stratify)
 model=RandomForestClassifier(n_estimators=120,max_depth=8,class_weight='balanced',random_state=17); model.fit(Xtr,ytr)
 pred=model.predict(Xte); metrics={'accuracy':accuracy_score(yte,pred),'report':classification_report(yte,pred,output_dict=True),'sample_count':len(df),'synthetic':True}
 out=ROOT/'artifacts';out.mkdir(exist_ok=True);joblib.dump({'model':model,'feature_names':FEATURE_NAMES,'version':'demo-rf-1'},out/'recommender.joblib')
 (out/'metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'accuracy':metrics['accuracy'],'samples':len(df)},indent=2))
if __name__=='__main__': main()
