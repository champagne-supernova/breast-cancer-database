from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url
from django.conf import settings
from . import views

urlpatterns = [
	url(r'^$', views.report_home_page, name='report_home_page'),
	url(r'^signin/$', views.signin_page, name='signin_page'),
	url(r'^forgot/$', views.forgot_psw, name='forgot_psw'),
	url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATICFILES_DIRS}),
]
urlpatterns += staticfiles_urlpatterns()

