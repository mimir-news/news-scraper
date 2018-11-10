# Standard library
import json
from uuid import uuid4
from typing import Optional


def wrap_error_message(error: Exception, id: Optional[str] = None) -> str:
    """Wraps an exceptions error message into 
    a json formated string with a unique error id.

    :param error: Exception to wrap.
    :param id: Optional id to add to the error.
    :return: JSON formated error string.
    """
    error_id: str = id or str(uuid4())
    return json.dumps({
        'id': error_id,
        'message': str(error)
    })
