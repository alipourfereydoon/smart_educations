FEATURE_NAMES=['motivation','attention','self_regulation','practice_preference','visual_engagement','reading_comprehension','mathematics_performance']
def normalize_score(value, minimum=1, maximum=5, reverse=False):
 try: n=max(0.0,min(1.0,(float(value)-minimum)/(maximum-minimum))) if maximum>minimum else 0.5
 except (TypeError,ValueError): return None
 return 1-n if reverse else n
def calculate_assessment_values(responses):
 buckets={k:[] for k in FEATURE_NAMES}
 mapping={'reading':'reading_comprehension','mathematics':'mathematics_performance'}
 for item in responses:
  cat=item.get('category'); key=mapping.get(cat,cat)
  if key in buckets:
   val=item.get('normalized_value')
   if val is None: val=normalize_score(item.get('numeric_value'),item.get('min_value',1),item.get('max_value',5),item.get('reverse_scored',False))
   if val is not None: buckets[key].append(val)
 out={k:(sum(v)/len(v) if v else 0.5) for k,v in buckets.items()}
 visual=buckets['practice_preference']; out['visual_engagement']=sum(visual)/len(visual) if visual else out['practice_preference']
 return out
def build_features_from_responses(student, questionnaire=None):
 qs=student.responses.select_related('question').all()
 if questionnaire is not None: qs=qs.filter(questionnaire=questionnaire)
 rows=[]
 for r in qs:
  q=r.question
  rows.append({'category':q.category,'numeric_value':r.numeric_value,'min_value':q.min_value,'max_value':q.max_value,'reverse_scored':q.reverse_scored})
 return calculate_assessment_values(rows)
