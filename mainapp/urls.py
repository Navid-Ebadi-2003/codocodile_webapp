from django.urls import path
from mainapp import views

urlpatterns = [
    path('', view=views.home),
    path('login/', view=views.login_page)
]