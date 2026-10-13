from django.urls import path
from . import views
urlpatterns=[path('',views.home,name='home'),path('register/',views.register_view,name='register'),path('login/',views.login_view,name='login'),path('logout/',views.logout_view,name='logout'),path('questionnaire/<int:student_id>/',views.questionnaire,name='questionnaire'),path('profile/<int:student_id>/',views.profile,name='profile'),path('plan/<int:student_id>/',views.plan,name='plan'),path('api/feedback/<int:plan_item_id>/',views.feedback_api,name='feedback_api')]
