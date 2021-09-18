from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('content/', views.content, name="content"),
    path('content/<int:content_id>/', views.content_detail, name='detail'),
    path('content/create/', views.ContentCreate.as_view(), name='content_create'),
    path('content/<int:pk>/update/', views.ContentUpdate.as_view(), name='content_update'),
    path('content/<int:pk>/delete/', views.ContentDelete.as_view(), name='content_delete'),
    path('content/<int:content_id>/add_entry/', views.add_entry, name='add_entry'),
    path('content/<int:content_id>/delete_entry/', views.delete_entry, name='delete_entry'),
    path('platforms', views.PlatformList.as_view(), name="platform_list"),
    path('platforms/<int:pk>/', views.PlatformDetail.as_view(), name='platform_detail'),
    path('platforms/create/', views.PlatformCreate.as_view(), name='platform_create'),
    path('platforms/<int:pk>/update', views.PlatformUpdate.as_view(), name='platform_update'),
    path('platforms/<int:pk>/delete', views.PlatformDelete.as_view(), name='platform_delete'),
]