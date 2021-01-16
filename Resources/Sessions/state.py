from flask import make_response, render_template, request
from flask_restful import Resource

from config import session_connector
from Utils.authentication import is_authenticated


class SessionState(Resource):
    decorators = [is_authenticated]

    def get(self):
      get_active = request.args.get('active', True)
      if get_active:
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('sessions.html', live_sessions=session_connector.get_one_or_all_entities()), 200, headers)
      else:
        pass  # Todo: get entities where delete exists and is less than 1 hour old 