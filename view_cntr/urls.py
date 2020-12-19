from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard.html'),
    path('view-cntr', views.view_cntr, name='view_cntr.html'),
]