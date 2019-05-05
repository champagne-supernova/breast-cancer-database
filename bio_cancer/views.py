# --*--coding:UTF-8--*--
import json
import tempfile  # 用于创建临时文件和目录
from bio_home.views import *
import connect_mongo_db as md
import detail_info as di
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, FileResponse, Http404
import os.path
import genomic_image as gi
import re


# Create your views here.

class BioExprParamsInit:
    def __init__(self, ):
        self.bio_cancer_home = 'bio_cancer/bio_cancer_home.html'  # home
        self.bio_cancer_page = 'bio_cancer/bio_cancer_genomic.html'  # 基因组数据浏览页
        self.bio_cancer_image = 'bio_cancer/bio_cancer_image.html'  # 影像数据浏览页
        self.bio_cancer_about = 'bio_cancer/bio_cancer_about.html'  # about
        self.bio_cancer_contact = 'bio_cancer/bio_cancer_contact.html'  # contact
        self.bio_cancer_detail = 'bio_cancer/bio_cancer_detail.html'  # 基因组数据详情页
        self.bio_image_detail = 'bio_cancer/bio_image_detail.html'  # 影像数据详情页


params_info = BioExprParamsInit()


# 基因组数据浏览、搜索页面
class BioCancerPage(TemplateView):
    template_name = params_info.bio_cancer_page

    def __init__(self):
        self.params = md.dvs.SAMPLE_SOURCE + md.dvs.EXPERI_STRATAGY
        self.btns = None
        self.max_num = 12
        self.tmpfile = os.path.join(tempfile.gettempdir(), 'tmp_db.txt')
        self.total_count = []

    # tempfile.gettempdir()返回用于临时文件的目录的名称

    def get_data(self, form_btns):
        form_btns = [label for label in form_btns if label in self.params]
        # print(form_btns)
        mogo_obj = md.GenomicsMonoGo()
        search_res = mogo_obj.filter(*form_btns)
        self.total_count = mogo_obj.count
        with open(self.tmpfile, 'w') as fp:
            fp.write('\n'.join(form_btns))
        return form_btns, search_res

    def render_data(self, request, search_res, form_btns, objects, page_range, page):
        # for i in objects.object_list:
        #     print(i[0])
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
        paginator = Paginator(queryset, display_amount)  # 将queryset分页，每页为12个数据
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
        print(page_range)
        return objects, page_range, page

    def get(self, request):
        if 'page' in request.GET.keys():
            form_btns = [line.strip() for line in open(self.tmpfile).readlines()]
            # print(form_btns)
            form_btns, search_res = self.get_data(form_btns)
            objects, page_range, page = self.pagination(request, search_res, self.max_num)
            return self.render_data(request, search_res, form_btns, objects, page_range, page)
        else:
            form_btns = ['Primary Tumor']
            form_btns, search_res = self.get_data(form_btns)
            objects, page_range, page = self.pagination(request, search_res, self.max_num)
            return self.render_data(request, search_res, form_btns, objects, page_range, page)

    # POST 用于
    def post(self, request):
        form_btns = request.POST.keys()  # 获取checkbox选择的值 request.POST.getlist('name')，但此方法不能让CheckBox里的选项保留
        # print(form_btns)
        form_btns, search_res = self.get_data(form_btns)
        print(search_res[2])
        objects, page_range, page = self.pagination(request, search_res, self.max_num)
        return self.render_data(request, search_res, form_btns, objects, page_range, page)

