from django.urls import path
from . import views

app_name = 'claims'

urlpatterns = [
    path('submit/<int:item_id>/', views.submit_claim, name='submit'),
    path('<int:pk>/', views.claim_detail, name='detail'),
]
