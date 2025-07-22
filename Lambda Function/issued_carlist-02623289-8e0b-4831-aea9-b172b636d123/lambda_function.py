import json
import boto3
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
from boto3.dynamodb.conditions import Key, And
table = dynamodb.Table('issuecar')


def lambda_handler(event, context):
    http_method = event.get('httpMethod')
    if http_method =='GET':
        req_userId=''
        req_use = event['queryStringParameters']
        print(req_use)
        req_userId = event['queryStringParameters']['userid']

        #Retrieves records from DynamoDB 
        final_data=[]
        res_items = table.scan()
        #res_items = = table.scan(FilterExpression=And(*[(Key(key).eq(value)) for key, value in filters.items()]))
        data=res_items['Items']
        
        while 'LastEvaluatedKey' in res_items:
            res_items = table.scan(ExclusiveStartKey=res_items['LastEvaluatedKey'])
            data.extend(res_items['Items'])
            
        for i in data:
            if(req_userId==i['issue_to']):
                temp_data= {'id':i['id'],'carid':i['carid'],'issue_date':i['issue_date'],'stat':i['stat'],'return_date':i['return_date']}
                final_data.append(temp_data)
            else:
                pass
        
            response = {
                "isBase64Encoded": False,
                "statusCode": 200,
                "body": json.dumps(final_data),  
                "headers": {
                    'Content-Type' : 'application/json',
                    'Access-Control-Allow-Origin' : '*',
                    'Allow' : 'POST',
                    'Access-Control-Allow-Methods' : 'POST',
                    'Access-Control-Allow-Headers' : '*'
                    }
                }
    else:
        response = {
            "isBase64Encoded": False,
            "statusCode": 405,
            "body": json.dumps('httpMethod: '+http_method+ ' not supported for request'),  
            "headers": {
                'Content-Type' : 'application/json',
                'Access-Control-Allow-Origin' : '*',
                'Allow' : 'PATCH',
                'Access-Control-Allow-Methods' : 'POST',
                'Access-Control-Allow-Headers' : '*'
                }
            }        
   
    return response      
  
        
     


