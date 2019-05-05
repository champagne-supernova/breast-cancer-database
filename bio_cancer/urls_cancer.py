# --*--coding:UTF-8--*--
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url
from . import views

urlpatterns = [
		url(r'home$', views.BioCancerhome.as_view(), name = 'home_page'),
		url(r'^$', views.BioCancerPage.as_view(), name='cancer_genomic_page'),
        url(r'simple-search$', views.BioCancerPage.as_view(), name='cancer_genomic_page'),
        url(r'text-search$', views.BioCancerPage_textsearch.as_view(), name='genomic_page_text'),
		url(r'images/$', views.BioCancerImagePage.as_view(), name='cancer_image_page'),
		url(r'about$', views.BioCancerabout.as_view(), name='about_page'),
		url(r'contact$', views.BioCancercontact.as_view(), name='contact_page'),
		url(r'genomic_detail/(?P<sample_id>.*)/(?P<type_id>.*)$', views.BioCancerdetail.as_view(), name='genomic_detail'),
		url(r'image_detail/(?P<patient_id>.*)/(?P<serie_id>.*)$', views.BioImagedetail.as_view(), name='image_detail'),
		# 获取参数sample_id, type_id
        # /(?P<sample_id>.*)/(?P<type_id>\.*)}
		url(r'image/(?P<patient_id>.*)$', views.BioImagePatient.as_view(), name='patient_image'),
		url(r'^image_download/(?P<serie_id>.*)$', views.download_image, name='download_image'),
		url(r'^genomic_download/(?P<sample_id>.*)/(?P<type_id>.*)/(?P<the_name>.*)$', views.download_tcga, name='download_tcga')
]

