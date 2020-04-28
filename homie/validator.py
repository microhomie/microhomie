from homie.constants import (
    BOOLEAN,
    COLOR,
    ENUM,
    FALSE,
    FLOAT,
    INTEGER,
    STRING,
    TRUE,
    RGB,
)


def payload_is_valid(cls, payload):
    _dt = cls.datatype
    _fmt = cls.format

    if _dt == STRING:
        pass
    elif _dt == INTEGER or _dt == FLOAT:
        try:
            float(payload)
        except ValueError:
            return False
    elif _dt == BOOLEAN:
        if payload != TRUE and payload != FALSE:
            return False
    elif _dt == ENUM:
        _values = cls.format.split(",")
        if payload not in _values:
            return False
    elif _dt == COLOR:
        if _fmt == RGB:
            if len(payload.split(",")) != 3:
                return False

    return True
