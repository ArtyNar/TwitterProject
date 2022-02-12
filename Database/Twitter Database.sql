-- # Design your database
-- # Store data about tweets - the tweet, the id, who made the tweet, location (if avaialable), Hashtags
-- # if fully normalized - User table, Tweet table, HashTag, Location table junction table - 
-- # reasonable - Tweet table, HashTag table, junction between Tweet & HashTags (because of many-to-many)

-- # Sentiment - 
-- #'id': '1458635016875950083', 'sentiment': 'mixed',
-- #'confidence_scores': SentimentConfidenceScores(positive=0.32, neutral=0.01, negative=0.67),
-- # Negative tweet
-- # confidence scores table?
-- # TweetSentiment table?  Tweet ID, Setiment (mixed)
-- # Lookup Table -


-- CREATE SCHEMA Twitter
-- GO
USE artemkoval
DROP TABLE IF EXISTS KeyPhrases, Sentiments, TweetToHashtag, Hashtags, Tweets, Users, Locations--, ConfidenceTypes, TweetConfidence
GO

USE artemkoval
DROP TABLE IF EXISTS Twitter.KeyPhrases, Twitter.Sentiments, Twitter.TweetToHashtag, Twitter.Hashtags, Twitter.Tweets, Twitter.Users, Twitter.Locations--, ConfidenceTypes, TweetConfidence
GO

CREATE TABLE Twitter.Users
(
	UserID bigint NOT NULL PRIMARY KEY,
	Username varchar(20) NOT NULL,
	FullName varchar(max) NOT NULL
)

CREATE TABLE Twitter.Locations
(
	EntreeID bigint IDENTITY(1,1) PRIMARY KEY NOT NULL,
	GeoID varchar(max) NOT NULL,
	LocationName varchar(max) NOT NULL
)

CREATE TABLE Twitter.Tweets
(
	TweetID bigint NOT NULL PRIMARY KEY,
	TweetText varchar(max) NOT NULL,
	TweetTopic varchar(20) NOT NULL,
	AuthorID bigint NOT NULL REFERENCES Twitter.Users(UserID),
	TweetLocation bigint REFERENCES Twitter.Locations(EntreeID),
	TweetDate varchar(50),
	OriginalJSON varchar(max) NOT NULL,
)

CREATE TABLE Twitter.Hashtags
(
	HashID bigint IDENTITY(1,1) PRIMARY KEY NOT NULL,
	HashText varchar(20) NOT NULL UNIQUE
)

CREATE TABLE Twitter.TweetToHashtag
(
	TweetID bigint REFERENCES Twitter.Tweets(TweetID),
	HashID bigint REFERENCES Twitter.Hashtags(HashID)
)

CREATE TABLE Twitter.Sentiments
(
	TweetID bigint REFERENCES Twitter.Tweets(TweetID),
	Sentiment varchar(8),
	ConfidencePositive float,
	ConfidenceNeutral float,
	ConfidenceNegative float
)

CREATE TABLE Twitter.KeyPhrases
(
	TweetID bigint REFERENCES Twitter.Tweets(TweetID),
	KeyPhrase varchar(20)
)


-- CREATE TABLE ConfidenceTypes
-- (
-- 	ConfidenceTypeKey bigint PRIMARY KEY NOT NULL,
-- 	ConfidenceLabel varchar(100) NOT NULL
-- )

-- CREATE TABLE TweetConfidence
-- (
-- 	TweetConfidenceKey int IDENTITY(1,1) PRIMARY KEY NOT NULL,
-- 	TweetSentimentKey bigint,
-- 	ConfidenceKey bigint,
-- 	ConfidenceScore float
-- )


SELECT * FROM Twitter.Users
SELECT * FROM Twitter.Tweets
SELECT * FROM Twitter.Hashtags
SELECT * FROM Twitter.TweetToHashtag
SELECT * FROM Twitter.Locations
SELECT * FROM Twitter.KeyPhrases
SELECT * FROM Twitter.Sentiments

SELECT COUNT(*) FROM Twitter.Users
SELECT COUNT(*) FROM Twitter.Tweets
SELECT COUNT(*) FROM Twitter.Sentiments
SELECT COUNT(*) FROM Twitter.KeyPhrases
SELECT COUNT(*) FROM Twitter.Hashtags

