from flask.json import JSONEncoder
from datetime import datetime


class MyJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                obj = obj.utc().isoformat()
        except TypeError:
            pass
        else:
            return obj
        return JSONEncoder.default(self, obj)