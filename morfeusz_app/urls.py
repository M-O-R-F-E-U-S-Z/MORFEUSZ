from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='morfeusz_app-home'),
    path('group/<int:group_id>/', views.manage_group, name='group')
]

