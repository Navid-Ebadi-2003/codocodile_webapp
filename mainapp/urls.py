from django.urls import path
from mainapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', view=views.home, name="home"),
    path('login/', view=views.login_page, name="login"),
    path('register/', view=views.register_page, name="register"),
    path('posts/<str:pk>', views.post_page, name='post'),
    path('users/<str:username>', views.profile_page, name='profile'),
    path('new-post/', views.create_post, name='newPost'),
    path('posts/<str:pk>/edit', views.editPost, name='editPost'),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('logout/', views.logout_page, name='logout'),
    path('rate/<str:username>', views.add_rate, name='rate'),
    path('profile-edit/<str:username>', views.edit_profile, name='edit_profile'),
    path('search/', views.search, name = 'search'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)