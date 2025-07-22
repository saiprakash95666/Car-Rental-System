import json
import boto3
import logging
from datetime import datetime
from decimal import Decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super(DecimalEncoder, self).default(obj)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('carlist')

def get_item_by_id(car_id):
    response = table.get_item(Key={'carid': car_id})
    if 'Item' in response:
        data = response['Item']
        return {
            'carid': data['carid'],
            'carName': data['carName'],
            'modelName': data['modelName'],
            'status': data['status'],
            'no_of_miles': data['no_of_miles']
        }
    return None

def create_response(status_code, body):
    return {
        "isBase64Encoded": False,
        "statusCode": status_code,
        "body": json.dumps(body, cls=DecimalEncoder),
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Allow': 'POST',
            'Access-Control-Allow-Methods': 'GET,POST,PATCH,DELETE',
            'Access-Control-Allow-Headers': '*'
        }
    }

def lambda_handler(event, context):
    http_method = event['httpMethod']
    if http_method == 'GET':
        car_id = event['queryStringParameters']['carid']
        data = get_item_by_id(car_id)
        if data is not None:
            return create_response(200, data)
        else:
            return create_response(404, 'No record found for Car ID: ' + car_id)

    elif http_method == 'POST':
        body = event.get('body')
        if body is not None:
            payload = json.loads(body)
            car_id = payload.get('carid')
            data = get_item_by_id(car_id)
            if data is not None:
                return create_response(400, 'Already available car for this CarId: ' + car_id)
            else:
                try:
                    table.put_item(Item=payload)
                    return create_response(200, 'Car Added successfully for: ' + car_id)
                except:
                    return create_response(400, 'Error while saving data')

    elif http_method == 'PATCH':
        body = event.get('body')
        if body is not None:
            payload = json.loads(body)
            car_id = payload.get('carid')
            new_status = payload.get('status')
            try:
                table.update_item(
                    Key={'carid': car_id},
                    UpdateExpression='SET #new_status = :new_value',
                    ExpressionAttributeNames={'#new_status': 'status'},
                    ExpressionAttributeValues={':new_value': new_status},
                    ReturnValues="UPDATED_NEW"
                )
                return create_response(200, 'Car status updated successfully')
            except:
                return create_response(400, 'Error while updating data')

    elif http_method == 'DELETE':
        car_id = event['queryStringParameters']['carid']
        try:
            table.delete_item(Key={'carid': car_id})
            return create_response(200, 'Car deleted successfully')
        except:
            return create_response(400, 'Error while deleting data')
    else:
        return create_response(405, 'Method Not Allowed')
