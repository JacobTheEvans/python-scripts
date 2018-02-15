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

#Main Twitter API function for sending requests
def send_request(screen_name,relationship_type,next_cursor=None):
    url = "https://api.twitter.com/1.1/%s/ids,json?screen_name=%s&count=5000" % (relationship_type,screen_name)

    if next_cursor is not None:
        url += "&cursor=%s" % next_cursor

    response = requests.get(url,auth=oauth)

    time.sleep(3)

    if response.status_code == 200:
        result = json.loads(response.content)
        return result

    return None

def get_all_friends_or_followers(screen_name,relationship_type):
    account_list = []
    next_cursor = None

    #send off first request
    accounts = send_request(screen_name, relationship_type)

    #valid user account so start pulling relationships
    if accounts is not None:
        account_list.extend(accounts["ids"])

        print "[*] Downloaded %d of type %s" % (len(account_list),relationship_type)

        #while we have a cursor keep downloading friends and followers
        while accounts["next_cursor"] != 0 and accounts["next_cursor"] != -1:
            accounts = send_request(screen_name,relationship_type,accounts["next_cursor"])

            if accounts is not None:
                account_list.extend(accounts["ids"])
                print "[*] Downloaded %d of type %s" % (len(account_list),relationship_type)
            else:
                break

        return account_list

def main():
    print "[+] Friends and Followers Twitter Download Bot"
    screen_name = ""
    while screen_name == "":
        print "[*] Input user screen name"
        screen_name = raw_input(">> ")

    friends = get_all_friends_or_followers(screen_name,"friends")
    followers = get_all_friends_or_followers(screen_name, "followers")

    print "[**] Retrieved %d friends" % len(friends)
    print "[**] Retrieved %d followers" % len(followers)

    #Download files in json format

if __name__ == "__main__":
    main()
