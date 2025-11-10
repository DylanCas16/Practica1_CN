import json
from pydantic import ValidationError
from botocore.exceptions import ClientError
from models.ticket import Ticket
from db_connection import db, _format_response

def handler(event, context):
    try:
        ticket_id = event['pathParameters']['id']
        data = json.loads(event.get('body', '{}'))
        data.pop('ticket_id', None)
        data.pop('event_name', None)
        data.pop('purchase_date', None)
        data.pop('event_date', None)
        
        ticket = Ticket(**data)
        updated = db.update_ticket(ticket_id, ticket)
        
        if updated:
            return _format_response(updated.model_dump(), 200)
        else:
            return _format_response({'error': 'Ticket no encontrado'}, 404)
            
    except ValidationError as e:
        details = e.errors() if isinstance(e, ValidationError) else str(e)
        return _format_response({'error': 'Validation error', 'details': details}, 400)
    except KeyError:
        return _format_response({'error': "Missing ticket id"}, 400)
    except ClientError as e:
        return _format_response({'error': 'Client error', 'details': e.response['Error']['Message']}, 500)
    except Exception as e:
        return _format_response({'error': 'Server error', 'details': str(e)}, 500)