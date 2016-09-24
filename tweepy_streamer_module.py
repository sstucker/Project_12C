
from tweepy import StreamListener
from tweepy import Stream
import tweepy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Firefox()
#defines the webdriver in use
action = webdriver.common.action_chains.ActionChains(browser)
"""calls webdriver.common.action_chains.ActionChains...
follow with .move_to_element(arg).click(arg).perform()"""

auth = tweepy.OAuthHandler("SMOe7ZDuvt7awpfcfuMmWVJl3", "RGNUdCYe4YHMMDVDbOF37v2vefsEq7x4ryUnw8rtlvDAi5ITdD")
auth.set_access_token("278285139-ChvAChDXSJe67L0p0s0Jj4ATCMdQCGy8HA9H0rQn", "396tmk41GyA1kQJ9v2kC1tOrrtnrZjSvzSMY6OsJ6jzfo")
api = tweepy.API(auth)
#authenticates tweepy with twitter api, defines api

vendorID = "278285139" #INPUT #twitter id of vendor
vendor_tweepy_user = api.get_user(id = vendorID)
vendortwitterusername = vendor_tweepy_user.screen_name #username of twitter vendor for usage in webdriver
tweetIDtoWebDriver = 0 #initialized for use with findlink()

def findlink(twitterid,tweetIDtoWebDriver): #takes vendor id and tweet id, locates and clicks on hyperlink
    yeezytweet = "https://twitter.com/" + str(twitterid) + "/status/" + str(tweetIDtoWebDriver)
    browser.get(yeezytweet) #retrieves tweet detected to contain url
    shopbutton = browser.find_element_by_partial_link_text("/")
    action.move_to_element(shopbutton).click(shopbutton).perform()

class YeezyListener(StreamListener):
    def on_status(self, status):
        print("STATUS FROM",vendorID,"READS: ",status.text)
        if "RT @" not in status.text:
            if "https://t.co" in status.text:
                tweetIDtoWebDriver = status.id
                print(tweetIDtoWebDriver)
                findlink(vendortwitterusername,tweetIDtoWebDriver)
    def on_error(self, status):
        print(status)
    def on_connect(self):
        print("CONNECTED TO",vendorID)

if __name__ == '__main__':
    listener = YeezyListener()
    yeezystream = Stream(auth, listener)
    yeezystream.filter(follow=[vendorID])
    tweet.yeezystream
