from selenium import webdriver
from selenium import *
from selenium.webdriver.common.by import By
import datetime

def test_func (url):
    browser = webdriver.Firefox()       #Sets the webdriver function equal to browser
    browser.get(url)      #Pulls the webaddress
    action = webdriver.common.action_chains.ActionChains(browser) #Sets the action chain as a simple variable action

    test = browser.find_element_by_link_text('HERE')    #Sets the element with ID HERE to test

    print(test)     #Prints element ID

    browser.implicitly_wait(5)      #Waits for page to load

    print ("Clicking HERE")

    action.move_to_element(test).click(test).perform() #Perfoms action click on test

test_func("http://www.seleniumhq.org")