class BioCancerPage_textsearch(TemplateView):
    template_name = params_info.bio_cancer_page

    def __init__(self):
        self.params = md.dvs.SAMPLE_SOURCE + md.dvs.EXPERI_STRATAGY
        self.btns = None
        self.max_num = 12
        self.tmpfile = os.path.join(tempfile.gettempdir(), 'tmp_db.txt')
        self.total_count = []

    # tempfile.gettempdir()返回用于临时文件的目录的名称

    def get_data(self, sample_id):
        mogo_obj = md.Cancer_TextSearch()
        search_res = mogo_obj.filter(*sample_id)
        self.total_count = mogo_obj.count
        with open(self.tmpfile, 'w') as fp:
            fp.write('\n'.join(sample_id))
        return sample_id, search_res

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
            objects = paginator.page(paginator.num_pages)  # paginator.num_pages:分页后的总页数
        except:
            objects = paginator.page(1)

        if page >= after_range_num:
            page_range = paginator.page_range[page - after_range_num: page + bevor_range_num]
        else:
            page_range = paginator.page_range[0: page + bevor_range_num]
        print(page_range)
        return objects, page_range, page

    def get(self, request):
        if 'page' in request.GET.keys():
            form_btns = [line.strip() for line in open(self.tmpfile).readlines()]
            form_btns, search_res = self.get_data(form_btns)
            objects, page_range, page = self.pagination(request, search_res, self.max_num)
            return self.render_data(request, search_res, form_btns, objects, page_range, page)
        else:
            form_btns = ['Primary Tumor']
            form_btns, search_res = self.get_data(form_btns)
            objects, page_range, page = self.pagination(request, search_res, self.max_num)
            return self.render_data(request, search_res, form_btns, objects, page_range, page)

    # POST 用于
    def post(self, request):
        textarea = request.POST.get('textQueryInput', None)  # 获取textarea的内容
        # print(textarea)
        sample_id = textarea.split(' ')
        # print(sample_id)
        sample_id, search_res = self.get_data(sample_id)
        # print(sample_id)
        objects, page_range, page = self.pagination(request, search_res, self.max_num)
        return self.render_data(request, search_res, sample_id, objects, page_range, page)
