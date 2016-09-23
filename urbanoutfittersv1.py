#URBAN OUTFITTERS SNEAKERBOT V0.1

#item_id = input("ITEM ID? ")
#ASKS FOR ITEM ID (AS STRING)

item_id = "34765339"
url = 'http://www.urbanoutfitters.com/urban/catalog/productdetail.jsp?id='
acceptablesizes = ["11","12","10","13","9","7","6"]
#URL FOR URBANOUTFITTERS CATALOG, LIST OF 7 SIZES THAT ARE OK TO BUY IN ORDER OF PREFERENCE

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Firefox()
#defines the webdriver in use
action = webdriver.common.action_chains.ActionChains(browser)
"""calls webdriver.common.action_chains.ActionChains...
follow with .move_to_element(arg).click(arg).perform()"""
browser.get(url+item_id)
#gets product webpage, composed of constant for URBAN OUTFITTERS and input id

"""WAIT PERIOD"""

addtocart = browser.find_element_by_css_selector('.bag-button')
preferred_size = 0
repeater = True
rangecap = 7
while repeater == True:
    try:
        for i in acceptablesizes:
            for x in range(1,rangecap):
                sizeindex = "dd:nth-child("+str(x)+")"
                selected_size = browser.find_element_by_css_selector(sizeindex)
                sizeohtmlvalue = str(selected_size.get_attribute('outerHTML'))
                if i in sizeohtmlvalue:
                    action.move_to_element(selected_size).click(selected_size).perform()
                    action.move_to_element(addtocart).click(addtocart).perform()
                    print("yuh! size "+i+" added to cart... or at least attempted")
                    repeater = False
                    break
    except NoSuchElementException:
        rangecap = x
        print("end of viable sizes.  rangecap =",rangecap)
