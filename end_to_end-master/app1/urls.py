from django.contrib import admin
from django.urls import path
from .views import*
urlpatterns = [
    path('', login_view, name="login"),
    path('logout/',logout_view,name="logout"),
    path('home/',home,name="home"),
    path('registration/',registration,name="registration"),
    path('update/<int:user_id>/',update,name='update'),
    path('view_detail/<int:user_id>/',view_detail,name="view_detail"),
    path('delete/<int:user_id>/',delete,name="delete")
] 
