from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

class StudentProfile(models.Model):
 user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='student_profile')
 grade=models.CharField(max_length=40,blank=True); preferred_language=models.CharField(max_length=20,default='fa')
 created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
 def __str__(self): return f'{self.user.get_full_name() or self.user.username} ({self.grade})'
class Questionnaire(models.Model):
 title=models.CharField(max_length=160); is_active=models.BooleanField(default=True)
 created_at=models.DateTimeField(auto_now_add=True)
 def __str__(self): return self.title
class Question(models.Model):
 CATEGORIES=[(x,x.replace('_',' ')) for x in ['motivation','attention','self_regulation','practice_preference','reading','mathematics']]
 category=models.CharField(max_length=32,choices=CATEGORIES); text=models.CharField(max_length=500)
 answer_type=models.CharField(max_length=20,default='scale'); min_value=models.FloatField(default=1); max_value=models.FloatField(default=5)
 reverse_scored=models.BooleanField(default=False); is_active=models.BooleanField(default=True); order=models.PositiveIntegerField(default=0)
 class Meta: ordering=['order']; indexes=[models.Index(fields=['category','is_active'])]
 def __str__(self): return self.text[:80]
class Response(models.Model):
 student=models.ForeignKey(StudentProfile,on_delete=models.CASCADE,related_name='responses'); question=models.ForeignKey(Question,on_delete=models.CASCADE)
 questionnaire=models.ForeignKey(Questionnaire,on_delete=models.CASCADE); numeric_value=models.FloatField(null=True,blank=True); text_value=models.TextField(blank=True)
 created_at=models.DateTimeField(auto_now_add=True)
 class Meta: constraints=[models.UniqueConstraint(fields=['student','question','questionnaire'],name='unique_student_questionnaire_answer')]; indexes=[models.Index(fields=['student','questionnaire'])]
class Assessment(models.Model):
 student=models.ForeignKey(StudentProfile,on_delete=models.CASCADE,related_name='assessments'); questionnaire=models.ForeignKey(Questionnaire,on_delete=models.SET_NULL,null=True,blank=True)
 motivation=models.FloatField(default=.5,validators=[MinValueValidator(0),MaxValueValidator(1)]); attention=models.FloatField(default=.5,validators=[MinValueValidator(0),MaxValueValidator(1)])
 self_regulation=models.FloatField(default=.5,validators=[MinValueValidator(0),MaxValueValidator(1)]); practice_preference=models.FloatField(default=.5,validators=[MinValueValidator(0),MaxValueValidator(1)])
 visual_engagement=models.FloatField(default=.5,validators=[MinValueValidator(0),MaxValueValidator(1)]); reading_comprehension=models.FloatField(default=.5,validators=[MinValueValidator(0),MaxValueValidator(1)])
 mathematics_performance=models.FloatField(default=.5,validators=[MinValueValidator(0),MaxValueValidator(1)])
 feature_json=models.JSONField(default=dict,blank=True); source=models.CharField(max_length=40,default='questionnaire'); model_version=models.CharField(max_length=80,blank=True); created_at=models.DateTimeField(auto_now_add=True)
 class Meta: indexes=[models.Index(fields=['student','-created_at'])]
 def __str__(self): return f'Assessment {self.student_id} / {self.created_at:%Y-%m-%d}'
class InterventionStrategy(models.Model):
 code=models.SlugField(max_length=50,unique=True); title=models.CharField(max_length=160); description=models.TextField(); priority=models.PositiveSmallIntegerField(default=3)
 duration_minutes=models.PositiveSmallIntegerField(default=20); frequency_per_week=models.PositiveSmallIntegerField(default=3); rules_json=models.JSONField(default=dict,blank=True); is_active=models.BooleanField(default=True)
 def __str__(self): return self.title
class Recommendation(models.Model):
 STATUS=[('suggested','پیشنهادی'),('accepted','پذیرفته‌شده'),('dismissed','ردشده')]
 student=models.ForeignKey(StudentProfile,on_delete=models.CASCADE,related_name='recommendations'); assessment=models.ForeignKey(Assessment,on_delete=models.CASCADE,related_name='recommendations'); strategy=models.ForeignKey(InterventionStrategy,on_delete=models.PROTECT)
 score=models.FloatField(default=.5,validators=[MinValueValidator(0),MaxValueValidator(1)]); confidence=models.FloatField(default=.5,validators=[MinValueValidator(0),MaxValueValidator(1)]); priority=models.PositiveSmallIntegerField(default=3)
 reasons_json=models.JSONField(default=list,blank=True); model_version=models.CharField(max_length=80,blank=True); status=models.CharField(max_length=16,choices=STATUS,default='suggested'); created_at=models.DateTimeField(auto_now_add=True)
 class Meta: indexes=[models.Index(fields=['student','status','-created_at'])]
class LearningPlan(models.Model):
 STATUS=[('active','فعال'),('completed','تکمیل‌شده'),('archived','بایگانی')]
 student=models.ForeignKey(StudentProfile,on_delete=models.CASCADE,related_name='plans'); title=models.CharField(max_length=180); objective=models.TextField(); start_date=models.DateField(default=timezone.localdate); end_date=models.DateField(null=True,blank=True); estimated_minutes=models.PositiveIntegerField(default=0); status=models.CharField(max_length=16,choices=STATUS,default='active'); is_current=models.BooleanField(default=True); created_at=models.DateTimeField(auto_now_add=True)
 class Meta: indexes=[models.Index(fields=['student','is_current','status'])]
class PlanItem(models.Model):
 plan=models.ForeignKey(LearningPlan,on_delete=models.CASCADE,related_name='items'); recommendation=models.ForeignKey(Recommendation,on_delete=models.SET_NULL,null=True,blank=True); title=models.CharField(max_length=180); description=models.TextField(blank=True); scheduled_date=models.DateField(null=True,blank=True); estimated_minutes=models.PositiveSmallIntegerField(default=20); is_completed=models.BooleanField(default=False); completion_percent=models.PositiveSmallIntegerField(default=0,validators=[MaxValueValidator(100)]); feedback=models.TextField(blank=True); completed_at=models.DateTimeField(null=True,blank=True); order=models.PositiveSmallIntegerField(default=0)
 class Meta: ordering=['order']; indexes=[models.Index(fields=['plan','is_completed'])]
class Outcome(models.Model):
 student=models.ForeignKey(StudentProfile,on_delete=models.CASCADE,related_name='outcomes'); plan_item=models.ForeignKey(PlanItem,on_delete=models.SET_NULL,null=True,blank=True); metric=models.CharField(max_length=80); value=models.FloatField(); observed_at=models.DateTimeField(default=timezone.now); notes=models.TextField(blank=True)
class ModelVersion(models.Model):
 version=models.CharField(max_length=80,unique=True); artifact_path=models.CharField(max_length=255,blank=True); metrics_json=models.JSONField(default=dict,blank=True); is_active=models.BooleanField(default=False); created_at=models.DateTimeField(auto_now_add=True)
class AuditLog(models.Model):
 actor=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True); action=models.CharField(max_length=100); object_type=models.CharField(max_length=100); object_id=models.CharField(max_length=80,blank=True); details_json=models.JSONField(default=dict,blank=True); created_at=models.DateTimeField(auto_now_add=True)
 class Meta: indexes=[models.Index(fields=['-created_at','action'])]
