import json
import boto3
from datetime import datetime
from datetime import timedelta
from dateutil import parser
import os
import sys

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'lib'))
from pytz import timezone

lambda_client = boto3.client('lambda')
cf_client = boto3.client('cloudformation')

def detector(event, context):
    now_time = datetime.now(timezone('UTC'))
    checked_date = now_time - timedelta(days = int(os.environ['DURATION_DAYS']))
    
    lambda_function_list = lambda_client.list_functions()
    stack_lambda_map = create_stack_lambda_map()
    function_time_map = {}
    
    for function in lambda_function_list['Functions']:
        if checked_date > parser.parse(function['LastModified']):
            stack_name = ""
            if function['FunctionName'] in stack_lambda_map:
                stack_name = stack_lambda_map[function['FunctionName']]
                
            function_time_map[function['FunctionName']] = {
                'FunctionArn': function['FunctionArn'],
                'LastModified': function['LastModified'],
                'Tags': lambda_client.list_tags(Resource=function['FunctionArn'])['Tags'],
                'StackName': stack_name
                }
            
    
    return function_time_map
    
def create_stack_lambda_map():
    
    next_token = None
    
    stack_map = cf_client.describe_stacks()
    stack_lambda_map = {}
    
    add_stack_lambda_map(stack_map, stack_lambda_map)
    
    while next_token:
        stack_map = cf_client.describe_stacks(NextToken=next_token)
        add_stack_lambda_map(stack_map, stack_lambda_map)

    return stack_lambda_map

def add_stack_lambda_map(stack_map, stack_lambda_map):
    for stack_info in stack_map['Stacks']:
        stack_resources = cf_client.list_stack_resources(StackName = stack_info['StackName'])
        for stack_resource in stack_resources['StackResourceSummaries']:
            if stack_resource['ResourceType'] == "AWS::Lambda::Function":
                stack_lambda_map[stack_resource['PhysicalResourceId']] = stack_info['StackName']

    return stack_lambda_map    
    