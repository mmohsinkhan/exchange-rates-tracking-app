'''
Serverless exchange rates tracking application deployment stack.
'''
from constructs import Construct
from aws_cdk import (
    Stack,
    Duration,
    triggers,
    RemovalPolicy,
    aws_logs as logs,
    aws_lambda as lambda_,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
    aws_events as events,
    aws_events_targets as events_targets
)

# Lambda code files path
LAMBDA_CODE = './lambda'
# Exchange rate update Lambda execution hour (UTC)
LAMBDA_SCHEDULED_HOUR = '16'


class ExchangeRatesTrackingStack(Stack):
    '''
    Serverless currency exchange rates tracking application.
    '''

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Dynamodb table for storing exchange rates data
        table = dynamodb.Table(self, 'table-exchange-rates',
                               partition_key=dynamodb.Attribute(name='id', type=dynamodb.AttributeType.STRING),
                               removal_policy=RemovalPolicy.DESTROY)

        # Lambda function for updating exchange rates
        lambda_update = lambda_.Function(self, 'update-exchange-rates',
                                         runtime=lambda_.Runtime.PYTHON_3_8,
                                         code=lambda_.Code.from_asset(LAMBDA_CODE),
                                         handler='update_exchange_rates.handler',
                                         timeout=Duration.minutes(5),
                                         log_retention=logs.RetentionDays.FIVE_DAYS)
        lambda_update.add_environment('TABLE_NAME', table.table_name)
        table.grant_read_write_data(lambda_update)

        # Schedule update Lambda function execution
        lambda_schedule = events.Schedule.cron(hour=LAMBDA_SCHEDULED_HOUR, minute='0')
        lambda_target = events_targets.LambdaFunction(handler=lambda_update)
        events.Rule(self, "exchange-rates-update-event",
                    description="Daily trigger for exchange rates update lambda function",
                    enabled=True,
                    schedule=lambda_schedule,
                    targets=[lambda_target])

        # Lambda function for reading exchange rates
        lambda_read = lambda_.Function(self, 'get-exchange-rates',
                                       runtime=lambda_.Runtime.PYTHON_3_8,
                                       code=lambda_.Code.from_asset(LAMBDA_CODE),
                                       handler='get_exchange_rates.handler',
                                       timeout=Duration.seconds(30),
                                       log_retention=logs.RetentionDays.FIVE_DAYS)
        lambda_read.add_environment('TABLE_NAME', table.table_name)
        table.grant_read_data(lambda_read)

        # REST API for fetching exchanges rates data
        api = apigateway.LambdaRestApi(self, 'api-exchange-rates',
                                       handler=lambda_read,
                                       proxy=False)
        api_resource = api.root.add_resource('exchangerates')
        api_resource.add_method('GET')

        # Trigger to populate initial exchange rates data in table after deployment
        trigger = triggers.TriggerFunction(self, 'init-exchange-rates',
                                           execute_after=[table, lambda_update],
                                           runtime=lambda_.Runtime.PYTHON_3_8,
                                           code=lambda_.Code.from_asset(LAMBDA_CODE),
                                           handler='update_exchange_rates.handler',
                                           timeout=Duration.minutes(5),
                                           log_retention=logs.RetentionDays.FIVE_DAYS,
                                           execute_on_handler_change=False)
        trigger.add_environment('TABLE_NAME', table.table_name)
        table.grant_read_write_data(trigger)
