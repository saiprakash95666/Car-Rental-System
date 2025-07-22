import json
import boto3
import logging
import datetime
from datetime import datetime
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('booklist')

now = datetime.now()
x = now.strftime("%m/%d/%Y, %H:%M:%S")

def lambda_handler(event, context):
    http_method = event.get('httpMethod')
    if http_method == 'GET':
        req_bookId=''
        req_bookId = event['queryStringParameters']['bookId']
        #Retrieves records from DynamoDB 
        response = table.get_item(Key={'bookId': req_bookId })
        if 'Item' in response :
            data = response['Item']
            print(data)
            bookId = data['bookId']
            bookName = data['bookName']
            authName= data['authName']
            pubName = data['pubName']
            status = data['status']
            no_of_books = int(data['no_of_books'])
            res_items = {
                'bookId'     : bookId,
                'bookName'   : bookName,
                'authName'   : authName,
                'pubName'    : pubName,
                'status'     : status,
                'no_of_books': no_of_books
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
                    "body": json.dumps('No record found for Book ID:' +bookId),  
                    "headers": {
                        'Content-Type' : 'application/json',
                        'Access-Control-Allow-Origin' : '*',
                        'Allow' : 'POST',
                        'Access-Control-Allow-Methods' : 'POST',
                        'Access-Control-Allow-Headers' : '*'
                        }
                }
            
                                
    elif http_method == 'PATCH':
        body = event.get('body')
        req_bookId = ''
        req_no_of_books = ''
        
        if body is not None:
            req_bookId = json.loads(body).get('bookId', req_bookId)
            req_no_of_books = json.loads(body).get('no_of_books', req_no_of_books)
            req_no_of_books = int(req_no_of_books) # Convert to integer to ignore decimal value
            
        try:
            update_item = table.update_item(
                Key={'bookId': req_bookId},
                UpdateExpression="set no_of_books=:s",
                ExpressionAttributeValues={':s': req_no_of_books},
                ReturnValues="UPDATED_NEW"
                )
                     
            response = {
                "statusCode": 200,
                "body": json.dumps('Book count updated successfully for: ' +req_bookId),  
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
                        'body': json.dumps('Error whle saving data'),
                        'headers': {
                            'Content-Type' : 'application/json',
                            'Access-Control-Allow-Origin' : '*',
                            'Allow' : 'PATCH',
                            'Access-Control-Allow-Methods' : 'PATCH',
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
  
