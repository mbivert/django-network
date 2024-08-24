from django.urls               import path
from network                   import views
from django.contrib.auth.views import LoginView, LogoutView
from .forms                    import LoginForm

app_name = 'network'

urlpatterns = [
	path('',      views.HomeView.as_view(), name='home'),
	path('new/',  views.HomeView.as_view(), name='new'), # TODO
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
