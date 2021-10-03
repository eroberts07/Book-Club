from django.urls import path
from . import views

urlpatterns=[
    path('',views.index),
    path('create/', views.register),
    path('signin', views.signin),
    path('logout', views.logout),
    path('profile/create_book/', views.create_book),
    path('profile/', views.profile),
    path('profile/logout', views.logout)
]