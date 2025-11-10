import json
from db.clientDB import PostgresDatabase

try:
    db = PostgresDatabase()
except ValueError as e:
    raise RuntimeError(f"Error inicializando DB: {e}") from e

def _format_response(body, status_code=200):
    response_body = ""
    if body is not None:
        response_body = json.dumps(body)

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,x-api-key",
            "Access-Control-Allow-Methods": "POST,GET,PUT,DELETE,OPTIONS"
        },
        "body": response_body
    }