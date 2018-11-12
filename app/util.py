# Standard library
import json
from datetime import datetime
from uuid import uuid4
from typing import Optional

# Internal modules
from app.config import DATE_FORMAT


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


def date_to_str(date: datetime) -> str:
    """Formats a date as a string.

    :param date: Datetime to format.
    :return: String
    """
    return date.strftime(DATE_FORMAT)


def str_to_date(date_str: str) -> datetime:
    """Parses the date value from a string.

    :param date_str: String representation of a date.
    :return: Parsed datetime.
    """
    return datetime.strptime(date_str, DATE_FORMAT)
