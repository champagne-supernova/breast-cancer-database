# --*--coding:UTF-8--*--
import json
import tempfile  # 用于创建临时文件和目录
from bio_home.views import *
import connect_mongo_db as md
import detail_info as di
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
# Create your views here.

class BioExprParamsInit:
	def __init__(self, ):
		self.bio_cancer_home = 'bio_cancer/bio_cancer_home.html'
		self.bio_cancer_page = 'bio_cancer/bio_cancer_genomic.html'
		self.bio_cancer_image = 'bio_cancer/bio_cancer_image.html'
		self.bio_cancer_about = 'bio_cancer/bio_cancer_about.html'
		self.bio_cancer_contact = 'bio_cancer/bio_cancer_contact.html'
		self.bio_cancer_detail = 'bio_cancer/bio_cancer_detail.html'
params_info = BioExprParamsInit()

class BioCancerPage(TemplateView):	
	template_name = params_info.bio_cancer_page

	def __init__(self):
		self.params  = md.dvs.SAMPLE_SOURCE + md.dvs.EXPERI_STRATAGY
		self.btns    = None
		self.max_num = 12
		self.tmpfile = os.path.join(tempfile.gettempdir(), 'tmp_db.txt')
		self.total_count =[]
		# tempfile.gettempdir()返回用于临时文件的目录的名称

	def get_data(self, form_btns):
		form_btns = [ label for label in form_btns if label in self.params ]
		mogo_obj = md.GenomicsMonoGo()
		search_res = mogo_obj.filter(*form_btns)
		self.total_count = mogo_obj.count
		print("total count:")
		print(self.total_count)
		with open(self.tmpfile, 'w') as fp:
			fp.write('\n'.join(form_btns))
		return form_btns, search_res
	
	def render_data(self, request, search_res, form_btns, objects, page_range, page):
		return render(
			request, 
			params_info.bio_cancer_page,
			{
				'counts': len(search_res),
				'checkNames': json.dumps(form_btns),  # json.dump()将 Python 对象编码成 JSON 字符串
				'objects': objects,
				'page_range': page_range,
				'max_page': page * self.max_num,
				'min_page': (page - 1) * self.max_num + 1,
				'total_count': self.total_count  # simple search中各选项数量统计
			}
		)
		
	def pagination(self, request, queryset, display_amount, after_range_num=5, bevor_range_num=4):
		paginator = Paginator(queryset, display_amount)	
		try:
			page = int(request.GET.get('page'))
		except:
			page = 1
		try:
			objects = paginator.page(page)
		except EmptyPage:
			objects = paginator.page(paginator.num_pages)
		except:
			objects = paginator.page(1)

		if page >= after_range_num:
			page_range = paginator.page_range[page - after_range_num: page + bevor_range_num]
		else:
			page_range = paginator.page_range[0: page + bevor_range_num]
		return objects, page_range, page

	def get(self, request):
		if 'page' in request.GET.keys():
			form_btns = [ line.strip() for line in open(self.tmpfile).readlines() ]
			form_btns, search_res = self.get_data(form_btns)
			objects, page_range, page = self.pagination(request, search_res, self.max_num)
			return self.render_data(request, search_res, form_btns, objects, page_range, page)
		else:
			form_btns = ['Primary Tumor']
			form_btns, search_res = self.get_data(form_btns)
			objects, page_range, page = self.pagination(request, search_res, self.max_num)
			return self.render_data(request, search_res, form_btns, objects, page_range, page)

	def post(self, request):
		form_btns = request.POST.keys()  # 获取checkbox选择的值 request.POST.getlist('name')，但此方法不能让CheckBox里的选项保留
		form_btns, search_res = self.get_data(form_btns)
		objects, page_range, page = self.pagination(request, search_res, self.max_num)
		return self.render_data(request, search_res, form_btns, objects, page_range, page)

class BioCancerImagePage(TemplateView):
	template_name = params_info.bio_cancer_image

class BioCancerhome(TemplateView):
	template_name = params_info.bio_cancer_home

class BioCancerabout(TemplateView):
	template_name = params_info.bio_cancer_about

class BioCancercontact(TemplateView):
	template_name = params_info.bio_cancer_contact

class BioCancerdetail(TemplateView):
	template_name = params_info.bio_cancer_detail

	def get(self, request, sample_id, type_id):
		print(type_id)
		print(sample_id)
		info, analysis, input_files = di.Detail_Info().find_sample(sample_id, type_id)
		# print(info)
		# print(analysis)

		return render(
			request,
			params_info.bio_cancer_detail,
			{
				'info': info,
				'sample_id': sample_id,
				'analysis': analysis,
				'input_files': input_files
			}
		)
