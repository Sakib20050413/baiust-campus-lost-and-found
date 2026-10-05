from django.urls import path
from . import views

app_name = 'items'

urlpatterns = [
    path('', views.home, name='home'),
    path('items/', views.item_list, name='list'),
    path('items/report/', views.item_create, name='create'),
    path('items/<int:pk>/', views.item_detail, name='detail'),
    path('items/<int:pk>/edit/', views.item_update, name='update'),
    path('items/<int:pk>/delete/', views.item_delete, name='delete'),
    path('items/<int:pk>/matches/', views.match_suggestions, name='match_suggestions'),
]
