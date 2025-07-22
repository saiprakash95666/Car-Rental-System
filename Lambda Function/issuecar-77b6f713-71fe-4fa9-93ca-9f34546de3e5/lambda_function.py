import json
import boto3
import logging
import datetime
import uuid
from datetime import datetime
logger = logging.getLogger()
logger.setLevel(logging.INFO)


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('issuecar')

now = datetime.now()
x = now.strftime("%m/%d/%Y, %H:%M:%S")


def lambda_handler(event, context):
    http_method = event.get('httpMethod')
    if http_method == 'GET':
        req_Id=''
        req_Id = event['queryStringParameters']['id']
        #Retrieves records from DynamoDB 
        response = table.get_item(Key={'id': req_Id })
        if 'Item' in response :
            data = response['Item']

            Id = data['id']
            carId = data['carid']
            issue_date= data['issue_date']
            return_date = data['return_date']
            status = data['stat']
            res_items = {
                'id'         : Id,
                'carid'     : carId,
                'issue_date' : issue_date,
                'return_date': return_date,
                'stat'       : status
            }    
            response = {
                "isBase64Encoded": False,
                "statusCode": 200,
                "body": json.dumps(res_items),  
                "headers": {
                    'Content-Type' : 'application/json',
                    'Access-Control-Allow-Origin' : '*',
                    'Allow' : 'POST',
                    'Access-Control-Allow-Methods' : 'GET',
                    'Access-Control-Allow-Headers' : '*'
                    }
            }
        else:
            response = {
                    "isBase64Encoded": False,
                    "statusCode": 404,
                    "body": json.dumps('No record found for Car ID:' + carId),  
                    "headers": {
                        'Content-Type' : 'application/json',
                        'Access-Control-Allow-Origin' : '*',
                        'Allow' : 'POST',
                        'Access-Control-Allow-Methods' : 'POST',
                        'Access-Control-Allow-Headers' : '*'
                        }
                }
            
    elif http_method == 'POST':
        body = event.get('body')
        req_carId      = ''
        req_issue_date  = ''
        req_return_date = ''
        req_status      = ''

        if body is not None:
            req_carId = json.loads(body).get('carid', req_carId)
            req_issue_date = json.loads(body).get('issue_date', req_issue_date)
            req_return_date = json.loads(body).get('return_date', req_return_date)
            req_status = json.loads(body).get('stat', req_status)
            try:
                table.put_item(
                    Item={
                        'id'            : str(uuid.uuid4()),
                        'carid'        : req_carId,
                        'issue_date'    : req_issue_date,
                        'return_date'   : req_return_date,
                        'stat'          : req_status
                        }
                     )
                            
                response = {
                    "isBase64Encoded": False,
                    "statusCode": 200,
                    "body": json.dumps('Car booking successful!'),  
                    "headers": {
                        'Content-Type' : 'application/json',
                        'Access-Control-Allow-Origin' : '*',
                        'Allow' : 'POST',
                        'Access-Control-Allow-Methods' : 'POST',
                        'Access-Control-Allow-Headers' : '*'
                        }
                    }
                
            except:
                    response= {
                        'statusCode': 400,
                        'body': json.dumps('Error whle saving data'),
                        'headers': {
                        'Content-Type' : 'application/json',
                        'Access-Control-Allow-Origin' : '*',
                        'Allow' : 'POST',
                        'Access-Control-Allow-Methods' : 'POST',
                        'Access-Control-Allow-Headers' : '*'
                        }
                    }
    
    elif http_method == 'PATCH':
        body = event.get('body')
        req_Id = ''
        req_status = ''
        req_return_date=''
        
        if body is not None:
            req_Id = json.loads(body).get('id', req_Id)
            req_status = json.loads(body).get('status', req_status)
            req_return_date = json.loads(body).get('return_date', req_return_date)
            
            
        try:
            update_item = table.update_item(
                Key={'id': req_Id},
                UpdateExpression="set stat=:st ,return_date=:rtd",
                ExpressionAttributeValues={':st': req_status,':rtd':req_return_date},
                ReturnValues="UPDATED_NEW"
                )
                     
            response = {
                "statusCode": 200,
                "body": json.dumps('Car status updated successfully for: ' +req_Id),  
                "headers": {
                    'Content-Type' : 'application/json',
                    'Access-Control-Allow-Origin' : '*',
                    'Allow' : 'PATCH',
                    'Access-Control-Allow-Methods' : 'PATCH',
                    'Access-Control-Allow-Headers' : '*'
                    }
                }
        except:
                response= {
                        'statusCode': 400,
                        'body': json.dumps('Error while saving data'),
                        'headers': {
                            'Content-Type' : 'application/json',
                            'Access-Control-Allow-Origin' : '*',
                            'Allow' : 'PATCH',
                            'Access-Control-Allow-Methods' : 'PATCH',
                            'Access-Control-Allow-Headers' : '*'
                            }
                    }
    elif http_method == 'DELETE':
        req_carId=''
        req_carId = event['queryStringParameters']['carid']
        try:
            table.delete_item(Key={'carid': req_carId})
            response = {
                "statusCode": 200,
                "body": json.dumps('Deleted successfully for:' +req_carId),  
                "headers": {
                    'Content-Type' : 'application/json',
                    'Access-Control-Allow-Origin' : '*',
                    'Allow' : 'DELETE',
                    'Access-Control-Allow-Methods' : 'DELETE',
                    'Access-Control-Allow-Headers' : '*'
                        }
                    } 
        except:
            response= {
                'statusCode': 400,
                'body': json.dumps('Error while updating data'),
                'headers': {
                    'Content-Type' : 'application/json',
                    'Access-Control-Allow-Origin' : '*',
                    'Allow' : 'POST',
                    'Access-Control-Allow-Methods' : 'POST',
                    'Access-Control-Allow-Headers' : '*'
                        }
                    }                       
           
                       
    else:
        response = {
            "statusCode": 405,
            "body": json.dumps('httpMethod:  not supported for request'),  
            "headers": {
                'Content-Type' : 'application/json',
                'Access-Control-Allow-Origin' : '*',
                'Allow' : 'PATCH',
                'Access-Control-Allow-Methods' : 'PATCH',
                'Access-Control-Allow-Headers' : '*'
                }
            }        
    return response      
  
        
     


