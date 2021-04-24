'''
This file sets up the basic environment needed to pull data from the instagram API. This includes access credentials and basic api endpoint URLS, along with api call functions.
A significant portion of this code came from https://github.com/imakashsahu/Instagram-Graph-API-Python/, although it has been heavily modified. 
'''
import requests
import json
import os


def getEndpointBase(credentials):
	return credentials['graph_domain'] + credentials['graph_version'] + '/'

def getCreds() :
	access_token = os.getenv('IG_API_TOKEN')
	client_secret = os.getenv('IG_CLIENT_SECRET')
	creds = {
		'access_token':access_token
		,'client_id':'482649729602172'
		,'client_secret':client_secret
		,'graph_domain':'https://graph.facebook.com/'
		,'graph_version':'v7.0'
		,'debug':'no'
		,'page_id':'102861825285216'
		,'instagram_account_id':'17841403107366659'
	}
	print(client_secret, access_token)
	creds['endpoint_base'] = getEndpointBase(creds)
	return creds

def makeApiCall(url, endpointParams, debug = 'no') :

	data = requests.get( url, endpointParams ) # make get request

	response = {
		'url':url
		,'endpoint_params':endpointParams
		,'endpoint_params_pretty':json.dumps(endpointParams, indent = 4)
		,'json_data': json.loads(data.content)
		,'json_data_pretty':json.dumps(json.loads(data.content), indent = 4)
	}
	#response = dict() # hold response info
	#response['url'] = url # url we are hitting
	#response['endpoint_params'] = endpointParams #parameters for the endpoint
	#response['endpoint_params_pretty'] = json.dumps( endpointParams, indent = 4 ) # pretty print for cli
	#response['json_data'] = json.loads( data.content ) # response data from the api
	#response['json_data_pretty'] = json.dumps( response['json_data'], indent = 4 ) # pretty print for cli

	if ( 'yes' == debug ) : # display out response info
		displayApiCallData( response ) # display response

	return response # get and return content



def displayApiCallData( response ) :
	""" Print out to cli response from api call """

	print ("\nURL: ") # title
	print (response['url']) # display url hit
	print ("\nEndpoint Params: ") # title
	print (response['endpoint_params_pretty']) # display params passed to the endpoint
	print ("\nResponse: ") # title
	print (response['json_data_pretty']) # make look pretty for cli
