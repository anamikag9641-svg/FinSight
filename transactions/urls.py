from django.urls import path
from . import views


urlpatterns = [
    path('', views.transaction_list, name='transactions'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('delete/<int:id>/', views.delete_transaction, name='delete_transaction'),
]