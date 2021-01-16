from flask import redirect
from flask_restful import Resource

from config import session_connector, meetings_resource_connector
from Utils.authentication import is_authenticated
from Resources.errors import BadRequestError
from Utils.zoom_connector import ZoomConnector


class SessionEnd(Resource):
    decorators = [is_authenticated]

    def get(self, meeting_id=None):
      raise NotImplementedError()
        
    def post(self, meeting_id=None):
        # Check if meeting exists
        session_connector.get_one_or_all_entities({"entity_id": meeting_id})

        # TODO: API Call to Zoom to end the meeting

        self._end_meeting(meeting_id)
        return redirect('/')

    def _end_meeting(self, meeting_id=None):
      if not meeting_id or session_connector._is_exist(meeting_id):
        raise BadRequestError('Invalid id')
      
      ZoomConnector.end_meeting(meeting_id)
      session_connector.end_session({'entity_id': meeting_id})
      meetings_resource_connector.release_meeting(meeting_id)

      return session_connector
