from __future__ import unicode_literals
import logging, os, re, json, urllib2, pdb

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.views.generic import View, TemplateView
from models import *
from forms import *
from bio_database import settings

logger = logging.getLogger('__name__')

class ParamsInit:
	def __init__(self, ):
		self.url = 'http://192.168.0.101:5002/blast'
		self.blast_params = {'query'  : None, 
							 'outfmt' : 0,
							 'e-value': 1e-5,
		}
		self.http_header = {'Content-Type': 'application/json', 
							'Accept'      : 'application/json',
		}
		self.home_page = 'home/index.html'
		self.blast_search = 'search/search.html'
		self.blast_results = 'blast/blast_results.html'
		self.genome_page = 'genome/genome.html'

params_info = ParamsInit()

class GenomeHomePage(TemplateView):
	template_name = params_info.genome_page

class BlastHomePage(TemplateView):
	template_name = params_info.home_page

class BlastSearch(TemplateView):
	template_name = params_info.blast_search

class BlastResults(View):
	def __init__(self, ):
		self.blast_results = []
		self.sequnce_info = []
		self.sumary_infos = {'first': '', 
							'last': ''
		} 
		
	def verify_seq_format(self, input_seq):
		pattern = re.compile('[^a-zA-Z\s\n>]')
		match_res = pattern.findall(input_seq)
		return (False if match_res else True)

	def urllib2_post(self, url, data, header):
		post_json_data = json.dumps(data)
		request = urllib2.Request(url, post_json_data, header)
		try:
			response_results = json.loads(urllib2.urlopen(request).read()).values()[0]
		except urllib2.HTTPError, e:
			logger.error(e)
		return response_results
	
	def match_target(self, source, expression):
		return [re.findall(r'%s'%exp, source)[0] for exp in expression]
	
	def parse_blast_results(self, results):
		results_to_list = results.split('>')
		expression = ['BLAST[\D|\d]+letter', '(?:Data)[\d|\D]+']
		self.sumary_infos['first'], self.sumary_infos['last'] = self.match_target(results, expression)
		
		for index, content in enumerate(results_to_list):
			if index is 0: continue
			pattern = re.compile(r'(Length=)\d+')
			infos = pattern.sub('\n', content).split('Query', 1)
			object_seq_name = infos[0].split('\n')[0].split()[0]
			expression = ['Score\s=\s(\d+)', 
						  'Expect\s=\s(.*)',
						  'Identities\s=\s\d+/\d+\s\((.*)\),'
			]
			object_seq_score, object_exp_value, object_ident_value  = self.match_target(infos[0], expression)
			header_info = {'description': object_seq_name, 
						   'max_score': object_seq_score, 
						   'total_score': object_seq_score,
					       'evalue': object_exp_value,
						   'identities': object_ident_value,
			}
			self.sequnce_info.append(header_info)
			results_body = '\nQuery' + infos[-1]

			self.blast_results.append({'results': results_body,
								 'description': header_info
			})

	def post(self, request):
		input_sequesces = request.POST.get('Sequences')
		verify_result = self.verify_seq_format(input_sequesces)
		if not verify_result:
			return HttpResponse('incorrect fasta format sequences!')
		
		if input_sequesces:
			params_info.blast_params['query'] = input_sequesces
			try:
				url_response_results = self.urllib2_post(params_info.url, 
														 params_info.blast_params,
														 params_info.http_header
				)
			except:
				return HttpResponseRedirect('/blast')
			
			self.parse_blast_results(url_response_results)
			return render(request,
						  params_info.blast_results, 
						  {'blast_results': self.blast_results, 'seq_info': self.sequnce_info}
			)
		else:
			logger.warning('No input query sequences.')
			return HttpResponseRedirect('/search')

