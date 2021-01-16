import os

from Utils.mongo_utils import MongoConnector

mongo_client = MongoConnector()
session_connector = mongo_client.connectors.get('sessions')
meetings_resource_connector = mongo_client.connectors.get('meetings_resource')

zoom_api_token = os.environ.get('ZOOM_API_TOKEN')
zoom_meeting_password = os.environ.get('ZOOM_MEETING_PASSWORD')
POLLING_INTERVAL_SEC = 10