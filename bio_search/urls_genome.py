from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url
from . import views

urlpatterns = [
		url(r'^$', views.GenomeHomePage.as_view(), name='genome_page'),
]

