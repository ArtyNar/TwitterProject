import matplotlib.pyplot as plt
import numpy as np
from pullTweets import pull
from pushToDatabase import push

#To change the number of tweets pulled and the hashtag searched
numOfTweets = 1000
TweetTopic1 = 'Topic1'
TweetTopic2 = 'Topic2'
TweetTopic3 = 'Topic3'

tweet_data = pull(numOfTweets, TweetTopic1)

print(tweet_data) # For validation only

push(TweetTopic1, tweet_data)

