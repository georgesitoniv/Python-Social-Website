from django.conf.urls import url, include
from django.contrib.auth import views as auth_view
from . import views

urlpatterns = [
    url(r'^login/$', auth_view.login, name='login'),
    url(r'^logout/$', auth_view.logout, name='logout'),
    url(r'^logout-then-login/$', auth_view.logout_then_login,name='logout_then_login'),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^password-change/$',auth_view.password_change, name='password_change'),
    url(r'^password-change-done/$', auth_view.password_change_done, name='password_change_done'),
    url(r'^register/$', views.RegisterForm.as_view(), name='register'),
    url(r'^edit/$', views.ProfileEdit.as_view(), name='edit'),
]
