import boto3
import json
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key, Attr

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

#Get Table Objects
Child_Table = dynamodb.Table('Child_Tasks')
Parent_Table = dynamodb.Table('Parent_Tasks')

#Scans Parent Table
def AltViewHistory(params):

    #Get Param
    daysBack = int(params['DaysBack'])

    #Denote variables
    items = []
    missed = 0
    complete = 0

    #Calculate days
    yest = (datetime.now()-timedelta(days=1)).strftime('%Y%m%d')
    past = (datetime.now()-timedelta(days=daysBack)).strftime('%Y%m%d')

    #Scan Parent Table
    parents = Parent_Table.scan(
        FilterExpression=Attr('Active').eq(1)
    )['Items']

    #Iterate through Parent Ids
    for p in parents:

        #Query Child Table
        children = Child_Table.query(
            IndexName= "Parent_Index",
            KeyConditionExpression=
                Key('Parent_Id').eq(p['Parent_Id']) &
                Key('Due_Date').between(past, yest),
                FilterExpression=Attr('Active').eq(1)
        )['Items']

        #Iterate through children
        for child in children:

            #Calculate Date Completed
            if child['Completed']:
                completed_on = datetime.fromtimestamp(
                    float(child['Completed_DateTime'])
                ).strftime('%c')
            else:
                completed_on = ''
                
            #Determine Task Status
            if child['Completed'] and child['Late']:
                status = 'Late'
            elif child['Completed']:
                status = 'Complete'
                complete += 1
            else:
                status = 'Missed'
                missed += 1

            #Add additional fields
            child['Completed_On'] = completed_on
            child['Status'] = status

            #Remove Fields
            del child['Active']
            del child['Late']
            del child['Completed']
            del child['Completed_DateTime']

            #Add task to list
            items.append(child)

    #Build result object
    result = {
        'Items': items,
        'Missed': missed,
        'Complete': complete
    }

    return result

#Dear Future Capstone Student - Use this if Alt View History
#   becomes slow. This doesn't rely on scan, so the size of
#   the database will not affect latency. Speed is only
#   affected by how many queries you run. I.e the more DaysBack
#   the more queries will be run. 
def ViewHistory(params):

    #Get Param
    days = int(params['DaysBack'])

    #Denote variables
    items = []
    missed = 0
    complete = 0

    #Iterate through tasks
    for daysBack in range(1, days+1):

        #Calculate key for due date
        dueDate = (datetime.now()-timedelta(days=daysBack)).strftime('%Y%m%d')

        #Get tasks due for calculated due date
        children = Child_Table.query(
            KeyConditionExpression=
                Key('Due_Date').eq(dueDate),
            FilterExpression=Attr('Active').eq(1)
        )['Items']

        #Iterate through children
        for child in children:

            #Calculate Date Completed
            if child['Completed']:
                completed_on = datetime.fromtimestamp(
                    float(child['Completed_DateTime'])
                ).strftime('%c')
            else:
                completed_on = ''
                
            #Determine Task Status
            if child['Completed'] and child['Late']:
                status = 'Late'
            elif child['Completed']:
                status = 'Complete'
                complete += 1
            else:
                status = 'Missed'
                missed += 1

            #Add additional fields
            child['Completed_On'] = completed_on
            child['Status'] = status

            #Remove Fields
            del child['Active']
            del child['Late']
            del child['Completed']
            del child['Completed_DateTime']

            items.append(child)

    #Build result object
    result = {
        'Items': items,
        'Missed': missed,
        'Complete': complete
    }

    return result

def ViewHistoryHandler(event, context):

    reqParams = ['DaysBack']

    #Get Query Params
    paramVals = event["queryStringParameters"]

    #Return client error if no string params
    if (paramVals is None):
        return{
            'statusCode': 400,
            'headers':{
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                'Message' : 'Failed to provide query string parameters.'
            })
        }

    #Check for each parameter we need
    for name in reqParams:
        if (name not in paramVals):
            return {
                'statusCode': 400,
                'headers':{
                    'Content-Type': 'text/plain'
                },
                'body': json.dumps({
                    'Message' : 'Failed to provide parameter: ' + name
                })
            }   

    try:
        #Call function
        result = AltViewHistory(paramVals)

        #Send Response
        return {
            'statusCode': 200,
            'headers':{
                'Content-Type': 'text/plain'
            },
            'body': json.dumps(result)
        }
    except Exception as e:
        #Return exception with response
        return {
            'statusCode': 500,
            'headers':{
                'Content-Type': 'text/plain'
            },
            'body': json.dumps({
                'Message' : str(e)
            }) 
        }