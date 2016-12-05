import datetime
import getopt
import json
import logging
import os
import requests
import sys
from FileWriter import FileWriter
from requests.auth import HTTPBasicAuth

"""
Salesforce API
"""
class SalesforceApi:

    def __init__(self,environment,debug=0):
        self.username = environment['username']
        self.password = environment['password']
        self.securityToken = environment['securityToken']
        self.sfConsumerKey = environment['consumerKey']
        self.sfConsumerSecret = environment['consumerSecret']
        self.sfURL = environment['salesforceURL']
        self.accessToken = ''
        self.debug = debug
        self.logPath = 'logs/tmp_'+datetime.datetime.now().strftime('%Y%m%d-%H%M.%S')+'.json'
        if self.debug:
            print "salesforce api initiated"


    def authenticate(self):
        """Authenticate against Salesforce using an OAuth connection. Sets the accessToken attribute of the SalesforceApi class
        Parameters
        ----------

        Returns
        -------
        void
        """
        # Login Step 1, Request Access token
        # To do so, you must have created a connected App in Salesforce and have a clientId and clientSecret available along with username, password, and securityToken
        authHeaders = {'Content-Type': 'application/x-www-form-urlencoded'}
        # Constrcut the body of the request for access token
        payload = {'grant_type':'password','client_id':self.sfConsumerKey,'client_secret':self.sfConsumerSecret,'username':self.username,'password':self.password+self.securityToken}

        # Post to https://login.salesforce.com/services/oauth2/token
        rawResponse = requests.post('https://'+self.sfURL+'/services/oauth2/token',headers=authHeaders, data=payload)

        response = json.loads(rawResponse.text)
        if self.debug:
            print "[DEBUG] authenticate >> "
            print response
        self.accessToken = response['access_token']


    def queryEventLogFile(self, eventType=''):
        """Query the Event Log File object for API events. Requires that accessToken is set
        Parameters
        ----------

        Returns
        -------
        json query response
        """
        # If accessToken is not set, throw error
        if (self.accessToken == ''):
            raise ValueError('accessToken has not been set, run authenticate method to set token')
            exit
        # Set headers
        headers = {'Content-Type': 'application/json','Authorization':'Bearer '+self.accessToken}

        # Build WHERE clause
        whereClause = ''
        if eventType != '':
            whereClause = "WHERE++EventType+=+'"+eventType+"'"
        # post the request
        rawResponse = requests.get("https://"+self.sfURL+"/services/data/v32.0/query?q=SELECT+Id+,+EventType+,+LogFile+,+LogDate+,+LogFileLength+FROM+EventLogFile+"+whereClause, headers=headers)
        response = json.loads(rawResponse.text)

        if self.debug:
            print "[DEBUG] queryEventLogFile >> "
            print response

        return response

    def eventLogFile(self,eventLogFile):
        """Retrieves a single Event File Log and writes it to the appropriate directory
        Parameters
        ----------
        param: eventLogFile
            ex:
            {
              'LogFileLength': 5199.0,
              'EventType': 'API',
              'LogDate': '2016-11-22T00:00:00.000+0000',
              'attributes': {
                'url': '/services/data/v32.0/sobjects/EventLogFile/0ATr00000000TWHGA2',
                'type': 'EventLogFile'
              },
              'LogFile': '/services/data/v32.0/sobjects/EventLogFile/0ATr00000000TWHGA2/LogFile',
              'Id': '0ATr00000000TWHGA2'
            }

        Returns
        -------
        csv containing event file log
        """
        if (self.accessToken == ''):
            raise ValueError('accessToken has not been set, run authenticate method to set token')
            exit

        eventFileId = eventLogFile['Id']
        headers = {'Authorization':'Bearer '+self.accessToken,'X-PrettyPrint':'1','Accept-Encoding': 'gzip'}
        rawResponse = requests.get('https://'+self.sfURL+'/services/data/v32.0/sobjects/EventLogFile/'+eventFileId+'/LogFile',headers=headers)


        if self.debug:
            print "[DEBUG] eventLogFile >> "
            print rawResponse
            print rawResponse.content

        # if self.log:
        #     w = FileWriter('log', eventFileId)
        #     w.writeFile(rawResponse.content)

        w = FileWriter(eventLogFile)
        w.writeFile(rawResponse.content)

        return rawResponse
