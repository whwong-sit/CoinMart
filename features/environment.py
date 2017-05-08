import threading
#from wsgiref import simple_server
from selenium import webdriver
import flaskr
from flaskr import app


def before_all(context):
    context.server = flaskr.flaskr
    context.thread = threading.Thread(target=context.server.test_server)
    context.thread.start()  # start flask app server
    context.browser = webdriver.Chrome()
    context.server_address = "http://" + app.config['SERVER_NAME']
    context.home = context.server_address



def after_all(context):
    context.browser.get(context.server_address + "/shutdown") # shut down flask app server
    context.thread.join()
    context.browser.quit()

