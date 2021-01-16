import json
import requests
import threading
import time

from config import meetings_resource_connector, session_connector, zoom_api_token, zoom_meeting_password

ZOOM_BASE_URL = "https://api.zoom.us"
MEETING_DETAILS_API = f'{ZOOM_BASE_URL}/v2/metrics/meetings'
MEETING_END_API = ZOOM_BASE_URL + '/v2/meetings/{meeting_id}/status'
MEETING_URL = "https://zoom.us/j/{}?pwd={}"


class ZoomConnector(object):
  def __init__(self):
    self.running = True

  def run(self):
    """
    A polling thread that constantly checks Zoom for meetings and updates the state and participants, locking and release meetings as necessary
    """
    def _poll_for_live_meetings():
      # Todo poll zoom ever X seconds for active meetings
      # Update the database
      print('Polling for Live Zoom Meetings')

      headers = {'authorization': 'Bearer {}'.format(zoom_api_token)}
      res = requests.get(MEETING_DETAILS_API, headers=headers)

      meetings = res.json().get('meetings', [])
      known_meetings = list(map(lambda m: requests.get('{}/{}'.format(MEETING_DETAILS_API, m.get('entity_id')), headers=headers).json(), meetings_resource_connector.get_one_or_all_entities()))

      for meeting in list({v['id']:v for v in meetings + known_meetings}.values()):
        if meeting.get('participants', 0) > 0:
          meetings_resource_connector.lock_meeting(meeting.get("id"), url=MEETING_URL.format(meeting.get("id"), zoom_meeting_password))
          session_connector.update_participants(meeting.get("id"), meeting.get('participants'))
        else:
          meetings_resource_connector.release_meeting(meeting.get("id"))
          session_connector.end_session(meeting.get("id"), meeting.get('participants', 0))

    while self.running:
      t = threading.Thread(target=_poll_for_live_meetings)
      t.start()
      t.join()
      time.sleep(30)
  
  @staticmethod
  def end_meeting(meeting_id):
    if zoom_api_token:
      print('Ending meeting: {}'.format(meeting_id))
      url = MEETING_END_API.format(meeting_id=meeting_id)
      headers = {'authorization': 'Bearer {}'.format(zoom_api_token), 'Content-Type': 'application/json'}
      body = json.dumps({'action': 'end'})
      res = requests.put(url, headers=headers, data=body)
      if res.status_code != 204:
        # Simple retry mechanism
        return requests.put(url, headers=headers, data=body)
  
      return res


  def start_meeting(self, meeting_id):
    # Todo: Trigger new zoom meeting
    pass
