# Standard library
import json
from uuid import uuid4


def wrap_error_message(error: Exception) -> str:
    return json.dumps({
        'id': str(uuid4()),
        'message': str(error)
    })
