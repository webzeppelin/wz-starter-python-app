"""Entry point for the server application."""

import logging
from gevent.wsgi import WSGIServer
from flask import request, Response, jsonify
from datetime import datetime
import time
from pytz import timezone
from tzlocal import get_localzone
from .config import configure_app, app, HOSTNAME, PORT
from .utils import html_codes
from .models import HealthStatus, ServerTime


@app.before_first_request
def set_up():
    """Configure the application to be used by the application."""
    configure_app(app)


@app.route('/api/v1/health', methods=['GET'])
def get_health():
    """Return service health information."""
    ret = HealthStatus(is_up=True)
    return jsonify(**(ret.to_dict()))

@app.route('/api/v1/time', methods=['GET'])
def get_time():
    """Return the current server time in the server's timezone"""
    tz = get_localzone()
    t = datetime.now(tz)
    #t = tz.localize(t, is_dst=None)

    d = ServerTime(hour=t.hour,
                      minute=t.minute,
                      second=t.second,
                      tz_name=tz.zone,
                      tz_offset=tz.utcoffset(datetime.now()).total_seconds()/3600).to_dict()
    return jsonify(**d)


def main():
    """Main entry point of the app."""
    try:
        http_server = WSGIServer((HOSTNAME, PORT),
                                 app,
                                 log=logging,
                                 error_log=logging)

        http_server.serve_forever()
    except Exception as exc:
        logging.error(exc.message)
    finally:
        # get last entry and insert build appended if not completed
        # Do something here
        pass
