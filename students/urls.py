from django.urls import path
from students import views

urlpatterns = [
    path('', views.home, name="home"),
    path("signup/", views.SignUp.as_view(), name="signup")
    # path('signup/', views.SignUp, name="signup")
]
