import unittest
import time
import boto3
from lambda_function import *
import json

event_one_file = {
  "Records": [
    {
      "eventID": "1",
      "eventVersion": "1.0",
      "dynamodb": {
        "Keys": {
          "s3-url": {
            "S": "https://s3.amazonaws.com/code-index/prep-output/sqs_bulk_integration_test_1.txt"
          }
        },
        "NewImage": {
          "Message": {
            "S": "New item!"
          },
          "s3-url": {
            "S": "http:"
          }
        },
        "StreamViewType": "NEW_AND_OLD_IMAGES",
        "SequenceNumber": "111",
        "SizeBytes": 26
      },
      "awsRegion": "us-east-1",
      "eventName": "INSERT",
      "eventSourceARN": "arn:aws:dynamodb:us-east-1:account-id:table/ExampleTableWithStream/stream/2015-06-27T00:48:05.899",
      "eventSource": "aws:dynamodb"
    }
  ]
}

class TestMethods(unittest.TestCase):

	def test_lambda_function__one_file_event__successful_results(self):
		# Arrange
		s3 = boto3.resource('s3')
		bucket = "code-index"
		key = "prep-input/sqs_bulk_integration_test_1.txt"
		file_text = "import java;\nprint('Hello world'); \n if x <> 5\n-;-"
		file_text_binary = bytes(file_text, 'utf-8')
		object = s3.Object(bucket, key)
		object.put(Body=file_text_binary)


		# Act
		result = lambda_handler(event_one_file, "Integration Test")
		print(json.dumps(result, indent=3))

		# Assert
		self.assertEqual(result["msg"], "Success")

if __name__ == '__main__':
	unittest.main()		


