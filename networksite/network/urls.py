from django.contrib.auth.decorators import login_required
from django.contrib.auth.views      import LoginView, LogoutView
from django.urls                    import path
from .forms                         import LoginForm
from network                        import views

app_name = 'network'

urlpatterns = [
	path('',                 views.HomeView.as_view(),      name='home'),
	path('following/', login_required(views.FollowingView.as_view()), name='following'),
	path('profile/<int:pk>/', views.ProfileView.as_view(),            name='profile'),


	path('follow/<int:pk>/', views.follow,             name='follow'),
	path('delete/<int:pk>/', views.delete,             name='delete'),
	path('edit/<int:pk>/',   views.edit,               name='edit'),
	path('like/<int:pk>/',   views.like,               name='like'),
#	path('new/',             views.HomeView.as_view(), name='new'),

	path('login/', LoginView.as_view(
			template_name='network/login.html',
			redirect_authenticated_user=True,
			# This is the default; made explicit
			redirect_field_name='next',
			authentication_form=LoginForm,
		), name = 'login'),

	path('logout/',  LogoutView.as_view(), name='logout'),
	path('signin/',  views.signin,         name='signin'),
	path('signout/', views.signout,        name='signout'),
]
