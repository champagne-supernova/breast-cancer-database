# --*--coding:UTF-8--*--
# #!/usr/bin/env python
#title       : connect_mongo_db.py 
#description : Connect mongo database and render the results on the templates
#author      : Huamei Li
#date        : 22/01/2019
#type        : main script
#version     : 2.7

####################################################################
# load python modules

import pdb
import pymongo   as pg
import numpy     as np
from collections import defaultdict

####################################################################
# load own modules

import define_variables as dvs

####################################################################

CLIENT = pg.MongoClient(host="127.0.0.1", port=27017)

class ConnectDb:
	def __init__(self):
		self.image       = CLIENT["bcdb"]["image"]
		self.TCGA_RNA    = CLIENT["bcdb"]["TCGA_RNA"]
		self.TCGA_SNV    = CLIENT["bcdb"]["TCGA_SNV"]
		self.TCGA_meth   = CLIENT["bcdb"]["TCGA_meth"]
		self.epigenetics = CLIENT["bcdb"]["epigenetics"]
		self.hi_c = CLIENT["bcdb"]["hi_c"]

class GenomicsMonoGo(ConnectDb):
	def __init__(self):
		self.results = defaultdict(lambda: defaultdict(list))  # 表示键对应的值为字典，该字典中键对应的值为列表
		# defaultdict在普通的dict之上添加了默认工厂，使得键不存在时会自动生成相应类型的值，此时为list
		self.table = []
		self.count = []
		ConnectDb.__init__(self)

	def total_count(self):
		self.count.append(self.TCGA_RNA.count_documents({}) + self.TCGA_SNV.count_documents({}) + \
						  self.TCGA_meth.count_documents({}))
		for i in ['T-47D', 'MDA-MB-231', 'HMLE breast cancer cell line', 'MCF-7', 'ZR-75-1', 'TAMR', 'WS8']:
			self.count.append(self.epigenetics.count_documents({"sample_source": i}) \
							  + self.hi_c.count_documents({"sample_source": i}))
		self.count.append(self.TCGA_RNA.count_documents({}))
		self.count.append(self.TCGA_SNV.count_documents({}))
		self.count.append(self.TCGA_meth.count_documents({}))
		for i in ['DNase-Hypersensitivity', 'ATAC-seq', '3C', 'Hi-C']:
			self.count.append(self.epigenetics.count_documents({"assay_type": i}) \
							  + self.hi_c.count_documents({"librarystrategy": i}))

	def sample_source(self, *args):
		for src in args[0]:
			if src in ['Primary Tumor', 'Metastatic', 'Solid Tissue Normal']:
				tmp_val = list(self.TCGA_SNV.find({'sample_source': src.lower()})) + \
						  list(self.TCGA_RNA.find({'sample_source': src.lower()})) + \
						  list(self.TCGA_meth.find({'sample_source': src.lower()}))
			else:
				tmp_val = list(self.epigenetics.find({'sample_source': src})) + list(self.hi_c.find({'sample_source': src}))
			self.results[src] = tmp_val

	def exper_strategy(self, *args):
		for src in args[0]:
			tmp_val = []
			if src in ['3C', 'Hi-C']:
				tmp_val = self.hi_c.find({'librarystrategy': src})
			elif src in ['DNase', 'ATAC-seq']:
				src = 'DNase-Hypersensitivity' if src == 'DNase' else src
				tmp_val = self.epigenetics.find({'assay_type': src})
			elif src in ['RNA-seq']:
				tmp_val = self.TCGA_RNA.find()
			elif src in ['SNV']:
				tmp_val = self.TCGA_SNV.find()
			elif src in ['DNA-methy']:
				tmp_val = self.TCGA_meth.find()
			if tmp_val:
				self.results[src] = list(tmp_val)
			
	def sample_intersect_expr(self, *args):	
		sample_class = [name for name in args[0] if name in dvs.SAMPLE_SOURCE]
		exper_class = [name for name in args[0] if name in dvs.EXPERI_STRATAGY]
		if not sample_class:
			[self.table.extend(self.results[exp]) for exp in self.results]
		elif not exper_class:
			[self.table.extend(self.results[sn]) for sn in self.results]

		else:
			for sn in sample_class:
				for exp in exper_class:
					exp = 'DNase-Hypersensitivity' if exp == 'DNase' else exp
					ovp_res = np.intersect1d(np.array(self.results[sn]), np.array(self.results[exp])).tolist()
					if not ovp_res:
						continue
					self.table.extend(ovp_res)

	def convert_astable(self):
		tablelst = []
		for infos in self.table:
			key_names = infos.keys()  # keys()函数以列表返回一个字典所有的键。
			for label, values in dvs.GROUP_NAMES.iteritems():
				ovp_names = set(key_names) & set(values)
				if len(ovp_names) == len(values):
					key_names = values
					break
			if len(key_names) == 3:
				tmp_val = [infos[key_names[0]], infos[key_names[1]], '-', infos[key_names[2]] ]
			else:
				tmp_val = [infos[key] for key in key_names]
			tablelst.append(tmp_val)
		self.table = tablelst
	
	def filter(self, *args):
		self.total_count()
		self.sample_source(args)
		self.exper_strategy(args)
		self.sample_intersect_expr(args)
		self.convert_astable()
		return self.table

	def text_search(self, *args):
		for sample_id in args[0]:
			tmp_val = list(self.TCGA_SNV.find({'patient_id': sample_id})) \
					  + list(self.TCGA_RNA.find({'patient_id': sample_id}))\
					  + list(self.TCGA_meth.find({'patient_id': sample_id}))\
					  + list(self.epigenetics.find({'sample_id': sample_id}))\
					  + list(self.hi_c.find({'sample_id': sample_id}))
			self.results[sample_id] = tmp_val

