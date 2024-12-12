import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import boto3
from pyspark.sql.functions import lit

# Initialize Glue context
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Specify S3 bucket and data source
s3_bucket = "testing-trigger-for-glue-job" 
s3_path = f"s3://{s3_bucket}/testing_file.csv" 

# Read data from S3 into a DynamicFrame
datasource0 = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [s3_path]},
    format="csv",
    format_options={"withHeader": True}
)

# Convert to DataFrame for processing
df = datasource0.toDF()

# Trim leading and trailing spaces from column names
df = df.toDF(*[col.strip() for col in df.columns])

# Rename columns to match DynamoDB schema for visit information
df = df.withColumnRenamed("Timestamp", "timestamp") \
       .withColumnRenamed("Where are you", "location") \
       .withColumnRenamed("CU Username (the text before your @clemson email)", "user_id") \
       .withColumn("name", lit(""))  # Add an empty column for "name"

# Extract and process visit data
visitData = df.select("user_id", "timestamp", "location", "name")

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
visit_table = dynamodb.Table('test-visits')

# Write visitData to test-visits
for row in visitData.collect():
    if row.user_id:  # Check if the user_id is not empty
        visit_table.put_item(Item={
            'user_id':          row.user_id,
            'timestamp':        row.timestamp,
            'location':         row.location,
            'name':             "",
            '_ignore':          "1",
            # Add other user attributes if needed
        })

# Rename columns to match DynamoDB schema for user information
df = df.withColumnRenamed("What is your University status?", "university_status") \
       .withColumnRenamed("What is your Major?", "major") \
       .withColumnRenamed("What College are you in?", "college") \
       .withColumnRenamed("College Acronym", "college_acronym") \
       .withColumnRenamed("If an Undergraduate, what year are you?", "undergraduate_class")

# Extract and process user data
userData = df.select("user_id", "university_status", "major", "college", "college_acronym", "undergraduate_class")

# Initialize DynamoDB table for user information
user_table = dynamodb.Table('test-users')

# Write userData to test-users
for row in userData.collect():
    if row.user_id:  # Check if the user_id is not empty
        user_table.put_item(Item={
            'user_id':                  row.user_id,
            'university_status':        row.university_status,
            'major':                    row.major,
            'college':                  row.college,
            'college_acronym':          row.college_acronym,
            'undergraduate_class':      row.undergraduate_class,
            # Add other user attributes if needed
        })
        
# Rename columns to match DynamoDB schema for equipment information
df = df.withColumnRenamed("Print Name (ex: crab, apple, car)", "print_name") \
       .withColumnRenamed("What type of project is this?", "project_type") \
       .withColumnRenamed("What class is this project for?", "class_number") \
       .withColumnRenamed("Who is your Professor? Please write first and last name format as: First Last", "faculty_name") \
       .withColumnRenamed("Who is your advisor for the project?  Please write first and last name format as: First Last", "advisor_name") \
       .withColumnRenamed("Who is the project sponsor?", "project_sponsor") \
       .withColumnRenamed("What is the name of the Club/Organization?", "organization_affiliation") \
       .withColumnRenamed("Which equipment are you logging?", "equipment_type") \
       .withColumnRenamed("Printer Name", "printer_name") \
       .withColumnRenamed("Print Time", "print_duration") \
       .withColumnRenamed("Print Mass", "print_mass") \
       .withColumnRenamed("Print Mass Estimate", "print_mass_estimate") \
       .withColumnRenamed("Print Status", "print_status") \
       .withColumnRenamed("What resin are you using?", "resin_type") \
       .withColumnRenamed("What is the name of your project?", "project_name") \
       .withColumnRenamed("What is your Department?", "department_name") \
       .withColumnRenamed("How satisfied were you with the help you received from the Makerspace staff (1 being not at all, 10 being very satisfied)?", "satisfaction_rate") \
       .withColumnRenamed("(Optional) Did you receive the filament color you wanted?", "recieved_filament_color") \
       .withColumnRenamed("(Optional) Of the colors we have what would you like to see more of?", "more_colors") \
       .withColumnRenamed("(Optional) What resin would you like us to buy?", "requested_colors") \
       .withColumnRenamed("Are you interested in presenting your and/or your organization's project at Makerday 15? (Tuesday, Nov 14th)", "present_makerday") \
       .withColumnRenamed("Which intern helped you today? (intern should be wearing nametag)", "intern_name") \
       .withColumnRenamed("What specific issues did you have?", "issue_notes") \
       .withColumnRenamed("How did you hear about the Makerspace?", "referral_source") \
       .withColumnRenamed("Did you have any difficulties today?", "difficulties_notes") \
       .withColumn("print_notes", lit(""))  # Add an empty column for "print_notes"

