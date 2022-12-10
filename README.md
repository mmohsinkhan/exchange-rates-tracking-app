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
			"currency": "BGN",
			"rate": "1.9558",
			"change": "0.0"
		},
		{
			"currency": "BRL",
			"rate": "5.5457",
			"change": "+0.0577"
		},
		{
			"currency": "CAD",
			"rate": "1.438",
			"change": "+0.0073"
		},
		{
			"currency": "CHF",
			"rate": "0.9856",
			"change": "-0.0033"
		},
		{
			"currency": "CNY",
			"rate": "7.3475",
			"change": "+0.0151"
		},
		{
			"currency": "CZK",
			"rate": "24.293",
			"change": "-0.031"
		},
		{
			"currency": "DKK",
			"rate": "7.4379",
			"change": "-0.0003"
		},
		{
			"currency": "GBP",
			"rate": "0.8595",
			"change": "-0.0031"
		},
		{
			"currency": "HKD",
			"rate": "8.2169",
			"change": "+0.028"
		},
		{
			"currency": "HRK",
			"rate": "7.555",
			"change": "-0.0003"
		},
		{
			"currency": "HUF",
			"rate": "417.53",
			"change": "-0.13"
		},
		{
			"currency": "IDR",
			"rate": "16453.46",
			"change": "+29.54"
		},
		{
			"currency": "ILS",
			"rate": "3.6128",
			"change": "-0.0078"
		},
		{
			"currency": "INR",
			"rate": "86.9535",
			"change": "+0.278"
		},
		{
			"currency": "ISK",
			"rate": "149.5",
			"change": "0.0"
		},
		{
			"currency": "JPY",
			"rate": "143.3",
			"change": "-0.45"
		},
		{
			"currency": "KRW",
			"rate": "1373.94",
			"change": "-13.12"
		},
		{
			"currency": "MXN",
			"rate": "20.849",
			"change": "+0.1501"
		},
		{
			"currency": "MYR",
			"rate": "4.6512",
			"change": "+0.0255"
		},
		{
			"currency": "NOK",
			"rate": "10.5345",
			"change": "+0.0465"
		},
		{
			"currency": "NZD",
			"rate": "1.6482",
			"change": "-0.0065"
		},
		{
			"currency": "PHP",
			"rate": "58.47",
			"change": "+0.237"
		},
		{
			"currency": "PLN",
			"rate": "4.6869",
			"change": "+0.0016"
		},
		{
			"currency": "RON",
			"rate": "4.9224",
			"change": "+0.0093"
		},
		{
			"currency": "SEK",
			"rate": "10.9188",
			"change": "+0.0128"
		},
		{
			"currency": "SGD",
			"rate": "1.426",
			"change": "+0.0004"
		},
		{
			"currency": "THB",
			"rate": "36.656",
			"change": "+0.097"
		},
		{
			"currency": "TRY",
			"rate": "19.6872",
			"change": "+0.0758"
		},
		{
			"currency": "USD",
			"rate": "1.0559",
			"change": "+0.004"
		},
		{
			"currency": "ZAR",
			"rate": "18.2358",
			"change": "+0.2133"
		}
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

*TriggerFunction* in CDK is used to execute Lambda during deployment, for populating initial exchange rates data in database.
Localstack does not support *TriggerFunction*. After deployment we have to manually invoke the Lambda function once.
```bash
# Get list of deployed Lambda functions
$ awslocal lambda list-functions
# From the response, find Lambda having 'updateexchangerates' in function name
# Manually invoke Lambda function to populate initial data in database
$ awslocal lambda invoke --function-name <function name> outfile
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
