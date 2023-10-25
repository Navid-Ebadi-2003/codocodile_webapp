from django.urls import path
from mainapp import views

urlpatterns = [
    path('', view=views.home, name="home"),
    path('login/', view=views.login_page, name="login"),
    path('register/', view=views.register_page, name="register")
]