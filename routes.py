
"""
Routes file - Manage api routes mapped to application functions
Apis are created using Flask-RESTful
"""
import threading

from flask import Flask, Blueprint
from flask_restful import Api

from config import zoom_api_token
from Resources.index import Index
from Resources.errors import ErrorDefinitions
from Resources.health import HealthCheck
from Resources.Sessions.get_available import AvailableSessions
from Resources.Sessions.end import SessionEnd
from Resources.Sessions.state import SessionState
from Utils.zoom_connector import ZoomConnector

# Server application creation and setup
app = Flask(__name__)
version_one = Blueprint('api', __name__, url_prefix='/api/v1')
api_v_one = Api(version_one, errors=ErrorDefinitions.errors)
app.register_blueprint(version_one)

routes_one = Blueprint('routes_api', __name__)
routes_v_one = Api(routes_one, errors=ErrorDefinitions.errors)
app.register_blueprint(routes_one)
# End server setup

###
# Index
###
routes_v_one.add_resource(Index, '/')

# Health Check
api_v_one.add_resource(HealthCheck, '/isalive')

###
# Sessions Apis
###
api_v_one.add_resource(AvailableSessions, '/sessions/get-available')
api_v_one.add_resource(SessionEnd, '/sessions/<int:meeting_id>/end')
api_v_one.add_resource(SessionState, '/sessions/state')

if zoom_api_token:
  zoom_poller = ZoomConnector()
  
  t = threading.Thread(target=zoom_poller.run)
  t.start()
  
if __name__ == '__main__':
  app.run("0.0.0.0", port=5000, debug=False)
