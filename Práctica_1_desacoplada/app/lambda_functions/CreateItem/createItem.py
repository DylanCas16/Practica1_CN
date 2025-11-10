import json
from pydantic import ValidationError
from botocore.exceptions import ClientError
from models.ticket import Ticket
from db_connection import db, _format_response

def handler(event, context):
    try:
        data = json.loads(event.get('body', '{}'))
        new_ticket = Ticket(**data)
        created = db.create_ticket(new_ticket)
        return _format_response(created.model_dump(), 201)
    
    except ValidationError as e:
        details = e.errors() if isinstance(e, ValidationError) else str(e)
        return _format_response({'error': 'Validation error', 'details': details}, 400)
    
    except ClientError as e:
        return _format_response({'error': 'Client error', 'details': e.response['Error']['Message']}, 500)
    
    except Exception as e:
        return _format_response({'error': 'Server error', 'details': str(e)}, 500)