GO
CREATE OR ALTER PROCEDURE Twitter.CreateTweet
(
	@TweetID bigint,
	@TweetTopic varchar(20),
	@AuthorID bigint,
 	@TweetText varchar(max),
	@TweetLocation varchar(max),
	@TweetDate varchar(50),
	@JSON varchar(max)
)
AS
BEGIN 
	IF (SELECT COUNT(*) FROM Tweets WHERE TweetID = @TweetID) = 0
	BEGIN
		INSERT Tweets (TweetID, TweetTopic, AuthorID, TweetText, TweetLocation, TweetDate, OriginalJSON) 
		VALUES (@TweetID, @TweetTopic, @AuthorID, @TweetText, (SELECT EntreeID FROM Locations WHERE GeoID = @TweetLocation), CAST(@TweetDate AS DATETIME), @JSON)	
	END
END
GO

GO
CREATE OR ALTER PROCEDURE Twitter.CreateUser
(
	@UserID bigint,
	@Username varchar(20),
	@FullName varchar(max)
)
AS
BEGIN 
	IF (SELECT COUNT(*) FROM Twitter.Users WHERE UserID = @UserID) = 0
	BEGIN
		INSERT Twitter.Users (UserID, Username, FullName) 
		VALUES (@UserID, @Username, @FullName)	
	END
END
GO

GO
CREATE OR ALTER PROCEDURE Twitter.CreateLocation
(
	@geoID varchar(max),
	@geoName varchar(max)
)
AS
BEGIN 
	IF (SELECT COUNT(*) FROM Twitter.Locations WHERE GeoID = @geoID) = 0
	BEGIN
		INSERT Twitter.Locations (GeoID, LocationName) 
		VALUES (@geoID, @geoName)	
	END
END
GO

GO
CREATE OR ALTER PROCEDURE Twitter.CreateHash
(
	@Hash varchar(20),
	@TweetID bigint
)
AS
BEGIN 
	IF (SELECT COUNT(*) FROM Twitter.Hashtags WHERE HashText = @Hash) = 0
	BEGIN 
		INSERT Twitter.Hashtags (HashText) 
		VALUES (@Hash)	
		
		INSERT Twitter.TweetToHashtag (TweetID, HashID) 
		VALUES (@TweetID, (SELECT HashID FROM Twitter.Hashtags WHERE HashText = @Hash)) 
	END
END
GO

GO
CREATE OR ALTER PROCEDURE Twitter.CreateSentiment
(
	@TweetID bigint,
	@Sentiment varchar(8),
	@Positive float,
	@Neutral float,
	@Negative float
)
AS
BEGIN 
	IF (SELECT COUNT(*) FROM Twitter.Sentiments WHERE TweetID = @TweetID) = 0
	BEGIN
		INSERT Twitter.Sentiments (TweetID, Sentiment, ConfidencePositive, ConfidenceNeutral, ConfidenceNegative) 
		VALUES (@TweetID, @Sentiment, @Positive, @Neutral, @Negative) 
	END
END
GO

GO
CREATE OR ALTER PROCEDURE Twitter.CreateKeyPhrase
(
	@TweetID bigint,
	@Phrase varchar(20)
)
AS
BEGIN 
	INSERT Twitter.KeyPhrases (TweetID, KeyPhrase) 
	VALUES (@TweetID, @Phrase) 
END
GO


GO
CREATE OR ALTER PROCEDURE Twitter.ClearDatabase
AS
BEGIN 
	DELETE FROM Twitter.KeyPhrases
	DELETE FROM Twitter.Sentiments
	DELETE FROM Twitter.TweetToHashtag
	DELETE FROM Twitter.Hashtags
	DELETE FROM Twitter.Tweets
	DELETE FROM Twitter.Users
	DELETE FROM Twitter.Locations
END
GO

GO
CREATE OR ALTER VIEW Twitter.ConfidenceClean
AS 
(
	SELECT 
		T.TweetID,
		T.TweetTopic,
		CASE 
			WHEN S.ConfidenceNegative > S.ConfidenceNeutral AND S.ConfidenceNegative > S.ConfidencePositive THEN S.ConfidenceNegative
			WHEN S.ConfidenceNeutral > S.ConfidenceNegative AND S.ConfidenceNeutral > S.ConfidencePositive THEN S.ConfidenceNeutral
			WHEN S.ConfidencePositive > S.ConfidenceNegative AND S.ConfidencePositive > S.ConfidenceNeutral THEN S.ConfidencePositive
			WHEN S.ConfidencePositive = S.ConfidenceNegative AND S.ConfidencePositive = S.ConfidenceNeutral THEN S.ConfidencePositive
		END AS Confidence
	FROM
		Twitter.Tweets T
		JOIN Twitter.Sentiments S ON T.TweetID = S.TweetID
)
GO 

-- SELECT 
-- 	* 
-- FROM 
-- 	Twitter.ConfidenceClean