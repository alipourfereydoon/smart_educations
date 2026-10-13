import re
import secrets
from django import forms
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import Question, StudentProfile

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model=StudentProfile
        fields=["first_name","last_name","grade","national_id","father_name","school_name","mobile"]
        labels={"first_name":"نام","last_name":"نام خانوادگی","grade":"مقطع تحصیلی","national_id":"کد ملی","father_name":"نام پدر","school_name":"نام مدرسه","mobile":"شماره تماس همراه"}
        widgets={k:forms.TextInput(attrs={"autocomplete":"off"}) for k in ["first_name","last_name","grade","national_id","father_name","school_name","mobile"]}
    def clean_national_id(self):
        value=self.cleaned_data["national_id"].strip()
        if not re.fullmatch(r"\d{10}",value) or len(set(value))==1: raise forms.ValidationError("کد ملی باید ۱۰ رقم معتبر و غیرتکراری باشد.")
        return value
    def clean_mobile(self):
        value=self.cleaned_data["mobile"].strip().replace(" ","").replace("-","")
        if not re.fullmatch(r"09\d{9}",value): raise forms.ValidationError("شماره همراه باید با ۰۹ و ۱۱ رقم وارد شود.")
        return value
    def clean_grade(self):
        value=self.cleaned_data["grade"].strip()
        if not value: raise forms.ValidationError("مقطع تحصیلی را وارد کنید.")
        return value
    @transaction.atomic
    def save(self, commit=True):
        profile=super().save(commit=False)
        User=get_user_model()
        user=User.objects.create_user(username=f"student_{profile.national_id}",password=None,first_name=profile.first_name,last_name=profile.last_name)
        user.set_unusable_password(); user.save()
        profile.user=user
        if commit: profile.save()
        return profile

class StudentLoginForm(forms.Form):
    national_id=forms.CharField(label="کد ملی",max_length=10,widget=forms.TextInput(attrs={"inputmode":"numeric","autocomplete":"off"}))
    mobile=forms.CharField(label="شماره همراه",max_length=11,widget=forms.TextInput(attrs={"inputmode":"tel","autocomplete":"off"}))
    def clean_national_id(self):
        v=self.cleaned_data["national_id"].strip()
        if not re.fullmatch(r"\d{10}",v) or len(set(v))==1: raise forms.ValidationError("کد ملی باید ۱۰ رقم باشد.")
        return v
    def clean_mobile(self):
        v=self.cleaned_data["mobile"].strip().replace(" ","").replace("-","")
        if not re.fullmatch(r"09\d{9}",v): raise forms.ValidationError("شماره همراه معتبر وارد کنید.")
        return v

class QuestionnaireForm(forms.Form):
 def __init__(self,*args,questions=None,**kwargs):
  super().__init__(*args,**kwargs); self.questions=list(questions or [])
  for q in self.questions:
   self.fields[f'q_{q.id}']=forms.IntegerField(label=q.text,min_value=int(q.min_value),max_value=int(q.max_value),widget=forms.RadioSelect(choices=[(i,str(i)) for i in range(int(q.min_value),int(q.max_value)+1)]),required=False)
 def clean(self):
  data=super().clean()
  if not any(data.get(f'q_{q.id}') is not None for q in self.questions): raise forms.ValidationError('لطفاً دست‌کم به یک پرسش پاسخ دهید.')
  return data

# Backwards-compatible names for existing integrations.
RegistrationForm = StudentRegistrationForm
LoginForm = StudentLoginForm
