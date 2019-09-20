from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
from func import *
import selenium
import telebot 
import requests
import json
import time


options = webdriver.ChromeOptions()
options.add_argument('headless')

driver = webdriver.Chrome('chromedriver.exe',options = options)

links_to_check_line = {}

def func():
	try:
		time.sleep(1)
		get_all_url_line(get_html('https://1xstavka.ru/live/Handball/'),links_to_check_line,driver)
		get_all_url_live(get_html('https://1xstavka.ru/line/Handball/'),links_to_check_line,driver)
	except Exception as e:
		print(e,0)
		func()
while True:
	func()





