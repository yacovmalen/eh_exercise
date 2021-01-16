"""
Index - returns 200 and the index.html page
"""
from flask import render_template, make_response
from flask_restful import Resource

from config import session_connector, meetings_resource_connector

class Index(Resource):
  def get(self):
    headers = {'Content-Type': 'text/html'}
    return make_response(render_template('index.html', live_sessions=session_connector.get_one_or_all_entities(), available_session=meetings_resource_connector.get_one_or_all_entities({'locked': False})), 200, headers)
    