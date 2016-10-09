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
from .models import HealthStatus, ServerTime, GuestbookEntry, GuestbookEntrySet


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

    st = ServerTime(hour=t.hour,
                      minute=t.minute,
                      second=t.second,
                      tz_name=tz.zone,
                      tz_offset=tz.utcoffset(datetime.now()).total_seconds()/3600)
    return jsonify(st.to_dict())

@app.route('/api/v1/guestbook', methods=['POST'])
def sign_guestbook():
    """Accept a new guestbook entry posted to the API and return the new entry"""
    print('Signing the guestbook')
    payload = request.get_json(force=True)
    if payload is None:
        return error_response(400, 'Missing guestbook entry in POST payload')

    name = payload.get('name')
    message = payload.get('message')

    if not name or not message:
        return error_response(400, 'Missing required parameters')

    entry = GuestbookEntry(
        id=123,
        name=name,
        message=message,
        timestamp=current_datetime()
    )

    # this is where it will get stored in the database

    return success_response(entry.to_dict())

@app.route('/api/v1/guestbook', methods=['GET'])
def browse_guestbook():
    """Return the most recent guestbook entries"""
    print('Browsing the guestbook')
    last_id_string = request.args.get("last_id")
    if last_id_string is None:
        entry_set = GuestbookEntrySet(
            entries=[
                GuestbookEntry(
                    id=4,
                    name='Andy Ford',
                    message='This is my first time signing the guest book.',
                    timestamp=current_datetime()
                ),
                GuestbookEntry(
                    id=3,
                    name='Andy Ford',
                    message='I could not help but sign this thing again.',
                    timestamp=current_datetime()
                )
            ],
            count=2,
            last_id=3,
            has_more=True
        )
    else:
        entry_set = GuestbookEntrySet(
            entries=[
                GuestbookEntry(
                    id=2,
                    name='Franky Ford',
                    message='I want to do this, too!',
                    timestamp=current_datetime()
                ),
                GuestbookEntry(
                    id=1,
                    name='Franky Ford',
                    message='I am back for more.',
                    timestamp=current_datetime()
                )
            ],
            count=2,
            last_id=1,
            has_more=False
        )

    return success_response(entry_set.to_dict())


def current_datetime():
    return datetime.utcnow() # get_localzone()


def error_response(status_code=400, message="Bad request"):
    print('Sending error response')
    ret = jsonify(message=message)
    ret.status_code = status_code
    ret.mimetype = 'application/json'
    return ret


def success_response(response_dict={}):
    print('Sending success response')
    ret = jsonify(response_dict)
    ret.status_code = 200
    ret.mimetype='application/json'
    return ret

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error))
    return error_response(500, error.message)

@app.errorhandler(404)
def internal_server_error(error):
    return error_response(404, "Not found")

@app.errorhandler(Exception)
def unhandled_exception(e):
    app.logger.error('Unhandled Exception: %s', (e))
    return error_response(500, str(e))

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
