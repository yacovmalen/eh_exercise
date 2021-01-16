from flask import make_response, render_template, request
from flask_restful import Resource

from config import meetings_resource_connector
from Utils.authentication import is_authenticated


class AvailableSessions(Resource):
    decorators = [is_authenticated]

    def get(self):
      get_active = request.args.get('active', True)
      if get_active:
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('available.html', available_sessions=meetings_resource_connector.get_one_or_all_entities({'locked': False})), 200, headers)
      else:
        pass  # Todo: get entities where delete exists and is less than 1 hour old 