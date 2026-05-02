from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:id>/', views.post_detail, name='detail'),
    path('create/', views.create_post, name='create'),
    path('edit/<int:id>/', views.edit_post, name='edit'),
    path('delete/<int:id>/', views.delete_post, name='delete'),
    path('like/<int:id>/', views.like_post, name='like'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]