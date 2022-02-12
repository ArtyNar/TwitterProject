from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def cognitiveServices(tweet_data):
    api_key='bb59020e2b4c4bf59f04d2380b221a1e' 
    api_endpoint = 'https://twitterproject.cognitiveservices.azure.com/'
    api_call = TextAnalyticsClient(endpoint=api_endpoint, credential=AzureKeyCredential(api_key))

    api_document = []
    for tweet in tweet_data:
        api_document.append({
            'id': str(tweet['id']), 
            'text': tweet['text']
        })    
    
    sentiments = api_call.analyze_sentiment(api_document, show_opinion_mining=True)
    key_phrases = api_call.extract_key_phrases(api_document)

    return sentiments, key_phrases


    # print(results[0]['id'])
    # print(tweet_data['data'][0]['text'])
    # print(results[0]['sentiment'])
    # print(results[0]['confidence_scores'])

    # for sentiment in results:
    #     print(sentiment['id'], ' - ', sentiment['sentiment'])
    #     print(sentiment['confidence_scores']['positive'], 
    #             sentiment['confidence_scores']['neutral'], 
    #             sentiment['confidence_scores']['negative'])

    # key_results = api_call.extract_key_phrases(api_document)

    # for key_result in key_results:
    #     print(key_result['id'])
    #     #print(key_result)
    #     for phrases in key_result['key_phrases']:
    #         print(phrases)