# 影像数据浏览、搜索页面
class BioCancerImagePage(TemplateView):
    template_name = params_info.bio_cancer_image

    def __init__(self):
        self.params = md.dvs.Manufacturer + md.dvs.Imaging_Modality
        self.btns = None
        self.max_num = 12
        self.tmpfile = os.path.join(tempfile.gettempdir(), 'tmp_db.txt')
        self.total_count = []

    # tempfile.gettempdir()返回用于临时文件的目录的名称

    def get_data(self, form_btns):
        form_btns = [label for label in form_btns if label in self.params]
        print(form_btns)
        mogo_obj = md.ImageMonoGo()
        search_res = mogo_obj.filter(*form_btns)
        self.total_count = mogo_obj.count
        with open(self.tmpfile, 'w') as fp:
            fp.write('\n'.join(form_btns))
        return form_btns, search_res

    def render_data(self, request, search_res, form_btns, objects, page_range, page):
        return render(
            request,
            params_info.bio_cancer_image,
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
            form_btns = [line.strip() for line in open(self.tmpfile).readlines()]
            form_btns, search_res = self.get_data(form_btns)
            objects, page_range, page = self.pagination(request, search_res, self.max_num)
            return self.render_data(request, search_res, form_btns, objects, page_range, page)
        else:
            form_btns = ['MR']
            form_btns, search_res = self.get_data(form_btns)
            objects, page_range, page = self.pagination(request, search_res, self.max_num)
            return self.render_data(request, search_res, form_btns, objects, page_range, page)

    def post(self, request):
        form_btns = request.POST.keys()  # 获取checkbox选择的值 request.POST.getlist('name')，但此方法不能让CheckBox里的选项保留
        form_btns, search_res = self.get_data(form_btns)
        objects, page_range, page = self.pagination(request, search_res, self.max_num)
        return self.render_data(request, search_res, form_btns, objects, page_range, page)


class BioCancerhome(TemplateView):
    template_name = params_info.bio_cancer_home


class BioCancerabout(TemplateView):
    template_name = params_info.bio_cancer_about


class BioCancercontact(TemplateView):
    template_name = params_info.bio_cancer_contact


class BioCancerdetail(TemplateView):
    template_name = params_info.bio_cancer_detail

    def get(self, request, sample_id, type_id):
        info, analysis, input_files, collection = di.Detail_Info().find_sample(sample_id, type_id)
        if sample_id[0:3] in 'TCGA':
            TCGA = True
        else:
            TCGA = False
        return render(
            request,
            params_info.bio_cancer_detail,
            {
                'info': info,
                'sample_id': sample_id,
                'analysis': analysis,
                'input_files': input_files,
                'TCGA': TCGA
            }
        )


class BioImagedetail(TemplateView):
    template_name = params_info.bio_image_detail

    def get(self, request, patient_id, serie_id):
        info, analysis, input_files, collection = di.Detail_Info().find_sample(patient_id, serie_id)
        dir_path = 'JPG/' + patient_id + '/' + serie_id
        dir_path2 = 'E:\\python_project\\bio_database\\static\\' + dir_path.replace('/', '\\')
        jpg_path = os.listdir(dir_path2)  # 找到serie_id文件夹的所有文件名，存入列表，传到html
        jpg_path2 = []
        # 判断是否有SNV数据
        snv_info, snv_analysis, snv_input_files, snv_collection = di.Detail_Info().find_sample(patient_id, 'WXS')
        if snv_info == {}:
            SNV = False
        else:
            SNV = True
        print(snv_info)
        for jpg in jpg_path:
            jpg_path2.append(dir_path + '/' + jpg)

        return render(
            request,
            params_info.bio_image_detail,
            {
                'info': info,
                'collection': collection,
                'jpg_path': jpg_path2,  # 传递所有图片地址到html
                'snv': SNV
            }
        )


class BioImagePatient(TemplateView):
    template_name = params_info.bio_cancer_image

    def __init__(self):
        self.params = md.dvs.Manufacturer + md.dvs.Imaging_Modality
        self.btns = None
        self.max_num = 12
        self.tmpfile = os.path.join(tempfile.gettempdir(), 'tmp_db.txt')
        self.total_count = []

    # tempfile.gettempdir()返回用于临时文件的目录的名称

    def get_data(self, patient_id):
        image_obj = gi.Patient_Image()
        search_res = image_obj.use(patient_id)
        self.total_count = image_obj.count
        with open(self.tmpfile, 'w') as fp:
            fp.write('\n'.join(patient_id))
        return search_res

    def render_data(self, request, search_res, objects, page_range, page):
        return render(
            request,
            params_info.bio_cancer_image,
            {
                'counts': len(search_res),
                # 'checkNames': json.dumps(form_btns),  # json.dump()将 Python 对象编码成 JSON 字符串
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

    def get(self, request, patient_id):
        search_res = self.get_data(patient_id)
        objects, page_range, page = self.pagination(request, search_res, self.max_num)
        return self.render_data(request, search_res, objects, page_range, page)

# def post(self, request):
# 	form_btns = request.POST.keys()  # 获取checkbox选择的值 request.POST.getlist('name')，但此方法不能让CheckBox里的选项保留
# 	form_btns, search_res = self.get_data(form_btns)
# 	objects, page_range, page = self.pagination(request, search_res, self.max_num)
# 	return self.render_data(request, search_res, form_btns, objects, page_range, page)


# def download(request):
# 	file = open('H:\\JPG\\TCGA-AO-A0J8\\TCGA-AO-A0J8-s1-1\\000000.jpg', 'rb')
# 	name = "000000.jpg"
# 	response = HttpResponse(file)
# 	response['Content-Type'] = 'application/octet-stream' #设置头信息，告诉浏览器这是个文件
# 	response['Content-Disposition'] = 'attachment;filename="{0}"'.format(name)
# 	return response

# 内部使用迭代器进行数据流传输
def download_image(request, serie_id):
    try:
        file_path = 'H:\\my_DOI\\' + serie_id[:12] + '\\' + serie_id[:15] + '\\' + serie_id + '.zip'
        file = open(file_path, 'rb')
        name = serie_id + ".zip"
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(name)
        return response
    except Exception:
        raise Http404


def download_tcga(request, sample_id, type_id, the_name):
    if type_id == 'Methylation Array':
        dir_path = 'H:\\TCGA_Genomic\\methy\\' + sample_id[:12]
        dir_parent = ''
        print(dir_path)
        for parent, dirnames, filenames in os.walk(dir_path):
            dir_parent = parent
            if sample_id[13] == 'T':
                file_name = [name for name in filenames if re.search(r'TCGA(.{9})01', name)][0]
                break
            elif sample_id[13] == 'M':
                file_name = [name for name in filenames if re.search(r'TCGA(.{9})06', name)][0]
                break
            elif sample_id[13] == 'N':
                file_name = [name for name in filenames if re.search(r'TCGA(.{9})11', name)][0]
                break
        file_path = os.path.join(dir_parent, file_name)
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response

    elif type_id == 'WXS':
        file_path = r'H:\TCGA_Genomic\SNV\gdc_download_20190118_084832.271889.tar.gz'
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
        response['Content-Disposition'] = 'attachment;filename="TCGA-SNV.tar.gz"'
        return response

    elif type_id == 'RNA-Seq':
        dir_path = os.path.join('H:\TCGA_Genomic\RNA\gdc', sample_id[:12])
        tmp = the_name.split('.')
        print(tmp)
        tmp2 = sample_id+'.' + tmp[1] + '.' + tmp[2] + '.' + tmp[3]
        print(tmp2)
        file_path = os.path.join(dir_path, tmp2)
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(tmp2)
        return response