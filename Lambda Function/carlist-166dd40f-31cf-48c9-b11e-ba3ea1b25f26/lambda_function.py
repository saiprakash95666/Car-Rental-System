import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('carlist')


def lambda_handler(event, context):
    http_method = event.get('httpMethod')
    if http_method == 'GET':
        # Retrieves records from DynamoDB using pagination and a projection expression
        final_data = []
        response = table.scan(ProjectionExpression='carid, carName, modelName, no_of_miles, #s',
                              ExpressionAttributeNames={'#s': 'status'})
        data = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ProjectionExpression='carid, carName, modelName, no_of_miles, #s',
                                  ExpressionAttributeNames={'#s': 'status'},
                                  ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])

        for i in data:
            temp_data = {'carid': i['carid'], 'carName': i['carName'], 'modelName': i['modelName'],
                        'no_of_miles': str(i['no_of_miles']), 'status': i['status']}
            final_data.append(temp_data)

        response = {
            "isBase64Encoded": False,
            "statusCode": 200,
            "body": json.dumps(final_data),
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Allow': 'POST',
                'Access-Control-Allow-Methods': 'POST',
                'Access-Control-Allow-Headers': '*'
            }
        }
    else:
        response = {
            "isBase64Encoded": False,
            "statusCode": 405,
            "body": json.dumps('httpMethod: ' + http_method + ' not supported for request'),
            "headers": {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Allow': 'PATCH',
                'Access-Control-Allow-Methods': 'POST',
                'Access-Control-Allow-Headers': '*'
            }
        }

    return response
