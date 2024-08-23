from django.urls               import path
from network                   import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'network'

urlpatterns = [
	path('',      views.home, name='home'),
	path('login/', LoginView.as_view(
			template_name='network/login.html',
			redirect_authenticated_user=True,
			# This is the default; made explicit
			redirect_field_name='next',
		), name = 'login'),

	path('logout/',  LogoutView.as_view(), name='logout'),
	path('signin/',  views.signin,         name='signin'),
	path('signout/', views.signout,        name='signout'),
]
