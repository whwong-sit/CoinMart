import os
import threading
from selenium import webdriver
import coinmart
from coinmart import app


def before_all(context):
    context.server = coinmart.coinmart
    context.thread = threading.Thread(target=context.server.test_server)
    context.thread.start()  # start flask app server
    chromedriver = "C:/Users/Daniel/Documents/GitHub/CoinMart/features/chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    context.browser = webdriver.Chrome(chromedriver)
    context.server_address = "http://" + app.config['SERVER_NAME']
    context.home = context.server_address


def after_all(context):
    context.browser.get(context.server_address + "/shutdown") # shut down flask app server
    context.thread.join()
    context.browser.quit()

