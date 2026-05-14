from django.urls import path
from . import views
urlpatterns = [
    path('patient_talk/', views.talk),
    path('system_monitor/', views.monitor),
    path('cached_clear/', views.clear),
    path('model_list/',views.model_list),
    path('model_switch/', views.model_switch),
    path('ner_predict/', views.ner_predict),
    path('model_add/', views.model_add),
    path('model_delete/', views.model_delete),
    path('model_params/', views.model_params),
]