# Extract and process equipment data        
equipmentData = df.select("user_id", "timestamp", "location", "project_name", "project_type", "class_number", "faculty_name", "project_sponsor", "organization_affiliation", "equipment_type", "printer_name", "print_duration", "print_mass", "print_mass_estimate", "print_status", "print_notes", "advisor_name", "resin_type", "print_name", "department_name", "satisfaction_rate", "recieved_filament_color", "more_colors", "requested_colors", "present_makerday", "intern_name", "issue_notes", "referral_source", "difficulties_notes")

# Initialize DynamoDB table for equipment data 
equipment_table = dynamodb.Table('test-equipment')

# Write equipmentData to test-equipment
for row in equipmentData.collect():
    if row.user_id:  # Check if the user_id is not empty
        # Create printer_info dictionary
        if row.equipment_type == "FDM 3D Printer (Plastic)" or row.equipment_type == "SLA Printer (Resin)":
            printer_info = {
                "print_status":                 row.print_status,
                "print_notes":                  "",
                "printer_name":                 row.printer_name,
                "print_mass_estimate":          row.print_mass_estimate,
                "print_duration":               row.print_duration,
                "print_mass":                   row.print_mass
            }
            
            equipment_table.put_item(Item={
                '3d_printer_info':              printer_info,
                'user_id':                      row.user_id,
                'timestamp':                    row.timestamp,
                'location':                     row.location,
                'project_name':                 row.project_name,
                'project_type':                 row.project_type,
                'class_number':                 row.class_number,
                'faculty_name':                 row.faculty_name,
                'advisor_name':                 row.advisor_name,
                'project_sponsor':              row.project_sponsor,
                'organization_affiliation':     row.organization_affiliation,
                'department_name':              row.department_name,
                'equipment_type':               row.equipment_type,
                'print_name':                   row.print_name,
                'resin_type':                   row.resin_type,
                'satisfaction_rate':            row.satisfaction_rate,
                'recieved_filament_color':      row.recieved_filament_color,
                'more_colors':                  row.more_colors,
                'requested_colors':             row.requested_colors,
                'present_makerday':             row.present_makerday,
                'intern_name':                  row.intern_name,
                'issue_notes':                  row.issue_notes,
                'referral_source':              row.referral_source,
                'difficulties_notes':           row.difficulties_notes,
                '_ignore':                      "1",
                # Add other user attributes if needed
            })
        else:
            # Put columns into table
            equipment_table.put_item(Item={
                'user_id':                      row.user_id,
                'timestamp':                    row.timestamp,
                'location':                     row.location,
                'project_name':                 row.project_name,
                'project_type':                 row.project_type,
                'class_number':                 row.class_number,
                'faculty_name':                 row.faculty_name,
                'advisor_name':                 row.advisor_name,
                'project_sponsor':              row.project_sponsor,
                'organization_affiliation':     row.organization_affiliation,
                'department_name':              row.department_name,
                'equipment_type':               row.equipment_type,
                'print_name':                   row.print_name,
                'resin_type':                   row.resin_type,
                'satisfaction_rate':            row.satisfaction_rate,
                'recieved_filament_color':      row.recieved_filament_color,
                'more_colors':                  row.more_colors,
                'requested_colors':             row.requested_colors,
                'present_makerday':             row.present_makerday,
                'intern_name':                  row.intern_name,
                'issue_notes':                  row.issue_notes,
                'referral_source':              row.referral_source,
                'difficulties_notes':           row.difficulties_notes,
                '_ignore':                      "1",
                # Add other user attributes if needed
            })
        
        

job.commit()
