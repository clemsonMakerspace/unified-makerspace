import json
import boto3
from boto3.dynamodb.conditions import Key

poolID = "us-east-1_l5xLuC13j"
db = boto3.resource('dynamodb')
db_client = boto3.client('dynamodb')
client = boto3.client('cognito-idp')
table = db.Table('MakerspaceUser')

# get user role given id
def getUserRole(id):

    # Get user by id
    response = table.query(
        KeyConditionExpression = Key('PK').eq(str(id))
    )
    
    return(response['Items'][0]['AccessLevel'])

def getUsersHandler(event, context):
    
    # Verify that user exists within the pool
    try:
        token = event['token']
    except:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'Message' : 'Error loading data. '
             })
        }
    
    #Validate permissions
    role = getUserRole(token)
    if(role != "manager"):
        return {
            'code': 401,
            'message' : 'Insufficient Permissions. '
        }
    
   
    try:
        #Get full lists of users in the table
        query = "SELECT * FROM MakerspaceUser"
        r = db_client.execute_statement(Statement=query)
        response = r['Items']
        
        all_users = []
        #loop through existing users
        for user in response:
            temp_user = {}
            #save name, username, and permissions
            temp_user['name'] = user['First_Name']['S'] + " " + user['Last_Name']['S']
            temp_user['id'] = user['Email']['S']
            temp_user['perm'] = user['AccessLevel']['S']
            
            #TODO: Get any tasks assigned to the user
            temp_user['tasks'] = None
            
            print(temp_user)
            all_users.append(temp_user)
            
    except Exception as e:
        return {
            'code': 402,
            'message': "Error retrieving data"
        }

    return {
            'code': 200,
             'users': all_users
    }