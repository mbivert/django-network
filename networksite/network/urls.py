from django.urls               import path, include
from django.contrib.auth.views import LoginView

from . import views

app_name = 'network'

urlpatterns = [
	path('',                  views.AllPostsView.as_view(),  name='allposts'),
	path('add/post/',         views.addpost,                 name='add'),
	path('following/',        views.FollowingView.as_view(), name='following'),
	path('profile/<int:pk>/', views.ProfileView.as_view(),   name='profile'),
	path('edit/<int:pk>/',    views.EditView.as_view(),      name='edit'),
	path('delete/<int:pk>/',  views.delete,                  name='delete'),
	# lazzy
    path("accounts/",      include("django.contrib.auth.urls")),
]
