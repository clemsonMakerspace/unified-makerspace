import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
dynamodb_client = boto3.client('dynamodb')


# adds a new machine with its details to the Machines table
# also adds the machine id to the Machine_Types table
# machine type must already exist
def insertNewStudent(id, threed_certified,access_level,college,degree_type,designation,email,fn,gen_cert,laser_cert,ln,major,
               vinyl_cert, year):
    # Table Resources
    table = dynamodb.Table('MakerspaceUser')


    # Check if Machine already exists
    response = table.query(
        KeyConditionExpression=Key('PK').eq(id)
    )

    # Return errror if it does
    if (len(response['Items']) > 0):
        return 0


    # Define New Machine Object
    newUser = {}
    newUser['PK'] = id
    newUser['3D_Certified'] = threed_certified
    newUser['AccessLevel'] = access_level
    newUser['College'] = college
    newUser['DegreeType'] = degree_type
    newUser['Designation'] = designation
    newUser['Email'] = email
    newUser['First_Name'] = fn
    newUser['General_Certified'] = gen_cert
    newUser['Laser_Certified'] = laser_cert
    newUser['Last_Name'] = ln
    newUser['Major'] = major
    newUser['Vinyl_Certified'] = vinyl_cert
    newUser['Year'] = year



    # Add New Machine to Db
    table.put_item(Item=newUser)

    # Success
    return 1


# input:
def insertNewStudentHandler(event, context):
    params = event['queryStringParameters']

    reqParams = ["PK","3D_Certified","AccessLevel","College","DegreeType","Designation","Email","First_Name",
                 "General_Certified","Laser_Certified","Last_Name","Major","Vinyl_Certified","Year"]

    # Check for query params
    if (params is None):
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                'Message': 'Failed to provide query string parameters.'
            })
        }

    for param in reqParams:
        if (param not in params):
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'text/plain'
                },
                'body': json.dumps({
                    'Message': 'Failed to provide parameter: ' + param
                })
            }


    # Set parameter values
    id = params["id"]
    threed_certified = params["3D_Certified"]
    access_level = params["AccessLevel"]
    college = params["College"]
    degree_type = params["DegreeType"]
    designation = params["Designation"]
    email = params["Email"]
    fn = params["First_Name"]
    gen_cert = params["General_Certified"]
    laser_cert = params["Laser_Certified"]
    ln = params["Last_Name"]
    major = params["Major"]
    vinyl_cert = params["Vinyl_Certified"]
    year = params["Year"]

    # Call Function
    flag = addMachine(id, threed_certified,access_level,college,degree_type,designation,email,fn,gen_cert,laser_cert,ln,major,
               vinyl_cert, year)

    # Error Message
    if (flag == 0):
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': "User already exists"
        }
    # Success Message
    else:
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': "Added User: " + id
        }

