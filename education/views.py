import hashlib, json
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import get_object_or_404,redirect,render
from django.views.decorators.http import require_POST
from .models import *
from .forms import QuestionnaireForm, StudentRegistrationForm, StudentLoginForm
from .services import submit_questionnaire,create_personalized_plan,record_feedback

def home(request):
 student=StudentProfile.objects.filter(user=request.user).first() if request.user.is_authenticated else None
 return render(request,'education/home.html',{'student':student,'question_count':Question.objects.filter(is_active=True).count()})

def register_view(request):
 if request.user.is_authenticated: return redirect('home')
 form=StudentRegistrationForm(request.POST or None)
 if request.method=='POST' and form.is_valid():
  student=form.save(); login(request,student.user,backend='django.contrib.auth.backends.ModelBackend')
  messages.success(request,'ثبت‌نام شما انجام شد. این ورود صرفاً دمو است و تأیید مالکیت شماره تماس محسوب نمی‌شود.')
  return redirect('profile',student_id=student.pk)
 return render(request,'education/register.html',{'form':form})

def _attempt_key(request,national_id):
 identity=f"{request.META.get('REMOTE_ADDR','')}:{national_id}"
 return 'auth-attempt:'+hashlib.sha256(identity.encode()).hexdigest()

def login_view(request):
 if request.user.is_authenticated: return redirect('home')
 form=StudentLoginForm(request.POST or None)
 if request.method=='POST':
  if form.is_valid():
   key=_attempt_key(request,form.cleaned_data['national_id'])
   if cache.get(key,0)>=5:
    form.add_error(None,'تلاش‌های ورود موقتاً محدود شده است. کمی بعد دوباره تلاش کنید.')
   else:
    user=authenticate(request,national_id=form.cleaned_data['national_id'],mobile=form.cleaned_data['mobile'])
    if user is not None:
     cache.delete(key); login(request,user); messages.success(request,'با موفقیت وارد شدید.')
     return redirect('profile',student_id=user.student_profile.pk)
    cache.set(key,cache.get(key,0)+1,900); form.add_error(None,'کد ملی یا شماره همراه نادرست است.')
 return render(request,'education/login.html',{'form':form})

@require_POST
def logout_view(request):
 logout(request); messages.success(request,'از حساب خارج شدید.'); return redirect('home')

def owned_student(request,student_id):
 return get_object_or_404(StudentProfile,pk=student_id,user=request.user)

@login_required
def questionnaire(request,student_id):
 student=owned_student(request,student_id); questions=Question.objects.filter(is_active=True); form=QuestionnaireForm(request.POST or None,questions=questions)
 if request.method=='POST' and form.is_valid():
  answers={str(q.id):form.cleaned_data.get(f'q_{q.id}') for q in questions if form.cleaned_data.get(f'q_{q.id}') is not None};submit_questionnaire(student,answers);messages.success(request,'پاسخ‌ها ثبت و پیشنهادهای آموزشی آماده شد.');return redirect('profile',student_id=student.id)
 return render(request,'education/questionnaire.html',{'student':student,'form':form})

@login_required
def profile(request,student_id):
 student=owned_student(request,student_id);assessment=student.assessments.order_by('-created_at').first()
 recs=assessment.recommendations.select_related('strategy') if assessment else []
 return render(request,'education/profile.html',{'student':student,'assessment':assessment,'recommendations':recs})

@login_required
def plan(request,student_id):
 student=owned_student(request,student_id); plan=student.plans.filter(is_current=True).prefetch_related('items').first()
 if not plan and student.assessments.exists(): plan=create_personalized_plan(student)
 return render(request,'education/plan.html',{'student':student,'plan':plan})

@login_required
@require_POST
def feedback_api(request,plan_item_id):
 item=get_object_or_404(PlanItem,pk=plan_item_id,plan__student__user=request.user)
 try: data=json.loads(request.body or '{}')
 except json.JSONDecodeError: return JsonResponse({'error':'درخواست JSON نامعتبر است.'},status=400)
 if not isinstance(data,dict): return JsonResponse({'error':'ساختار درخواست نامعتبر است.'},status=400)
 try: item=record_feedback(item,data.get('completed'),data.get('completion_percent'),str(data.get('feedback',''))[:1000])
 except (ValueError,TypeError): return JsonResponse({'error':'مقادیر ارسالی نامعتبر هستند.'},status=400)
 return JsonResponse({'ok':True,'completed':item.is_completed,'completion_percent':item.completion_percent})


# Compatibility alias for older URL configurations.
register = register_view
