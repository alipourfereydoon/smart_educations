from django.test import TestCase
from django.contrib.auth.models import User
from .models import *
from .services import submit_questionnaire
from ml_engine.feature_engineering import normalize_score
from ml_engine.recommender import recommend
class FeatureTests(TestCase):
 def test_normalization(self): self.assertEqual(normalize_score(1),0);self.assertEqual(normalize_score(5),1);self.assertEqual(normalize_score(1,reverse=True),1)
 def test_fallback(self): self.assertEqual(recommend({'response_count':0})[0]['strategy_code'],'human_review')
class QuestionnaireTests(TestCase):
 def test_submission_creates_assessment(self):
  user=User.objects.create_user('t');student=StudentProfile.objects.create(user=user);qnaire=Questionnaire.objects.create(title='q');q=Question.objects.create(category='motivation',text='سوال',order=1);InterventionStrategy.objects.create(code='human_review',title='بررسی',description='گفت‌وگوی آموزشی')
  assessment=submit_questionnaire(student,{str(q.id):4},qnaire);self.assertEqual(assessment.student,student);self.assertEqual(assessment.motivation,.75)
