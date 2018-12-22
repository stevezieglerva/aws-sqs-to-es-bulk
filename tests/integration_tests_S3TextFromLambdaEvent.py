import unittest
import time
from S3TextFromLambdaEvent import *
import boto3



class TestMethods(unittest.TestCase):

	def test_get_file_text_from_s3_bucket_and_key__one_file__one_file_text_returned(self):
		# Arrange
		s3 = boto3.resource('s3')
		bucket = "code-index"
		key = "prep-input\\integration_test_S3TextFromLambdaEvent.txt"
		file_text = "test_1.txt file contents\n2nd line"
		create_s3_text_file(bucket, key, file_text, s3)

		s3_list = {}
		s3_url = "https://s3.amazonaws.com/" + bucket + "/" + key
		s3_list[s3_url] = {"bucket" : bucket, "key" : key}
				
		# Act
		result = get_file_text_from_s3_bucket_and_key(s3_list, s3)
		print(result)

		# Assert
		self.assertEqual(len(result), 1)
		self.assertEqual(result[s3_url], file_text)

	def test_get_file_text_from_s3_urls__one_file__one_file_text_returned(self):
		# Arrange
		s3 = boto3.resource('s3')
		bucket = "code-index"
		key = "prep-input\\integration_test_S3TextFromLambdaEvent.txt"
		file_text = "test_1.txt file contents\n2nd line"
		create_s3_text_file(bucket, key, file_text, s3)
		

		s3_list = [1]
		s3_url = "https://s3.amazonaws.com/" + bucket + "/" + key
		s3_list[0] = s3_url
				
		# Act
		result = get_file_text_from_s3_urls(s3_list, s3)
		print(result)

		# Assert
		self.assertEqual(len(result), 1)
		self.assertEqual(result[s3_url], file_text)		

	def test_get_file_text_from_s3_urls__bad_url__file_text_is_empty(self):
		# Arrange
		s3 = boto3.resource('s3')
		s3_list = [1]
		s3_url = "https://s3.amazonaws.com/code-index/bad_key" 
		s3_list[0] = s3_url
				
		# Act
		result = get_file_text_from_s3_urls(s3_list, s3)
		print(result)

		# Assert
		self.assertEqual(len(result), 0)



if __name__ == '__main__':
	unittest.main()		


