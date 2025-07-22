import json
import boto3
from botocore.exceptions import ClientError
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('userdetails')
def lambda_handler(event, context):
    http_method = event.get('httpMethod')
    if http_method == 'POST':
        body = event.get('body')
        req_userId = ''
        req_passwd = ''
        if body is not None:
            req_userId = json.loads(body).get('userid', req_userId)
            req_passwd = json.loads(body).get('passwd', req_passwd)
        try:
            response = table.get_item(Key={'userid': req_userId})
            if 'Item' in response :
                data = response['Item']
                userId = data['userid']
                passwd = data['passwd']
                stat = data['stat']
                role = data['role']
                print(userId,passwd,stat)
                print(req_userId,req_passwd)
            
                if (userId == req_userId and  passwd==req_passwd and stat == 'active'):
                    return{
                        "isBase64Encoded": False,
                        'statusCode' : 200,
                        "headers": {
                         'Content-Type' : 'application/json'
                         },
                        "body" : json.dumps({"message" : "Login Successfull","role" : role})
                    
                    
                        }
                else:
                    return{
                        "isBase64Encoded": False,
                        "statusCode" : 400,
                        "headers": {
                        'Content-Type' : 'application/json'
                        },
                    "body" : json.dumps({"message" : "Invalid Credential"})
                     }
            else:
                print('No UserId ')
                return {
                    "isBase64Encoded": False,
                    "statusCode": 404,
                    "headers": {
                       'Content-Type' : 'application/json'
                        },
                    "body": json.dumps('User not found')
            }
        except ClientError as e:
            print(e.response['Error']['Message'])
            return {
            'statusCode': 400,
            'body': json.dumps('Error occurred')
        }  
    else:
        response = {
                "isBase64Encoded": False,
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
  