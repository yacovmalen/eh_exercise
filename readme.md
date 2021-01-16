# Coding Exercise

This coding example represents a simple web interface to present to a user Zoom sessions that are "live" in the user's Zoom account. The user is also provided links to Zoom sessions which do not currently have any participants in the meetings.

Available sessions are Zoom meetings that are not currently "live". The "available sessions" are automatically added as resources in the application as partipants access meeting links associated with the zoom account. The page will provide the user a quick access link. 

The user can end any "live session" by pressing the "End" action button on the page. This will close the meeting in Zoom (providing the Zoom meeting a notification that the host has ended the meeting).

The web portal may take up to 30 seconds to _automatically_ refresh and display the most accurate state of the sessions.

## Quick Start
* Requirements:
** Python==3.6
** Urllib (for startup script)
** Docker

### Running the start up script
The application has been designed to run within a docker envrionment. From the Build folder, use the following commands:

_usage:_ python setup.py <start|stop> [build]

- _start:_ (Default) Starts the docker container. If no docker image exists with the correct tag, automatically runs a
                       docker build
- _stop:_ Stops and removes all running docker containers (any running container on your machine)
- _build:_ (Optional) Forces a new docker build

The following environment variables are required by the cli command:
- _PYTHONPATH_=../ 
- MONGODB_IP=<local host ip> (IP address, not localhost) 
- ZOOM_API_TOKEN=<API TOKEN FOR ZOOM>
- ZOOM_MEETING_PASSWORD=<PASSWORD FOR MEETINGS> (Zoom meeting password (appears in the zoom url "pwd=*password*"))

Command Example:
```
PYTHONPATH=../ MONGODB_IP=192.168.1.10 ZOOM_API_TOKEN=abc123 ZOOM_MEETING_PASSWORD=123abc python setup.py start build
```

## APIs
**Baseurl** : localhost:5000/api/v1

### Basic Authentication
Login does not require authentication, however the internal api calls use a simple authentication api key.

In the request header, the following field is `required`:
>'SECURITY_TOKEN_AUTHENTICATION_KEY': **[__token__]**

For this test environment, a token is auto created and inserted into the database. The header key should look like:
>{'SECURITY_TOKEN_AUTHENTICATION_KEY': 'ExampleAccess'}
