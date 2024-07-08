#!/usr/bin/python3

"""
Helper functions
"""


from flask import jsonify
import uuid



def generate_uuid() -> str:
    """
    Generates a new uuid
    """

    return str(uuid.uuid4())


def error_response(message, status_code) -> jsonify:
    response = jsonify({
        "status": "Bad request",
        "message": message,
        "statusCode": status_code
    })
    response.status_code = status_code
    return response
