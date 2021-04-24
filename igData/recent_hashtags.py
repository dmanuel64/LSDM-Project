import os, csv
import time
from defines import getCreds, makeApiCall
import sys
import json
import mongoapi

#Gets the ID of a hashtag name passed to it
def getHashtagInfo(params, hashtag_name) :
    endpointParams = {
        'user_id':params['instagram_account_id']
        ,'q':hashtag_name
        ,'fields':'id,name'
        ,'access_token':params['access_token']
    }

    url = params['endpoint_base'] + 'ig_hashtag_search' # endpoint url

    return makeApiCall(url, endpointParams, params['debug'])


#Gets recent media for a given hashtag. This will try to get up to count number of posts, although the number of posts
#returned by the api may end up being more than this. Usually the total number of returned posts will end up being at most
#count + 24.
def hashtagMediaWrapper(hashtag_name, count=25):
    #Get credentials from defines.py
    params = getCreds()

    #Build a dict of parameters to pass when making an api request
    endpointParams = {
        'user_id':params['instagram_account_id']
        ,'fields':'id,permalink,comments_count,like_count,media_type,media_url,caption'
        ,'access_token':params['access_token']
        ,'limit':count
    }

    

    #Get the ID for the requested hashtag
    hashtagInfoResponse = getHashtagInfo(params, hashtag_name) 
    params['hashtag_id'] = hashtagInfoResponse['json_data']['data'][0]['id']

    #Build a base URL for the API request
    params['type'] = 'recent_media' # set call to get recent media for hashtag
    endpointParams['url'] = params['endpoint_base'] + params['hashtag_id'] + '/' + params['type'] # endpoint url
    
    #Get up to 50 recent posts by hashtag, and save pagination cursor
    partResponse = makeApiCall(endpointParams['url'], endpointParams, params['debug'] )
    endpointParams['after'] = partResponse['json_data']['paging']['cursors']['after']

    #Save the data portion of the response
    fullResponse = partResponse['json_data']['data']

    #It's possible that we've been exceeded rate limits. In this case, the only indication we'll receive is that the response will be empty. In this case, stop trying the endpoint, because it'll only make things worse
    if len(fullResponse) == 0:
        return fullResponse

    #Keep requesting more media while we have not met the requested amount
    while len(fullResponse) < count:
        #Decrement the limit parameter passed to the api. This should allow us to eventually get the exact number of posts requested
        endpointParams['limit'] -= len(fullResponse)
        #Sleep to try to avoid being rate limited
        time.sleep(1)
        #Repeat the request 
        partResponse = makeApiCall(endpointParams['url'], endpointParams, params['debug'] )
        fullResponse.extend(partResponse['json_data']['data'])
        try:
            #Try to get the cursor for the next page. If this fails, there's no more data, so exit
            endpointParams['after'] = partResponse['json_data']['paging']['cursors']['after']
        except:
            break
    return fullResponse

if __name__ == '__main__':
    hashtag = input()
    output = hashtagMediaWrapper(hashtag, count=25)
    if len(output) > 0:
        mongoapi.insertMongoPosts(output, "instagram", hashtag)
        print(output[-1])
    else:
        print("Empty Response")
