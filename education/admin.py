from django.contrib import admin
from .models import *
for model in [StudentProfile,Questionnaire,Question,Response,Assessment,InterventionStrategy,Recommendation,LearningPlan,PlanItem,Outcome,ModelVersion,AuditLog]: admin.site.register(model)
