from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard.html'),
    path('view-cntr', views.view_cntr, name='view_cntr.html'),
    path('fav/<int:pk>/<str:is_fav>/', views.fav),
    path('listed/<int:pk>/<str:is_listed>/', views.listed),
    path('daily_view/<int:pk>/', views.daily_view),
]