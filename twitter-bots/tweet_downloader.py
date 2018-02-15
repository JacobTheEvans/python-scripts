import requests
import json
import time

from requests_oauthlib import OAuth1

#authentication pieces
client_key = ""
client_secret = ""
token = ""
token_secret = ""

#the base for all Twiiter calls
base_twitter_url = "https://api.twitter.com/1.1/"

#setup authentication
oauth = OAuth1(client_key,client_secret,token,token_secret)

#
#Download Tweets from a user profile
#
def download_tweets(screen_name,number_of_tweets):

    api_url = "%s/statuses/user_timeline.json?" % base_twitter_url
    api_url += "screen_name=%s&" % screen_name
    api_url += "count=%d" % number_of_tweets
    print("[+] Fulll Twitter URL %s" % api_url)

    #send requests to Twitter
    response = requests.get(api_url, auth=oauth)

    if response.status_code == 200:
        tweets = json.loads(response.content)
        return tweets

    return None

def main():
    #get a list of Tweets
    tweet_list = download_tweets("rirocks",10)

    if tweet_list is not None:
        #loop over each Tweet and print the date and text
        for tweet in tweet_list:
            print "%s\t%s" % (tweet["created_at"],tweet["text"])
    else :
        print "[-] No Tweets retrieved"

if __name__ == "__main__":
    main()
