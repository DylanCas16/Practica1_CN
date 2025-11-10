from botocore.exceptions import ClientError
from db_connection import db, _format_response

def handler(event, context):
    try:
        tickets = db.get_all_tickets()
        body = [ticket.model_dump() for ticket in tickets]       
        return _format_response(body, 200)

    except ClientError as e:
        return _format_response({'error': 'Client error', 'details': e.response['Error']['Message']}, 500)
    
    except Exception as e:
        return _format_response({'error': 'Server error', 'details': str(e)}, 500)