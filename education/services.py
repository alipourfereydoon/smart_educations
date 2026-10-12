from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from .models import *
from ml_engine.feature_engineering import build_features_from_responses, calculate_assessment_values
from ml_engine.recommender import recommend

@transaction.atomic
def submit_questionnaire(student,answers,questionnaire=None):
 questionnaire=questionnaire or Questionnaire.objects.filter(is_active=True).first()
 if not questionnaire: questionnaire=Questionnaire.objects.create(title='پرسش‌نامهٔ آغازین')
 for qid,value in answers.items():
  try: q=Question.objects.get(pk=int(qid),is_active=True); num=float(value)
  except (ValueError,TypeError,Question.DoesNotExist): continue
  if q.min_value<=num<=q.max_value: Response.objects.update_or_create(student=student,question=q,questionnaire=questionnaire,defaults={'numeric_value':num,'text_value':''})
 return create_assessment_and_recommendations(student,questionnaire)
@transaction.atomic
def create_assessment_and_recommendations(student,questionnaire=None):
 features=build_features_from_responses(student,questionnaire); count=student.responses.filter(**({'questionnaire':questionnaire} if questionnaire else {}),numeric_value__isnull=False).count();features['response_count']=count
 assessment=Assessment.objects.create(student=student,questionnaire=questionnaire,feature_json=features,source='questionnaire',**{k:features[k] for k in ['motivation','attention','self_regulation','practice_preference','visual_engagement','reading_comprehension','mathematics_performance']})
 for row in recommend(features,InterventionStrategy.objects.filter(is_active=True).values_list('code',flat=True)):
  strategy=InterventionStrategy.objects.get(code=row['strategy_code'],is_active=True)
  Recommendation.objects.create(student=student,assessment=assessment,strategy=strategy,score=row['score'],confidence=row['confidence'],priority=strategy.priority,reasons_json=row['reasons'],model_version='hybrid-v1')
 return assessment
@transaction.atomic
def create_personalized_plan(student):
 LearningPlan.objects.filter(student=student,is_current=True).update(is_current=False,status='archived')
 assessment=student.assessments.order_by('-created_at').first()
 recs=assessment.recommendations.select_related('strategy').order_by('-confidence') if assessment else []
 plan=LearningPlan.objects.create(student=student,title='برنامهٔ یادگیری شخصی',objective='گام‌های کوتاه و قابل پیگیری برای پشتیبانی از یادگیری.',start_date=timezone.localdate(),end_date=timezone.localdate()+timedelta(days=7))
 for i,rec in enumerate(recs):
  PlanItem.objects.create(plan=plan,recommendation=rec,title=rec.strategy.title,description=rec.strategy.description,estimated_minutes=rec.strategy.duration_minutes,order=i)
 plan.estimated_minutes=sum(x.estimated_minutes for x in plan.items.all());plan.save(update_fields=['estimated_minutes']);return plan
@transaction.atomic
def record_feedback(plan_item,completed=None,completion_percent=None,feedback=''):
 if completed is not None: plan_item.is_completed=bool(completed)
 if completion_percent is not None: plan_item.completion_percent=max(0,min(100,int(completion_percent)));plan_item.is_completed=plan_item.completion_percent>=100
 if feedback: plan_item.feedback=feedback
 if plan_item.is_completed: plan_item.completed_at=timezone.now()
 plan_item.save();return plan_item
