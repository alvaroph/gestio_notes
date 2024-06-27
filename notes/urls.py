from django.urls import path
from .views import LoginView, ActivitiesView, update_grade, redirect_to_login, logout_view

urlpatterns = [
    path('', redirect_to_login, name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('activities/', ActivitiesView.as_view(), name='activities'),
    path('update_grade/', update_grade, name='update_grade'),  # Sin parámetros en la URL
]
