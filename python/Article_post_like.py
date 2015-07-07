from browsermobproxy import Server
import time
from pprint import pprint
import json
import kemster_util as ku


server = Server("./selenium/browsermob-proxy-2.1.0-beta-1/bin/browsermob-proxy")
#server = Server("./selenium/browsermob-proxy-2.0-beta-6/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy()

print proxy.port

from selenium import webdriver
profile  = webdriver.FirefoxProfile()
chrome = webdriver.chrome.options
profile.set_proxy(proxy.selenium_proxy())
driver = webdriver.Firefox(firefox_profile=profile)

proxy.new_har("beamly GA test 1")
driver.get("https://uk.beamly.com/tv-news/7-reasons-need-chloe-mad-fat-diary-best-friend/")

test_scenario = json.load(open('./scenario1_test.json'))

for t in test_scenario['tests']:
    if t['test_type'] == 'xpath':
        print 'Running test {0}'.format(t['name'])
        element = driver.find_element_by_xpath(t['xpath'])
        for i in xrange(0,2):
            element.click()
            time.sleep(t['sleep_time'])
            
feed = driver.find_element_by_class_name('more-top-stories')
hearts = feed.find_elements_by_class_name('icon-open-heart')

for h in hearts:
    if h.is_displayed():
        y = h.location['y']
        driver.execute_script("window.scrollTo(0, {0});".format(y))
        time.sleep(2)
        for i in xrange(0,2):
            h.click()
            time.sleep(2)
        break 
        

    #if t['test_type'] == 'class':
        # print 'Running test {0}'.format(t['name'])
        # element = driver.find_element_by_class_name(t['class'])
        # element.click()
        # time.sleep(t['sleep_time'])  

resp = proxy.har # returns a HAR JSON blob
proxy.close()
server.stop()
driver.quit()

parsed_har = ku.parse_har_file(resp, 'google-analytics')
pprint(parsed_har)
json.dump(parsed_har, open('scenario1_test2.json', 'w+'))
