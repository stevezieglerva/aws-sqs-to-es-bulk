import boto3
import time
import datetime
import logging
import structlog
import os
import json
from S3TextFromLambdaEvent import *
from Event import *


def lambda_handler(event, context):
	try:
		print("Started")
		if "text_logging" in os.environ:
			log = structlog.get_logger()
		else:
			log = setup_logging()
		log = log.bind(lambda_name="aws-code-index-stream-bulk-load")
		aws_request_id = ""
		if context is not None:
			aws_request_id = context.aws_request_id
			log = log.bind(aws_request_id=aws_request_id)
		
		log.critical("started", input_events=json.dumps(event, indent=3))


		#print(json.dumps(event, indent=3))
		s3 = boto3.resource("s3")
		s3_urls_to_process = []
		for event in event["Records"]:
			if event["eventName"] == "INSERT":
				s3_url = event["dynamodb"]["Keys"]["s3-url"]["S"]
				print("Found: " + s3_url)
				s3_urls_to_process.append(s3_url)

		if len(s3_urls_to_process) > 0:
			file_texts = get_file_text_from_s3_urls(s3_urls_to_process, s3)
			combined_text = ""
			for file in file_texts:
				combined_text = combined_text + "\n____\n" + file + "\n" + file_texts[file] 
			print("combined_text length: " + str(len(combined_text)))
			combined_file_name = "combined-files/" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + "-" + aws_request_id + ".txt"
			print("combined file name:" + combined_file_name)
			create_s3_text_file("code-index", combined_file_name, combined_text, s3)

			e = Event("", "")
			for file in s3_urls_to_process:
				e.purge_event("code-index", file)
			result = {"msg" : "Success", "input_file_count" : len(s3_urls_to_process), "processed_file_count" : len(file_texts)}
			log.critical("finished", result=result)
		else:
			print("No INSERT events")
			result = {"msg" : "Success - No INSERT events", "file_count" : 0}
			log.critical("finished_no_insert_events", result=result)

		print("Finished")

	except Exception as e:
		print("Exception: "+ str(e))
		raise(e)

	return result




def setup_logging():
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO
    )
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    return structlog.get_logger()

	