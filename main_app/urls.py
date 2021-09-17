from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('content/', views.content, name="content"),
    path('content/<int:content_id>/', views.content_detail, name='detail'),
    path('content/create/', views.ContentCreate.as_view(), name='content_create'),
    path('cats/<int:pk>/update/', views.ContentUpdate.as_view(), name='content_update'),
]