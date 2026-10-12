from django import forms
from .models import Question
class QuestionnaireForm(forms.Form):
 def __init__(self,*args,questions=None,**kwargs):
  super().__init__(*args,**kwargs); self.questions=list(questions or [])
  for q in self.questions:
   self.fields[f'q_{q.id}']=forms.IntegerField(label=q.text,min_value=int(q.min_value),max_value=int(q.max_value),widget=forms.RadioSelect(choices=[(i,str(i)) for i in range(int(q.min_value),int(q.max_value)+1)]),required=False)
 def clean(self):
  data=super().clean()
  if not any(data.get(f'q_{q.id}') is not None for q in self.questions): raise forms.ValidationError('لطفاً دست‌کم به یک پرسش پاسخ دهید.')
  return data
