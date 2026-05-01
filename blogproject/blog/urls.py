from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:id>/', views.post_detail, name='detail'),
    path('create/', views.create_post, name='create'),
    path('edit/<int:id>/', views.edit_post, name='edit'),
    path('delete/<int:id>/', views.delete_post, name='delete'),
]