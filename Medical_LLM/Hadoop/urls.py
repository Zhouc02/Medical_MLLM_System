from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login),
    path('manager_check/', views.manager_check),
    path('manager_add/', views.manager_add),
    path('manager_delete/', views.manager_delete),
    path('manager_update/', views.manager_update),
    path('patient_pic/', views.upload),
    path('patient_generate/', views.generate),
    path('history_list/', views.history_list),
    path('special_record/', views.special_record),
    path('patient_check/', views.patient_check),
    path('redis_clear/', views.redis_clear),
    path('manager_search/', views.manager_search),
    path('patient_search/', views.patient_search),
    path('dialogue_check/', views.dialogue_check),
    path('doctor_help/', views.doctor_help),
    path('log_list/', views.log_list),
    path('hive_analysis/', views.hive_analysis),
    path('mapreduce_analysis/', views.mapreduce_analysis)
]
