from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url
from . import views

urlpatterns = [
		url(r'^$', views.BlastSearch.as_view(), name='search_page'),
]

