"""
Service health check - returns 200 if service is up
"""
from flask.views import MethodView
from Utils.authentication import is_authenticated


class HealthCheck(MethodView):
    decorators = [is_authenticated]

    def get(self):
        return 'ok', 200