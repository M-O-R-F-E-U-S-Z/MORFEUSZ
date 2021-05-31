from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='morfeusz_app-home'),
    path('group/<int:group_id>/', views.manage_group, name='group'),
    path('delete_from_group/<int:group_id>/<int:member_id>/',
         views.delete_from_group, name='delete_from_group')
]

