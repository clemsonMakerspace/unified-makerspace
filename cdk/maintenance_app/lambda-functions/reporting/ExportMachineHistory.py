import xlsxwriter
import boto3
import json
import os
from io import BytesIO
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key, Attr

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

#Get client for s3 Upload
s3client = boto3.client('s3')

#Get Table Objects
Child_Table = dynamodb.Table('Child_Tasks')
Machine_Table = dynamodb.Table('Machines')

#GetBucketArn
bucketName = os.environ['bucketName']

def ExportMachineHistory(params):

    #Parameters
    machineId = params['MachineId']
    daysBack = int(params['DaysBack'])

    #Denote variables
    expires = 900
    missed = 0
    complete = 0
    row = 1

    #Create Excel Workbook/Sheet
    bytes = BytesIO()
    workbook = xlsxwriter.Workbook(bytes)
    worksheet = workbook.add_worksheet('Data')

    #Format Excel Headers
    bold = workbook.add_format({'bold': True})
    worksheet.set_column('A:Z', 18.0)
    worksheet.set_column('D:D', 22)
    worksheet.write('A1', 'Task', bold)
    worksheet.write('B1', 'Machine', bold)
    worksheet.write('C1', 'Comleted By', bold)
    worksheet.write('D1', 'Completed On', bold)
    worksheet.write('E1', 'Completion Status', bold)

    #Query Machine for Tasks
    machine = Machine_Table.query(
        KeyConditionExpression=Key('Machine_Id').eq(machineId)
    )['Items'][0]

    #Convert Set of Tasks to List
    if 'Tasks' in machine:
        machine['Tasks'] = list(machine['Tasks'])

    #Each Parent Tasks for Machine
    for pid in machine['Tasks']:

        #Calculate days
        yest = (datetime.now()-timedelta(days=1)).strftime('%Y%m%d')
        past = (datetime.now()-timedelta(days=daysBack)).strftime('%Y%m%d')

        #Query Child Table
        children = Child_Table.query(
            IndexName= "Parent_Index",
            KeyConditionExpression=
                Key('Parent_Id').eq(pid) &
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

            #Write task row to excel file
            worksheet.write(row, 0, child['Task_Name'])
            worksheet.write(row, 1, child['Machine_Name'])
            worksheet.write(row, 2, child['Completed_By'])
            worksheet.write(row, 3, completed_on)
            worksheet.write(row, 4, status)

            row+=1

    #Write Missed/Complete Tasks to Excel File
    worksheet.write('G1', 'Completed Tasks', bold)
    worksheet.write('H1', 'Missed Tasks', bold)
    worksheet.write('G2', complete)
    worksheet.write('H2', missed)

    #Close Workbook
    workbook.close()
    
    #Add workbook object to s3 bucket
    s3client.put_object(
        Body=bytes.getvalue(),
        Bucket=bucketName,
        Key=(machineId + '.xlsx'),
    )

    #Generate url to access s3 bucket object
    url = s3client.generate_presigned_url('get_object',
                Params={'Bucket': bucketName,
                        'Key': (machineId + '.xlsx')},
                ExpiresIn=expires)

    return url

def ExportMachineHistoryHandler(event, context):

    reqParams = ['DaysBack', 'MachineId']

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
        result = ExportMachineHistory(paramVals)

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