'''
Lambda function code for updating exchanges rates in Dynamodb table.
'''
import os
import io
import csv
import logging
import zipfile
import urllib.request
from datetime import datetime

import boto3

# Exchange rates zip file download link
DOWNLOAD_URL = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip'

# Logger
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

# Dynamodb table name
TABLE_NAME = os.environ['TABLE_NAME']

# Endpoint URL, required for execution on localstack
if 'LOCALSTACK_HOSTNAME' in os.environ:
    ENDPOINT_URL = f'http://{os.environ["LOCALSTACK_HOSTNAME"]}:4566'
else:
    ENDPOINT_URL = None


def handler(event, context):
    '''
    Update exchange rates in database.
    '''
    LOGGER.info('Getting exchange rates data from European Central Bank')
    date, exchange_rates = get_exchange_rates()
    LOGGER.info('Updating exchange rates in database')
    update_exchange_rates(date, exchange_rates)
    LOGGER.info('Job completed')


def update_exchange_rates(date, exchange_rates):
    '''
    Update exchange rates in database.
    '''
    dynamodb = boto3.resource('dynamodb', endpoint_url=ENDPOINT_URL)
    table = dynamodb.Table(TABLE_NAME)
    # Batch write to database
    with table.batch_writer() as writer:
        # Exchange rates
        for currency, data in exchange_rates.items():
            data['id'] = currency
            writer.put_item(Item=data)
        # Dates
        writer.put_item(Item={'id': 'publish_date', 'value': date})
        writer.put_item(Item={'id': 'update_date', 'value': datetime.utcnow().strftime('%Y-%m-%d')})


def get_exchange_rates():
    '''
    Get exchange rate data (current and difference) from European Central Bank.
    '''
    # Download zip file
    response = urllib.request.urlopen(DOWNLOAD_URL, timeout=30)
    # Extract zip file and read data from csv
    with zipfile.ZipFile(io.BytesIO(response.read())) as zip_file:
        csv_file = zip_file.open(zip_file.namelist()[0])
        csv_reader = csv.DictReader(io.TextIOWrapper(csv_file, 'utf-8'))
        data = [row for row in csv_reader]
    # Latest and previous day exchange rates
    latest_rates = {k.strip(): v.strip() for k, v in data[0].items() if k.strip()}
    date = latest_rates.pop('Date', None)
    previous_rates = {k.strip(): v.strip() for k, v in data[1].items() if k.strip()}
    previous_rates.pop('Date', None)
    # Exchange rates document with current rates and difference
    exchange_rates = {}
    for currency, rate in latest_rates.items():
        if rate == 'N/A' or previous_rates.get(currency, 'N/A') == 'N/A':
            continue
        # Previous rate
        p_rate = float(previous_rates[currency])
        # Difference
        diff = float(rate) - p_rate
        diff = round(diff, 4) or 0.0
        # Difference in percentage
        diff_percent = (diff / p_rate) * 100
        diff_percent = round(diff_percent, 4) or 0.0
        # Add sign to difference and percentage
        diff = f'+{diff}' if diff > 0 else f'{diff}'
        diff_percent = f'+{diff_percent} %' if diff_percent > 0 else f'{diff_percent} %'
        exchange_rates[currency] = {'value': rate, 'diff': diff, 'diff_percent': diff_percent}
    return date, exchange_rates
