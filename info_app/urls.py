from django.urls import path
from . import views
urlpatterns=[
    path('',views.encryption_info,name='encryption_info'),
    path('encryption_techniques',views.encryption_techniques,name='encryption_techniques'),
]