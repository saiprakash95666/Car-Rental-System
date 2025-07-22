import json
import boto3
import logging
import datetime
from datetime import datetime
logger = logging.getLogger()
logger.setLevel(logging.INFO)


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('userdetails')

now = datetime.now()
x = now.strftime("%m/%d/%Y, %H:%M:%S")


def lambda_handler(event, context):
    http_method = event.get('httpMethod')
    print("http_method:",http_method)
    if http_method == 'GET':
        req_userId=''
        req_userId = event['queryStringParameters']['userid']
        #Retrieves records from DynamoDB 
        response = table.get_item(Key={'userid': req_userId })
        if 'Item' in response :
            data = response['Item']
            userid  = data['userid']
            role    = data['role']
            passwd  = data['passwd']
            status  = data['stat']
            email   = data['email']
            
            res_items = {
                'userid' : userid,
                'role'   : role,
                'passwd' : passwd,
                'status' : status,
                'email'  : email
                
            } 
            print("res_items:",res_items)
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
                    "body": json.dumps('No record found for UserID:' +req_userId),  
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
        req_userId = ''
        req_passwd = ''
        req_role = ''
        req_status=''
        req_fristname = ''
        req_lastname = ''
        req_email = ''
        req_confirmpasswd=''
        if body is not None:
            req_userId = json.loads(body).get('userid', req_userId)
            req_role = json.loads(body).get('role', req_role)
            req_passwd = json.loads(body).get('passwd', req_passwd)
            req_status = json.loads(body).get('stat', req_status)
            
            req_fristname = json.loads(body).get('firstname', req_fristname)
            req_lastname = json.loads(body).get('lastname',req_lastname)
            req_email = json.loads(body).get('email',  req_email)
            req_confirmpasswd = json.loads(body).get('confirmpasswd',req_confirmpasswd)
            
            response = table.get_item(Key={'userid': req_userId})
            if  req_passwd != req_confirmpasswd:
                response = {
                            "isBase64Encoded": False,
                            "statusCode": 400,
                            "body": json.dumps('Please Enter Confirm Password'),  
                            "headers": {
                                    'Content-Type' : 'application/json',
                                    'Access-Control-Allow-Origin' : '*',
                                    'Allow' : 'POST',
                                    'Access-Control-Allow-Methods' : 'POST',
                                    'Access-Control-Allow-Headers' : '*'
                                    }
                                }
            else:
                if 'Item' in response :
                    response = {
                        "isBase64Encoded": False,
                        "statusCode": 400,
                        "body": json.dumps('Already available for userID:' +req_userId),  
                        "headers": {
                            'Content-Type' : 'application/json',
                            'Access-Control-Allow-Origin' : '*',
                            'Allow' : 'POST',
                            'Access-Control-Allow-Methods' : 'POST',
                            'Access-Control-Allow-Headers' : '*'
                            
                        }
                        
                    } 
                    
                else:
                    try:
                        table.put_item(
                            Item={
                                'userid'        : req_userId,
                                'firstname'     : req_fristname,
                                'lastname'      : req_lastname,
                                'role'          : req_role,
                                'stat'          : req_status,
                                'email'         : req_email,
                                'passwd'        : req_passwd,
                                'confirmpasswd' : req_confirmpasswd
                                
                            }
                            )
                        response = {
                            "isBase64Encoded": False,
                            "statusCode": 200,
                            "body": json.dumps('User registered successfully for: ' +req_userId),  
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
        req_userId = ''
        req_status = ''
        
        if body is not None:
            req_userId = json.loads(body).get('userid', req_userId)
            req_status = json.loads(body).get('status', req_status)
            
            
        try:
            update_item = table.update_item(
                Key={'userid': req_userId},
                UpdateExpression="set stat=:s",
                ExpressionAttributeValues={':s': req_status},
                ReturnValues="UPDATED_NEW"
                )
                     
            response = {
                "statusCode": 200,
                "body": json.dumps('User profile updated successfully for: ' +req_userId),  
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
    elif http_method == 'DELETE':
        req_userId=''
        req_userId = event['queryStringParameters']['userid']
        try:
            table.delete_item(Key={'userid': req_userId})
            response = {
                "statusCode": 200,
                "body": json.dumps('Deleted successfully for:' +req_userId),  
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
                'body': json.dumps('Error while deleting data'),
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
            "body": json.dumps('httpMethod:  not supported for this function request'),  
            "headers": {
                'Content-Type' : 'application/json',
                'Access-Control-Allow-Origin' : '*',
                'Allow' : 'PATCH',
                'Access-Control-Allow-Methods' : 'PATCH',
                'Access-Control-Allow-Headers' : '*'
                }
            }        
    return response