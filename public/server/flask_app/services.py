"""Entry point for the server application."""

import logging
from gevent.wsgi import WSGIServer
from flask import request, Response, jsonify
from .config import configure_app, app, HOSTNAME, PORT
from .utils import html_codes
from .models import HealthStatus


@app.before_first_request
def set_up():
    """Configure the application to be used by the application."""
    configure_app(app)


@app.route('/api/v1/health', methods=['GET'])
def get_health():
    """Return service health information."""
    ret = HealthStatus(is_up=True)
    return jsonify(**(ret.to_dict()))


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
