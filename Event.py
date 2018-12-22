import boto3
from LocalTime import *

class Event:

	def __init__(self, dynamoDB_table = "", event_text = ""):
		if dynamoDB_table != "" and event_text != "":
			db = boto3.client("dynamodb")
			local_time = LocalTime()
			response = db.put_item(TableName = dynamoDB_table, 
				Item = {"s3-url" : {"S" : event_text}, 
				"ttl" : {"N" : str(local_time.get_utc_epoch())}, 
				"timestamp" : {"S" : str(local_time.utc)}, 
				"timestamp_local" : {"S" : str(local_time.local)}})
		
	def purge_event(self, dynamoDB_table, event_text):
		db = boto3.client("dynamodb")
		response = db.delete_item(TableName = dynamoDB_table, 
			Key = {"s3-url" : {"S" : event_text}})
		
