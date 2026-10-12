import json
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404,redirect,render
from django.views.decorators.http import require_POST
from .models import *
from .forms import QuestionnaireForm
from .services import submit_questionnaire,create_personalized_plan,record_feedback

def home(request):
 student=StudentProfile.objects.filter(user__username='ali').first() or StudentProfile.objects.first()
 context={'student':student,'question_count':Question.objects.filter(is_active=True).count(),'plans_count':LearningPlan.objects.filter(is_current=True).count()}
 return render(request,'education/home.html',context)
def questionnaire(request,student_id):
 student=get_object_or_404(StudentProfile,pk=student_id); questions=Question.objects.filter(is_active=True); form=QuestionnaireForm(request.POST or None,questions=questions)
 if request.method=='POST' and form.is_valid():
  answers={str(q.id):form.cleaned_data.get(f'q_{q.id}') for q in questions if form.cleaned_data.get(f'q_{q.id}') is not None};submit_questionnaire(student,answers);messages.success(request,'پاسخ‌ها ثبت و پیشنهادهای آموزشی آماده شد.');return redirect('profile',student_id=student.id)
 return render(request,'education/questionnaire.html',{'student':student,'form':form})
def profile(request,student_id):
 student=get_object_or_404(StudentProfile,pk=student_id);assessment=student.assessments.order_by('-created_at').first()
 recs=assessment.recommendations.select_related('strategy') if assessment else []
 return render(request,'education/profile.html',{'student':student,'assessment':assessment,'recommendations':recs})
def plan(request,student_id):
 student=get_object_or_404(StudentProfile,pk=student_id); plan=student.plans.filter(is_current=True).prefetch_related('items').first()
 if not plan and student.assessments.exists(): plan=create_personalized_plan(student)
 return render(request,'education/plan.html',{'student':student,'plan':plan})
@require_POST
def feedback_api(request,plan_item_id):
 item=get_object_or_404(PlanItem,pk=plan_item_id)
 try: data=json.loads(request.body or '{}')
 except json.JSONDecodeError: return JsonResponse({'error':'درخواست JSON نامعتبر است.'},status=400)
 item=record_feedback(item,data.get('completed'),data.get('completion_percent'),str(data.get('feedback',''))[:1000])
 return JsonResponse({'ok':True,'completed':item.is_completed,'completion_percent':item.completion_percent})
