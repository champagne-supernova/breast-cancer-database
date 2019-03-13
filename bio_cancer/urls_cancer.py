# --*--coding:UTF-8--*--
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url
from . import views

urlpatterns = [
		url(r'home$', views.BioCancerhome.as_view(), name = 'home_page'),
		url(r'^$', views.BioCancerPage.as_view(), name='cancer_genomic_page'),
		url(r'images/$', views.BioCancerImagePage.as_view(), name='cancer_image_page'),
		url(r'about$', views.BioCancerabout.as_view(), name='about_page'),
		url(r'contact$', views.BioCancercontact.as_view(), name='contact_page'),
		url(r'detail/(?P<sample_id>.*)/(?P<type_id>.*)$', views.BioCancerdetail.as_view(), name='detail_page'),
		# 获取参数sample_id, type_id
        # /(?P<sample_id>.*)/(?P<type_id>\.*)}
]

