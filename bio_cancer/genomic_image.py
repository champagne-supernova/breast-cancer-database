#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/28 16:17
# @Author  : 
# @Site    : find images by patient_id
# @File    : genomic_image.py
# @Software: PyCharmUPGIVEUP
import pymongo   as pg
from collections import defaultdict
import define_variables as dvs

CLIENT = pg.MongoClient(host="127.0.0.1", port=27017)

class ConnectDb:
	def __init__(self):
		self.image       = CLIENT["bcdb"]["image"]

class Patient_Image(ConnectDb):

    def __init__(self):
        self.count = []
        self.table = []
        # self.results = defaultdict(lambda: defaultdict(list))
        ConnectDb.__init__(self)

    def find_image(self, patient_id):
        tmp = self.image.find({'patient_id': patient_id})
        self.table = list(tmp)

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

    def total_count(self):
        for i in ['MR', 'MG']:
            self.count.append(self.image.count_documents({"modality": i}))
        for i in ['GE MEDICAL SYSTEMS', 'SIEMENS']:
            self.count.append(self.image.count_documents({"manufacturer": i}))

    def use(self, patient_id):
        self.find_image(patient_id)
        self.convert_astable()
        self.total_count()
        return self.table