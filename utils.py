import requests
import urllib3
from selenium import webdriver
from retrying import retry
from faker import Faker
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class ChromeDriver:
    def driver(self):
        driver = webdriver.Chrome(executable_path="E:\CentBrowser\CentBrowser\Application\chromedriver.exe")
        return driver

class OpenBrowser(object):
    def __init__(self):
        self.driver = ChromeDriver().driver()

    def webOpen(self, url):
        self.driver.get(url)

    def webClose(self):
        self.driver.quit()

    def getHtml(self):
        return self.driver.page_source

class Common(object):
    @retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is False, wait_fixed=1000)
    def post_(self, url, **kwargs):
        try:
            kwargs.setdefault('timeout', 10)
            kwargs.setdefault('verify', False)
            kwargs.setdefault('headers', {'User-Agent': Faker().user_agent()})
            kwargs.setdefault('allow_redirects', False)
            kwargs.setdefault('params', {})
            kwargs.setdefault('proxies', {"http": None, "https": None})
            response = requests.post(url, **kwargs)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                return response.json()
        except requests.ConnectionError:
            return

    @retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is False, wait_fixed=1000)
    def get_(self, url, **kwargs):
        try:
            kwargs.setdefault('timeout', 10)
            kwargs.setdefault('verify', False)
            kwargs.setdefault('headers', {'User-Agent': Faker().user_agent()})
            kwargs.setdefault('allow_redirects', False)
            kwargs.setdefault('proxies', {"http": None, "https": None})
            response = requests.get(url, **kwargs)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                return response.text
        except requests.ConnectionError:
            return


