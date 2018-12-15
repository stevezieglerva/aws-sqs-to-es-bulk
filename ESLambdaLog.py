import boto3
import re
import json
from datetime import datetime
from aws_requests_auth.aws_auth import AWSRequestsAuth
from elasticsearch import Elasticsearch, RequestsHttpConnection
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth
from LocalTime import *
import structlog

class ESLambdaLog:
	def __init__(self, index_name = "aws_lambda_start"):
		self.index_name = index_name + "." + self.get_index_name_timestamp_label()
		es_host = 'search-ziegler-es-bnlsbjliclp6ebc67fu3mfr74u.us-east-1.es.amazonaws.com'
		auth = BotoAWSRequestsAuth(aws_host=es_host,
											aws_region='us-east-1',
											aws_service='es')

		self.es = Elasticsearch(host=es_host, use_ssl=True, port=443, connection_class=RequestsHttpConnection, http_auth=auth)	
		self.add_index_if_doesnt_exist()


	def add_index_if_doesnt_exist(self):
		indices = self.list_indices()
		if self.index_name not in indices:
			mappings = {
					"mappings": {
						"doc": {
							"properties": {
								"@timestamp": {
									"type": "date"
							}
						}
					}
				}
			}
			self.es.indices.create(self.index_name, body=mappings)

	def get_timestamp(self):
		local_time = LocalTime()
		return local_time.utc.strftime("%Y-%m-%dT%H:%M:%S.%f")

	def get_index_name_timestamp_label(self):	
		local_time = LocalTime()
		return local_time.utc.strftime("%Y.%m.%d")

	def log_event(self, event):
		local_time = LocalTime()
		event["@timestamp"] = self.get_timestamp()
		self.es.index(index=self.index_name, doc_type = "doc", body = event)

	def list_indices(self):
		results = self.es.indices.get(index = "*")
		list = []
		for index_name in results.keys():
			list.append(index_name)
		return list

