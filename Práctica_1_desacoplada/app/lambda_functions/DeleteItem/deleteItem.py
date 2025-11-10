from botocore.exceptions import ClientError
from db_connection import db, _format_response

def handler(event, context):
    try:
        ticket_id = event['pathParameters']['id']
        
        if db.delete_product(ticket_id):
            return _format_response(None, 204)
        else:
            return _format_response({'error': 'Ticket no encontrado'}, 404)

    except KeyError:
        return _format_response({'error': "Missing ticket id"}, 400)
    except ClientError as e:
        return _format_response({'error': 'Client error', 'details': e.response['Error']['Message']}, 500)
    except Exception as e:
        return _format_response({'error': 'Server error', 'details': str(e)}, 500)