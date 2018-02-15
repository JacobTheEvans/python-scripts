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


#Download Tweets from a user profile
def download_tweets(screen_name,number_of_tweets,max_id=None):
    api_url  = "%s/statuses/user_timeline.json?" % base_twitter_url
    api_url += "screen_name=%s&" % screen_name
    api_url += "count=%d" % number_of_tweets

    #If max_id is present attach it to request
    if max_id is not None:
        api_url += "&max_id=%d" % max_id

    print("[+] Requested API URL: %s" % api_url)

    #send request to twitter
    response = requests.get(api_url,auth=oauth)

    if response.status_code == 200:
        tweets = json.loads(response.content)
        return tweets
    else:
        print "[-] Request Failed"
        return None


#Download a users twitter history
def download_all_tweets(screen_name):
    full_tweet_list = []
    max_id = 0

    #grab first 200 tweets
    tweet_list = download_tweets(screen_name,200)

    #grab the oldest Tweet
    oldest_tweet = tweet_list[::-1][0]

    while max_id != oldest_tweet["id"]:
        full_tweet_list.extend(tweet_list)

        #set max_id to latest max_id we retrieved
        max_id = oldest_tweet["id"]

        print "[*] Retrieved: %d Tweets (max_id: %d)" % (len(full_tweet_list),max_id)

        #sleep to handle rate limiting
        time.sleep(3)

        #send next request with max_id set
        tweet_list = download_tweets(screen_name,200,max_id-1)

        #grab the oldest tweet
        if len(tweet_list):
            oldest_tweet = tweet_list[-1]

    #add the last few Tweets
    full_tweet_list.extend(tweet_list)

    #return full tweet list
    return full_tweet_list

def main():
    print("[+] Starting Python Tweet Download Bot")
    screen_name = ""
    while screen_name == "":
        print("[*] Input screen name of user")
        screen_name = raw_input(">> ")
    print(screen_name)
    full_tweet_list = download_all_tweets(screen_name)
    data = json.dumps(full_tweet_list)
    f = open(screen_name + "_data.json","w")
    f.write(data)
    f.close()
    print "[+] Data has been written"

if __name__ == "__main__":
    main()
