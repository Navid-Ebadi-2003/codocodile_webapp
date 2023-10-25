from django.urls import path
from mainapp import views

urlpatterns = [
    path('', view=views.home, name="home"),
    path('login/', view=views.login_page, name="login"),
    path('register/', view=views.register_page, name="register"),
    path('posts/<str:pk>', views.post_page, name='post'),
    path('users/<str:username>', views.profile_page, name='profile'),
    path('new-post/', views.create_post, name='newPost'),
    path('posts/<str:pk>/edit', views.editPost, name='editPost'),
]