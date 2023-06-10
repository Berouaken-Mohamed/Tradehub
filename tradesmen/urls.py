from django.urls import path
from . import views

app_name = 'tradesmen'

urlpatterns = [
    path('job_list/', views.job_list, name='job_list'),
    #path('', views.job_list, name='job_list'),
    path('create/', views.create_job, name='create_job'),
    path('delete-job/', views.delete_job, name='delete_job'),
    #customer service part
    path('customer-service/', views.customer_service, name='customer_service'),
    #user part
    path('register/', views.register, name='register'),
    path('user/<str:username>/', views.user_page, name='user_page'),
]

