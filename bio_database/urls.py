from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
	url(r'^$', TemplateView.as_view(template_name="home/index.html"), name='home_page'),
	url(r'^search/', include('bio_search.urls_search')),
	url(r'^blast/', include('bio_search.urls_blast')),
	url(r'genome/', include('bio_search.urls_genome')),
)
