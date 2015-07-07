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


driver.execute_script("window.scrollTo(0, 500);")
  
resp = proxy.har # returns a HAR JSON blob
proxy.close()
server.stop()
driver.quit()


parsed_har = ku.parse_har_file(resp, 'google-analytics')
print resp

json.dump(parsed_har, open('scenario1_test1.json', 'w+'))
print parsed_har