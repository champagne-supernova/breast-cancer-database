from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url
from . import views

urlpatterns = [
		url(r'^search_results/$', views.BlastResults.as_view(), name='blast_results'),
]

