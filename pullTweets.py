import requests
#import os
import json

def pull(numOfTweets, topicPull):
    bearer_token = '<A PERSONAL TOKEN GOES HERE>' ########### TO CHANGE
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    # http header for the request, passing required information
    headers = {
        'Authorization': 'Bearer {}'.format(bearer_token),
        'User-Agent': 'TopicPull-<USER NAME>'  ########### TO CHANGE
    }
    # The query parameters
    # https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent
    query_params = {
        'query': topicPull +' -is:retweet lang:en',
        'max_results': 100,
        'tweet.fields': 'created_at,geo',
        'expansions': 'author_id,geo.place_id'
    }

    tweet_counter = 0
    
    #Creates a one big dictionary where we will store our data
    parse_json_total = {'data': [], 
                        'includes': {
                            'users': [],
                            'places': []
                        }}

    while tweet_counter < numOfTweets:   
        #Making the API call and dumping results into a JSON
        response = requests.request("GET", search_url, headers=headers, params=query_params)
        parse_json = response.json()

        next_token = parse_json['meta']['next_token']    
           
        tweet_counter += 100

        # Add/set parameter for "next_token" to continue the search
        query_params['next_token'] = next_token

        # Having to add elements one by one.
        for data in parse_json['data']:
            parse_json_total['data'].append(data) 
            
        for includes in parse_json['includes']['users']:
            parse_json_total['includes']['users'].append(includes) 
        
        if 'places' in parse_json['includes']:
            for places in parse_json['includes']['places']:
                parse_json_total['includes']['places'].append(places) 

    return parse_json_total