##########project configurations#########
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from datetime import date, time
import requests
import random
# import logging as logger

today = date.today()
d1 = today.strftime("%d-%m-%Y")
# logger.basicConfig(filename=d1+"_logs.log", 
#                     format='%(asctime)s %(message)s', 
#                     filemode='w')

class ChromeDriver(object):
	"""docstring for Config"""
	def __init__(self):
		super(ChromeDriver, self).__init__()
		self.driver = None
		self.wait_attrib = None
		# self.logger = logger
		
	def drivers(self):
		proxy = Proxy()
		proxy.proxyType = ProxyType.MANUAL
		proxy.autodetect = False
		proxy.httpProxy = proxy.sslProxy = proxy.socksProxy = "http://61c6498052c94290892a400b3314cf78:@proxy.crawlera.com:8011/"

		capa = DesiredCapabilities.CHROME
		capa["pageLoadStrategy"] = "none"
		options = Options()
		# options.add_argument('--headless')

		options.add_argument('start-maximized')
		options.add_experimental_option("useAutomationExtension", False)
		options.add_experimental_option("excludeSwitches",["enable-automation"])
		options.Proxy = proxy
		self.driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options,desired_capabilities=capa)
		self.driver.maximize_window()

		return self.driver

	def wait(self):
		self.wait_attrib = WebDriverWait(self.driver, 20)
		return self.wait_attrib

	def wait_random(self):
		wait = WebDriverWait(self.driver, 10)
		slp = random.uniform(1.0, 3.0)
		wait_attrib = time.sleep(slp)
		return self.wait_attrib