#!/usr/bin/env python
#title       : define_variables.py 
#description : Pre-define variables for program
#author      : Huamei Li
#date        : 22/01/2019
#type        : main script
#version     : 2.7

####################################################################

SAMPLE_SOURCE = [
		'Primary Tumor'               ,
		'Solid Tissue Normal',
		'Metastatic',
		'T-47D'                       , 
		'MDA-MB-231'                  , 
		'HMLE breast cancer cell line',
		'MCF-7'                       , 
		'ZR-75-1'                     , 
		'TAMR'                        , 
		'WS8'
	]

EXPERI_STRATAGY = [
		'RNA-seq'  ,
		'SNV'      , 
		'DNA-methy', 
		'DNase'    , 
		'ATAC-seq' , 
		'3C'       , 
		'Hi-C'
	]

Imaging_Modality = [
		'MR',
		'MG'
]

Manufacturer = [
		'GE MEDICAL SYSTEMS',
		'SIEMENS'
]

COMMON_IMAGES  = ['serie_id', 'description', 'modality', 'size']
COMMON_GENOMIC = ['sample id', 'description', 'platform', 'sample_source']

GROUP_NAMES = {
		'TCGA_RNA'   : ['patient_id', 'experimental_strategy', 'platform', 'sample_source'],
		'TCGA_meth'  : ['patient_id', 'experimental_strategy', 'platform', 'sample_source'],
		'TCGA_SNV'   : ['patient_id', 'experimental_strategy', 'sample_source'],
		'epigenetics': ['sample_id', 'assay_type', 'instrument', 'sample_source'],
		'Hi_C'       : ['sample_id', 'librarystrategy', 'model', 'sample_source']
	}