class ImageMonoGo(ConnectDb):
	def __init__(self):
		self.results = defaultdict(lambda: defaultdict(list))  # 表示键对应的值为字典，该字典中键对应的值为列表
		# defaultdict在普通的dict之上添加了默认工厂，使得键不存在时会自动生成相应类型的值，此时为list
		self.table = []
		self.count = []
		ConnectDb.__init__(self)

	def total_count(self):
		for i in ['MR', 'MG']:
			self.count.append(self.image.count_documents({"modality": i}))
		for i in ['GE MEDICAL SYSTEMS', 'SIEMENS']:
			self.count.append(self.image.count_documents({"manufacturer": i}))

	def manufacturer(self, *args):
		for src in args[0]:
			if src in ['GE MEDICAL SYSTEMS', 'SIEMENS']:
				self.results[src] = list(self.image.find({'manufacturer': src}))

	def modality(self, *args):
		for src in args[0]:
			if src in ['MR', 'MG']:
				self.results[src] = list(self.image.find({'modality': src}))

	def modality_intersect_manufacturer(self, *args):
		modality_class = [name for name in args[0] if name in dvs.Imaging_Modality]
		manufacturer_class = [name for name in args[0] if name in dvs.Manufacturer]
		if not manufacturer_class:
			[self.table.extend(self.results[exp]) for exp in self.results]
		elif not modality_class:
			[self.table.extend(self.results[sn]) for sn in self.results]
		else:
			for sn in modality_class:
				for exp in manufacturer_class:
					ovp_res = np.intersect1d(np.array(self.results[sn]), np.array(self.results[exp])).tolist()
					if not ovp_res:
						continue
					self.table.extend(ovp_res)

	def convert_astable(self):
		tablelst = []
		for infos in self.table:
			tmp_val = []
			tmp_val.append(infos['patient_id'])
			tmp_val.append(infos['serie_id'])
			tmp_val.append(infos['modality'])
			tmp_val.append(infos['description'])
			tmp_val.append(infos['manufacturer'])
			tmp_val.append(infos['size'])
			tablelst.append(tmp_val)
		self.table = tablelst

	def filter(self, *args):
		self.total_count()
		self.manufacturer(args)
		self.modality(args)
		self.modality_intersect_manufacturer(args)
		self.convert_astable()
		return self.table

class Cancer_TextSearch(GenomicsMonoGo):
	# 输入:类型为list的sample_id，输出:查询结果
	# 功能：实现sample_id的关键字检索
	def __init__(self):
		GenomicsMonoGo.__init__(self)

	def text_search(self, *args):
		tablelist = []
		for sample_id in args[0]:
			tmp_val = list(self.TCGA_SNV.find({'patient_id': sample_id})) \
					  + list(self.TCGA_RNA.find({'patient_id': sample_id}))\
					  + list(self.TCGA_meth.find({'patient_id': sample_id}))\
					  + list(self.epigenetics.find({'sample_id': sample_id}))\
					  + list(self.hi_c.find({'sample_id': sample_id}))
			tablelist = tmp_val + tablelist
		self.table = tablelist
	def filter(self, *args):
		self.total_count()
		self.text_search(args)
		self.convert_astable()
		return self.table