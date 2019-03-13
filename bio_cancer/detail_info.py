#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/4 16:51
# @Author  : 
# @Site    : find sample info in database
# @File    : detail_info.py
# @Software: PyCharmUPGIVEUP

import pymongo as pg

CLIENT = pg.MongoClient(host="127.0.0.1", port=27017)


class ConnectDb:
    def __init__(self):
        self.image = CLIENT["bcdb"]["image"]
        self.TCGA_RNA = CLIENT["bcdb"]["TCGA_RNA"]
        self.TCGA_SNV = CLIENT["bcdb"]["TCGA_SNV"]
        self.TCGA_meth = CLIENT["bcdb"]["TCGA_meth"]
        self.epigenetics = CLIENT["bcdb"]["epigenetics"]
        self.hi_c = CLIENT["bcdb"]["hi_c"]


class Detail_Info(ConnectDb):

    def __init__(self):
        self.info = {}
        self.analysis = {}
        self.input_files = {}
        ConnectDb.__init__(self)

    def find_sample(self, sample_id, type_id):
        tmp_val = {}
        if type_id in ['3C', 'Hi-C']:
            tmp_val = list(self.hi_c.find({'sample_id': sample_id}))[0]
        elif type_id in ['DNase-Hypersensitivity', 'ATAC-seq']:
            tmp_val = list(self.epigenetics.find({'sample_id': sample_id}))[0]
        elif type_id in ['RNA-Seq']:
            tmp_val = list(self.TCGA_RNA.find({'patient_id': sample_id}))[0]
            tmp_val['file_size'] = str(int(tmp_val['file_size']) / 1024) + 'MB'
            self.analysis = tmp_val['analysis'][0]
            del tmp_val['analysis']
            self.input_files = tmp_val['input_files'][0]
            del tmp_val['input_files']
        elif type_id in ['WXS']:
            tmp_val = list(self.TCGA_SNV.find({'patient_id': sample_id}))[0]
            tmp_val['file_size'] = str(int(tmp_val['file_size']) / 1024) + 'MB'
            self.analysis = tmp_val['analysis'][0]
            del tmp_val['analysis']
            self.input_files = tmp_val['input_files'][0]
            del tmp_val['input_files']
        elif type_id in ['Methylation Array']:
            tmp_val = list(self.TCGA_meth.find({'patient_id': sample_id}))[0]
            tmp_val['file_size'] = str(int(tmp_val['file_size'])/1024)+'MB'
            self.analysis = tmp_val['analysis'][0]
            del tmp_val['analysis']
        if tmp_val:
            del tmp_val['_id']
        self.info = tmp_val
        return self.info, self.analysis, self.input_files
