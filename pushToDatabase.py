import pyodbc
import pandas as pd
from requests import NullHandler
from cognitiveServices import cognitiveServices

# The purpose of it is simply making sure
# there is no data in a database, but gotta be 
# careful here to not remove things I do not want to
# remove
def resetDatabase(cursor):
    sql_push = '''       
        EXEC Twitter.ClearDatabase
    '''
    cursor.execute(sql_push)
    cursor.commit()

# Basically opens our database
def setDatabase(): ########### TO CHANGE ADD DATABASE
    server = ''
    database = ''
    username = ''
    password = ''

    connection = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=' +
                                server + ';DATABASE=' + database +
                                ';UID=' + username + ';PWD=' + password)
    cursor = connection.cursor()
    return cursor

# Main method that pushes all the data into the database
def push(TweetTopic,tweet_data):
    cursor = setDatabase()
    #resetDatabase(cursor) ---- Can be super useful for testing

    #Figuring out the number of users and tweets
    numOfUsers = len(tweet_data['includes']['users'])
    numOfTweets = len(tweet_data['data'])

    #Pushing User Data from 'includes' part of json
    for i in range(numOfUsers):
        userName = tweet_data['includes']['users'][i]['username']
        userId = tweet_data['includes']['users'][i]['id']
        fullName = tweet_data['includes']['users'][i]['name']
        #Removing non-askii characters from user names for readibility
        if not fullName.isascii():
            fullName = fullName.encode("ascii", "ignore")
        pushUser(userId,userName,fullName, cursor)
    
    print('\n------USER TABLE SUCCESS------PUSHED:', numOfUsers, '\n')

    numOfLocations = 0
    #Pushing Location Data from 'includes' part of json if such exist
    if 'places' in tweet_data['includes']:
        numOfLocations = len(tweet_data['includes']['places'])
        for i in range(numOfLocations):
            geoID = tweet_data['includes']['places'][i]['id']
            geoName = tweet_data['includes']['places'][i]['full_name']
            pushLocation(geoID, geoName, cursor)

    print('\n------LOCATIONS TABLE SUCCESS------PUSHED:', numOfLocations, '\n')

    #Pushing Tweet Data from 'data' part of json
    for i in range(numOfTweets):
        tweetId = tweet_data['data'][i]['id']
        authorID = tweet_data['data'][i]['author_id']
        tweetText = tweet_data['data'][i]['text']
        tweetDate = tweet_data['data'][i]['created_at']
        if 'geo' in tweet_data['data'][i]:
            geoID = tweet_data['data'][i]['geo']['place_id']
        else:
            geoID = None
        # If wanting to remove the non-askii characters from the tweet
        # If not tweetText.isascii():
        #     tweetText = tweetText.encode("ascii", "ignore")
        json = str(tweet_data['data'][i])
        cleanDate = (tweetDate[:10] + ' ' + tweetDate[11:19])
        pushTweet(tweetId, TweetTopic, authorID,tweetText, geoID, cleanDate, json, cursor)
        separateHash(tweetText, tweetId, cursor)

    print('\n------TWEET TABLE SUCCESS------PUSHED:', numOfTweets, '\n')
    

    """ 
        Cognitive sercices accepts only entrees at a time 
        So, having to slice the data entree to be 10 at a time
        ...
        When we have a non-multiple of 10, it does modulus devicion
        to decide how many elements it has to push
    """
    tweet_counter = 0
    grab_until = 10
    while tweet_counter < numOfTweets:  
        sentiments, key_phrases = cognitiveServices(tweet_data['data'][grab_until-10:grab_until])
        grab_until+=10
        tweet_counter+=10
        #Pushing sentiment and key phrases data
        rang = 10
        if tweet_counter > numOfTweets:
            rang = numOfTweets % 10
        for i in range(rang):
            pushSentiment(sentiments[i]['id'], sentiments[i]['sentiment'],
                            sentiments[i]['confidence_scores']['positive'],
                            sentiments[i]['confidence_scores']['neutral'],
                            sentiments[i]['confidence_scores']['negative'], cursor)

            # Now onto key phrases
            if len(key_phrases[i]) > 0:
                for phrase in key_phrases[i]['key_phrases']:
                    if(phrase.lower() != TweetTopic.lower()):
                        pushKeyPhrase(key_phrases[i]['id'], phrase, cursor)

    print('\n------PUSHING SENTIMENTS AND PHRASES SUCCESS------\n')

#Pushes into Tweets table
def pushTweet(id, TweetTopic, authorID, text, location,date, json, cursor):
    sql_push = '''
        EXEC Twitter.CreateTweet ?, ?, ?, ?, ?, ?, ?
    '''
    args = (id, TweetTopic, authorID, text, location, date, json)
    cursor.execute(sql_push, args)
    cursor.commit()

#Pushes into Users table
def pushUser(id,username, fullname, cursor):
    sql_push = '''       
        EXEC Twitter.CreateUser ?, ?, ?
    '''
    args = (id,username, fullname)
    cursor.execute(sql_push, args)
    cursor.commit()

#Pushes into Users table
def pushLocation(geoID,geoName, cursor):
    sql_push = '''       
        EXEC Twitter.CreateLocation ?, ?
    '''
    args = (geoID,geoName)
    cursor.execute(sql_push, args)
    cursor.commit()

#Separates the hashtags and pushes them in a table
def separateHash(tweetText, tweetId, cursor):
    while True:
            hashIndex = tweetText.find('#')
            if hashIndex == -1:
                break
            index = hashIndex+1
            hash = ''
            prohibited_symbols = ['#', '.', ',', '/', '!', '?', '\"', '\'', ' ', '[', ']', '*',';',':','@','$','%','(',')', '+', '=','-']
            while(tweetText[index] not in prohibited_symbols and tweetText[index].isascii()):
                hash += tweetText[index]
                index+=1
                if index == len(tweetText):
                    break
            pushHash(hash, tweetId, cursor)
            tweetText = tweetText[index::]

#Pushes a hashtag
def pushHash(hash, id, cursor):
    sql_push = '''       
        EXEC Twitter.CreateHash ?, ?
    '''
    args = (hash, id)
    cursor.execute(sql_push, args)
    cursor.commit()

#Pushes a sentiment
def pushSentiment(tweetID, sentiment, positive, neutral, negative, cursor):
    sql_push = '''       
        EXEC Twitter.CreateSentiment ?, ?, ?, ?, ?
    '''
    args = (tweetID, sentiment, positive, neutral, negative)
    cursor.execute(sql_push, args)
    cursor.commit()

#Pushes a key phrase
def pushKeyPhrase(tweetID, phrase, cursor):
    sql_push = '''       
        EXEC Twitter.CreateKeyPhrase ?, ?
    '''
    args = (tweetID, phrase)
    cursor.execute(sql_push, args)
    cursor.commit()