import tweepy

# OAuth is the preferred method for authenticating to Twitter
# Consumer keys are under the application's Details page at
# http://dev.twitter.com/apps

consumer_key = 'rxbw7bzT55aGcAfwuGVhESbYO'
consumer_secret = 'k5roYh4ZRpefcKRpvbcICETWckxnzvVJsWGTMnwSRSzHLsrunm'
access_token = '1119404173794037760-MOlDKaPnJ9tRltnzmvXpjSm1K8YDYZ'
access_token_secret = 'WNSjFMUqIN5d2G9YI6WTy4b00AHZQBpfLAIRONXVXrLhD'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
print(api.me().name) # was authentication successful?

users = api.search_users(q="special collections library" [20])
print(users)