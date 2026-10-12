from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from education.models import *
from education.services import create_assessment_and_recommendations,create_personalized_plan
class Command(BaseCommand):
 help='Create or refresh a Persian demo learner and sample data.'
 def handle(self,*args,**opts):
  u,_=User.objects.get_or_create(username='ali',defaults={'first_name':'علی','last_name':'نمونه'});u.set_password('Ali12345!');u.save()
  student,_=StudentProfile.objects.get_or_create(user=u,defaults={'grade':'پایهٔ هفتم'})
  strategies=[('short_interactive','فعالیت تعاملی کوتاه','یادگیری در بازه‌های کوتاه با پرسش‌های فوری.',1,12,5),('practice_based','تمرین گام‌به‌گام','تمرین مسئله‌های کوتاه همراه با بازخورد.',2,20,4),('structured_study','مطالعهٔ ساختارمند','تقسیم کار به گام‌های ساده و مرور منظم.',2,25,4),('advanced_project','پروژهٔ چالشی','پروژهٔ کوچک برای به‌کارگیری آموخته‌ها.',3,35,2),('human_review','گفت‌وگوی آموزشی','بررسی انسانی برای شناخت بهتر نیازها و زمینهٔ یادگیری.',1,20,1)]
  for code,title,desc,pri,dur,freq in strategies: InterventionStrategy.objects.update_or_create(code=code,defaults={'title':title,'description':desc,'priority':pri,'duration_minutes':dur,'frequency_per_week':freq,'is_active':True})
  questionnaire,_=Questionnaire.objects.get_or_create(title='پرسش‌نامهٔ نمونهٔ یادگیری')
  bank={'motivation':['از یادگیری موضوع‌های تازه لذت می‌برم.','برای رسیدن به هدف درسی تلاش می‌کنم.','وقتی درس دشوار می‌شود ادامه می‌دهم.'],'attention':['هنگام مطالعه می‌توانم روی درس تمرکز کنم.','با حواس‌پرتی تمرکزم به‌راحتی کم می‌شود.','می‌توانم یک فعالیت درسی را تا پایان دنبال کنم.'],'self_regulation':['برای مطالعه برنامه‌ریزی می‌کنم.','پیشرفت خودم را بررسی می‌کنم.','برای انجام تکلیف زمان مشخصی می‌گذارم.'],'practice_preference':['با حل تمرین بهتر یاد می‌گیرم.','فعالیت عملی را به توضیح طولانی ترجیح می‌دهم.','نمونه‌مسئله به یادگیری من کمک می‌کند.'],'reading':['متن درسی را می‌خوانم و نکته‌های اصلی را پیدا می‌کنم.','می‌توانم مفهوم یک متن آموزشی را با زبان خودم توضیح دهم.','پس از خواندن، پرسش‌های متن را پاسخ می‌دهم.'],'mathematics':['در حل مسئله‌های ریاضی اعتمادبه‌نفس دارم.','می‌توانم راه‌حل مسئلهٔ ریاضی را مرحله‌به‌مرحله پیدا کنم.','تمرین بیشتر به من در ریاضی کمک می‌کند.']}
  questions=[]; order=0
  for category,texts in bank.items():
   for text in texts:
    q,_=Question.objects.update_or_create(text=text,defaults={'category':category,'min_value':1,'max_value':5,'answer_type':'scale','reverse_scored':category=='attention' and 'حواس‌پرتی' in text,'is_active':True,'order':order});questions.append(q);order+=1
  for q in questions:
   value=3 if q.category in ['motivation','attention','self_regulation','practice_preference'] else 3
   Response.objects.update_or_create(student=student,question=q,questionnaire=questionnaire,defaults={'numeric_value':value})
  if not student.assessments.filter(questionnaire=questionnaire).exists(): create_assessment_and_recommendations(student,questionnaire)
  if not student.plans.filter(is_current=True).exists(): create_personalized_plan(student)
  self.stdout.write(self.style.SUCCESS(f'Demo ready: ali / {len(questions)} questions / student id {student.id}'))
