from datetime import datetime, date


def datetime_serializer(o):
    if isinstance(o, (datetime, date)):
        return o.isoformat()
    return str(o)
