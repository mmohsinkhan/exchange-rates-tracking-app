# Serverless Exchange Rates Tracking Application

Exchange rates tracking application developed in AWS lambda environment, deployable using AWS CDK. 
Exchange rates are collected from European Central Bank [website](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html).

## Components

* Dynamodb table for storing exchange rates.
* Lambda function for periodically updating exchange rates. Scheduled to run at 16:00:00 UTC daily.
* REST API for fetching exchange rates.
* Lambda function connected to the REST API, for reading exchange rates from Dynamodb.

![Architecture](architecture.png?raw=true)

## REST API

Once deployed, application exposes a REST API endpoint providing current exchange rates along with the change with respect to previous day.

### Sample Response
```javascript
{
    "updated_at": "2022-12-10",
    "base_currency": "EUR",
    "exchange_rates": [
        {
            "currency": "AUD",
            "rate": "1.5553",
            "change": "-0.0037"
        },
        {
            "currency": "ISK",
            "rate": "149.5",
            "change": "0.0"
        },
        {
            "currency": "USD",
            "rate": "1.0559",
            "change": "+0.004"
        },
		...
    ]
}
```


## Deployment
### Required Tool

| Tool       | Tested Version  |
| --------   | --------------- |
| AWS CLI    | 2.9.5           |
| AWS CDK    | 2.54.0          |
| NodeJS     | 18.12.1         |
| npm        | 8.19.2          |
| Python3    | 3.8.15          |
| pip        | 22.3            |
| Localstack | 1.3.0           | 

> **Note**
> Make sure 'python3' executable is added to path and accessible using command line.

[Install](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) AWS CLI.

Install AWS CDK
```bash
$ npm install -g aws-cdk
```

Clone this repository and change working directory to repository root folder.

Create and activate Python virtual environment
```bash
# Create virtual environment
$ python3 -m venv .venv
# Activate virtual environment
$ source .venv/bin/activate
``` 

Install required Python packages
```bash
$ pip install -r requirements.txt
```

From here you can deploy application either on AWS or locally using Localstack.

### **Deploy on AWS**

[Configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) AWS CLI.

> **Note**
> AWS CLI should be configured with user credentials having privileges to create resources on AWS that are required for the application.

Bootstrap CDK to setup necessary resources in AWS to carry out CDK deployments
```bash
$ cdk bootstrap
```

(Optional) Synthesize code to generate CloudFormation template
```bash
$ cdk synth
```

Deploy application on AWS
```bash
$ cdk deploy
```

On successful deployment, link to a public REST endpoint shall be printed on console. Append resource name **exchangerates** to the link for exchange rates API
```bash
# Sample REST endpoint
https://**********.execute-api.us-east-1.amazonaws.com/prod/
# Exchange rates API
https://**********.execute-api.us-east-1.amazonaws.com/prod/exchangerates

# Curl for the API
curl -X GET https://**********.execute-api.us-east-1.amazonaws.com/prod/exchangerates
```
(Optional) Delete application, removing allocated resources
```bash
$ cdk destroy
```

### **Deploy locally on Localstack**

[Install](https://docs.localstack.cloud/getting-started/installation/) and start Localstack.

Install *cdklocal* tool
```bash
$ npm install -g aws-cdk-local
```

Install *awslocal* tool
```bash
$ pip install awscli-local
```

Bootstrap Localstack for CDK deployment
```bash
$ cdklocal bootstrap
```

(Optional) Synthesize code to generate CloudFormation template
```bash
$ cdklocal synth
```

Deploy application on Localstack
```bash
$ cdklocal deploy
```

*TriggerFunction* in CDK is used to execute Lambda during deployment, for populating initial exchange rates data.
Localstack does not support *TriggerFunction*. So after deployment Lambda function has be manually invoked once.
```bash
# Get list of deployed Lambda functions
$ awslocal lambda list-functions
# From the response, find Lambda having 'updateexchangerates' in function name
# Manually invoke Lambda function to populate initial data in database
$ awslocal lambda invoke --function-name <function name> /dev/null
```

Link to a local REST endpoint shall be printed on deployment console. Append resource name **exchangerates** to the link for exchange rates API
```bash
# Sample REST endpoint
https://**********.execute-api.localhost.localstack.cloud:4566/prod/
# Exchange rates API
https://**********.execute-api.localhost.localstack.cloud:4566/prod/exchangerates

# Curl for the API
curl -X GET https://**********.execute-api.us-east-1.amazonaws.com/prod/exchangerates
```
