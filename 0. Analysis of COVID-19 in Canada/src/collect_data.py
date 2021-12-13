import tweepy as tw
import pandas as pd

consumer_key= 'INSERT'
consumer_secret= 'INSERT'
access_token= 'INSERT'
access_token_secret= 'INSERT'
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# FIlter tweets by words and hashtags
words = ['Covid', 'vaccination', 'Pfizer', 'Moderna', 'corona', 'AstraZeneca', 'Janssen']
# Get tweets from Canada
geocodes = ['56.988998,-133.811869,1500km', '55.705271,-77.549072,1500km']
df=pd.DataFrame()
for word in words:
    for geocode in geocodes:
        tweets = tw.Cursor(api.search_tweets, q=word, lang='en', geocode=geocode, tweet_mode='extended').items(1500)
        clean_tweets = [[tweet.id, tweet.full_text, tweet.created_at, tweet.user.location] for tweet in tweets]
        tweet_text = pd.DataFrame(data=clean_tweets, columns=['id','text','time', 'location'])
        if (words.index(word) == 0) and (geocodes.index(geocode) == 0):
            tweet_text.to_csv('collected_data_full_text.csv', mode='w')
        else:
            tweet_text.to_csv('collected_data_full_text.csv', mode='a', header=False)
