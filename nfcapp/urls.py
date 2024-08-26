from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('run-make-data/', views.run_make_data, name='run_make_data'),
    path('run-send-data/', views.run_send_data, name='run_send_data'),
    path('register-nfc/', views.register_nfc, name='register_nfc'),
    path('run-send-nfc-data/', views.attend, name='attend'),
]
