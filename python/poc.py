from browsermobproxy import Server
import time
from pprint import pprint
import json



server = Server("./selenium/browsermob-proxy-2.1.0-beta-1/bin/browsermob-proxy")
#server = Server("./selenium/browsermob-proxy-2.0-beta-6/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy()

print proxy.port


from selenium import webdriver
profile  = webdriver.FirefoxProfile()
profile.set_proxy(proxy.selenium_proxy())
driver = webdriver.Firefox(firefox_profile=profile)

proxy.new_har("beamly GA test 1")
driver.get("https://uk.beamly.com/tv-news/7-reasons-need-chloe-mad-fat-diary-best-friend/")
#driver.find_element_by_id('r0ffsz')
votely_head = driver.find_element_by_xpath('//*[@id="votely-45a015df-cebf-4d61-a625-f079a3bbd445"]/div[2]/div[1]/div[2]/div[2]/div/div[3]/div')

for i in xrange(0,65):
    votely_head.click()

time.sleep(5)    
for i in xrange(0,10):
    votely_head.click()
    
resp = proxy.har # returns a HAR JSON blob
proxy.close()
server.stop()
driver.quit()
