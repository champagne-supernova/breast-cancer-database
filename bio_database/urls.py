from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
	url(r'^$', TemplateView.as_view(template_name="bio_home/bio_home.html"), name='home_page'),
	url(r'^search/', include('bio_search.urls_search')),
	url(r'genome/', include('bio_genome.urls_genome')),
	url(r'publication/', include('bio_publication.urls_publication')),
	url(r'cancer/', include('bio_cancer.urls_cancer')),
	url(r'expression/', include('bio_expr.urls_expr')),
	url(r'homolog/', include('bio_homolog.urls_homolog')),
	url(r'variation/', include('bio_variation.urls_var')),
	url(r'omic_wiki/', include('bio_omic_wiki.urls_omic')),
	url(r'kegg/', include('bio_kegg.urls_kegg')),
	url(r'go/', include('bio_go.urls_go')),
	url(r'microRNA/', include('bio_microRNA.urls_microRNA')),
	url(r'projects/', include('bio_reports.urls_report')),
	url(r'^data\.json$', TemplateView.as_view(template_name="jsondata/data.json")),
)
