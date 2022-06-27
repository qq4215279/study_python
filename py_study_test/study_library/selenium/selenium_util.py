# encoding: utf-8

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from selenium.webdriver import ChromeOptions
import time
import json


def getBrowser(path):
    s = Service(executable_path=path)
    options = ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # browser = webdriver.Chrome(executable_path=path, chrome_options=options)
    browser = webdriver.Chrome(service=s, options=options)