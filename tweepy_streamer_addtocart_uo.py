import time
from tweepy import StreamListener
from tweepy import Stream
import tweepy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

acceptablesizes = ['<span class="ng-binding">11.5</span>', '<span class="ng-binding">12</span>', '<span class="ng-binding">11</span>','<span class="ng-binding">10.5</span>', '<span class="ng-binding">10</span>', '<span class="ng-binding">6</span>']
#URL FOR URBANOUTFITTERS CATALOG, LIST OF 7 SIZES THAT ARE OK TO BUY IN ORDER OF PREFERENCE

browser = webdriver.Firefox()
#defines the webdriver in use
action = webdriver.common.action_chains.ActionChains(browser)
"""calls webdriver.common.action_chains.ActionChains...
follow with .move_to_element(arg).click(arg).perform()"""

auth = tweepy.OAuthHandler("SMOe7ZDuvt7awpfcfuMmWVJl3", "RGNUdCYe4YHMMDVDbOF37v2vefsEq7x4ryUnw8rtlvDAi5ITdD")
auth.set_access_token("278285139-ChvAChDXSJe67L0p0s0Jj4ATCMdQCGy8HA9H0rQn", "396tmk41GyA1kQJ9v2kC1tOrrtnrZjSvzSMY6OsJ6jzfo")
api = tweepy.API(auth)
#authenticates tweepy with twitter api, defines api

vendorID = "786572559592468481" #INPUT #twitter id of vendor
vendor_tweepy_user = api.get_user(id = vendorID)
vendortwitterusername = vendor_tweepy_user.screen_name #username of twitter vendor for usage in webdriver
tweetIDtoWebDriver = 0 #initialized for use with findlink()

def findlink(twitterid,tweetIDtoWebDriver): #takes vendor id and tweet id, locates and clicks on hyperlink
    yeezytweet = "https://twitter.com/" + str(twitterid) + "/status/" + str(tweetIDtoWebDriver)
    browser.get(yeezytweet) #retrieves tweet detected to contain url
    shopbutton = browser.find_element_by_partial_link_text("/")
    yeezyurl = shopbutton.get_attribute("href")
    buy(yeezyurl)

'''
Function that checks if an item is added to the cart
'''

def buy(url):
    end = 7
    browser.get(url)
    addtocart = browser.find_element_by_css_selector('.bag-button')
    for x in acceptablesizes:                           #Loops to find acceptable sizes, in priority order
        for i in range(1, end):
            mainselector = "dd:nth-child(" + str(i) + ")"  #Sets the main selector as the i child
            try:
                sizeelement = browser.find_element_by_css_selector(mainselector) #Finds dd:nth-child
            except NoSuchElementException:
                print("Cannot Find nth-child(" + str(i) + ")") # Prints if the mainselector is not found
            try:
                sizeofhtmlvalue = str(sizeelement.get_attribute('outerHTML')) #copys outerHTML of the selector
            except NoSuchElementException:
                print("Cannot find outerHTML")
            if x in sizeofhtmlvalue:                        #Checks to see if the size plus span tag are in the outerHTML
                try:
                    action.move_to_element(sizeelement).click(sizeelement).perform()    #Selects size
                    action.move_to_element(addtocart).click(addtocart).perform()    #Adds to cart
                    added_to_cart_uo()          #Runs the cart check script
                    time.sleep(1.5)
                    if (added_to_cart == True):
                        exit()
                except NoSuchElementException:                                  #If the element is not found
                    print("Cannot add to cart")

added_to_cart = False           #Sets the added to cart value to false
ready = False                   #Sets

def added_to_cart_uo ():
    try:
        bag_select = browser.find_element_by_class_name("emptyCart")
        action.move_to_element(bag_select).click(bag_select).perform()
    except NoSuchElementException:
        print ("Cannot find cart element")

    try:
        bag_condition = browser.find_element_by_css_selector('p')
        bag_status = str(bag_condition.get_attribute('outerHTML'))
    except NoSuchElementException:
        print("Cannnot find outerHTML")

    if "<p>Your bag is currently empty<p>" in bag_status:
         added_to_cart = False
    else:
        added_to_cart = True

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