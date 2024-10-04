from django.urls import path
from .import views
urlpatterns=[
    path('',views.home,name='home'),
    path('encrypt/',views.encrypt_message,name='encrypt_message'),
    path('decrypt/',views.decrypt_message,name='decrypt_message'),
    path('about/',views.about_view,name='about'),
]