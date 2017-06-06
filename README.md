# Salesforce Event Monitoring Log Retrieval
A lightweight Python command line utility that fetches Salesforce Event Monitoring Log Files for the purpose of consumption by log management and monitoring software.

# Setup
## Salesforce Event Monitoring
Setting up Event Monitoring is a two day process. Day one will be setup and on day two you can access actual log files. If you are using Lightning, you will need to switch to classic (as of Winter '17) to turn on Event Monitoring

Steps
* Go to Setup > Logs > Event Monitoring Setup
* Click enable
* Salesforce will start saving logs which can be accessed the next day

## Salesforce Connected App
You will need to create a Salesforce Connected app

Steps
* Go to Setup > Create > Apps
* Scroll down to Connected Apps, click New
* Enter the App Name, for instance, Event Monitoring Log Retrieval
* Enter Basic Information as necessary. Best practice is to use a service account rather than assigning to a specific administrator so that application access is not interrupted if an administrator leaves your team.
* Callback URL is required but is not necessary for this application. Enter the URL of your salesforce instance.
* Salesforce Event Monitoring Log Retrieval was built using the following Selected OAuth Scope, Access and Manage Your Data (api). Feel free to create custom permissions as needed.
* None of the information under Wave App Settings, Custom Connected App Handler, Mobile App Settings, or Canvas App Settings is required
* Click Save

## .env file
* Copy the .sample.env file and rename to .env  `cp .sample.env .env`
* Add site URI, do not include https://
* Enter user credentials including OAuth Consumer Key and Consumer Secret

# Requirements
* Salesforce Event Monitoring
* Python v2.7 or greater
* User with Salesforce API access

# Usage

## Run Locally
Retrieve logs for a given environment
```
$ retrieveLogs.py {orgname}
>>Fetching logs from, orgname.cs32.my.salesforce.com
```
Print debug output to terminal
```
$ retrieveLogs.py orgname -d
>>Fetching logs from, gsa-red--reddv10dvn.cs32.my.salesforce.com
>>Debug turned on
[TRUNCATED]
```
Display list of environments stored in .env
```
$ retrieveLogs.py -e
>>The following environments have credentials stored:
  - orgname1
  - orgname2
  - orgname3
>>You can use one of the sites by entering:

  $ python retrievePackage orgname
```
Display help
```
$ python retrieveLogs.py -h
usage: retrieveLogs.py [-h] [-e] [-d] [-l] [-v] [orgName]

Salesforce Event Monitoring Log Retrieval This python script will authenticate
against Salesforce and pull json responses containing api logs that may be
downloaded for consumption by a log processing application. Request responses
are logged in the /logs directory. Each run of this app will generate multiple
requests, those requests are merged into a single log file

positional arguments:
  orgName        enter the org key of the environment contained in .env

optional arguments:
  -h, --help     show this help message and exit
  -e, --env      display list of Salesforce environments contained in the .env
                 file
  -d, --debug    print results of program to terminal
  -l, --log      prints log of http requests to /logs folder
  -v, --verbose  prints full http request and response (status code and
                 headers) log to terminal. **NOTE, this argument prints a lot
                 of information to the terminal
```
Retrieve basic logs and store in logs/ directory
```
$ retrieveLogs.py {orgname} -l
>>Fetching logs from, orgname.cs32.my.salesforce.com
>>Logging turned on. File can be found at, logs/20161204-2027.34.log
```
Retrieve logs and display robust request log information including HTTP requests, response codes, and headers
```
$ retrieveLogs.py {orgname} -v
>>Fetching logs from, orgname.cs32.my.salesforce.com
[TRUNCATED]
```
## Setup CRON Job
```
$ crontab -e
0 1 * * * path/to/retrieveLogs.py {orgname}
```
