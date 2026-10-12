from pathlib import Path
import joblib
CODES=['short_interactive','practice_based','structured_study','advanced_project','human_review']
def recommend(features,available_codes=None,minimum_answers=5):
 available=set(available_codes or CODES); vals=[float(features.get(k,.5)) for k in ['motivation','attention','self_regulation','practice_preference','reading_comprehension','mathematics_performance']]; lowdata=features.get('response_count',0)<minimum_answers
 rules=[]
 def add(code,confidence,reason):
  if code in available and all(x['strategy_code']!=code for x in rules): rules.append({'strategy_code':code,'confidence':confidence,'score':confidence,'reasons':[reason]})
 mot=float(features.get('motivation',.5)); att=float(features.get('attention',.5)); prac=float(features.get('practice_preference',.5)); math=float(features.get('mathematics_performance',.5)); reg=float(features.get('self_regulation',.5)); reading=float(features.get('reading_comprehension',.5))
 if lowdata or not features: add('human_review',.96,'اطلاعات کافی نیست؛ بررسی و گفت‌وگوی آموزشی پیشنهاد می‌شود.')
 if mot<.4 or att<.4: add('short_interactive',.84,'فعالیت‌های کوتاه و تعاملی می‌تواند شروع یادگیری را آسان‌تر کند.')
 if prac>.65 and math<.55: add('practice_based',.82,'ترجیح تمرین عملی همراه با نیاز به تقویت ریاضی دیده می‌شود.')
 if math<.45 or reading<.4: add('structured_study',.8,'تمرین منظم و مرحله‌بندی‌شده برای تقویت مهارت پیشنهاد می‌شود.')
 if reg>.7 and math>.7 and reading>.65: add('advanced_project',.76,'خودتنظیمی و عملکرد قوی، زمینهٔ یک پروژهٔ چالشی را فراهم می‌کند.')
 if not rules: add('structured_study',.62,'برای ادامه، برنامهٔ منظم و قابل پیگیری پیشنهاد می‌شود.')
 path=Path(__file__).parent/'artifacts/recommender.joblib'
 if path.exists() and not lowdata:
  try:
   model=joblib.load(path); row=[[float(features.get(k,.5)) for k in model['feature_names']]]; label=str(model['model'].predict(row)[0])
   if label in available and all(x['strategy_code']!=label for x in rules): rules.append({'strategy_code':label,'confidence':.65,'score':.65,'reasons':['مدل یادگیری ماشین؛ پیشنهاد برای بررسی آموزشی.']})
  except Exception: pass
 return sorted(rules,key=lambda x:x['confidence'],reverse=True)[:3]
