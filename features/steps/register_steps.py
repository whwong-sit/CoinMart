from behave import given, when, then, use_step_matcher, Given, When
from hamcrest import assert_that, equal_to
import re
from login_utils import *
import time



@when(u'a user visits the register page')
def visit_register(context):
    context.browser.get(context.server_address + "/register")
    time.sleep(1)


@then(u'she should see the confirm password field')
def see_passwordConfirm_field(context):
    flaskr_found = re.search("Confirm your Password", context.browser.page_source, re.IGNORECASE)
    assert flaskr_found


@then(u'she should see the register button')
def see_register_button(context):
    flaskr_found = re.search("Register", context.browser.page_source, re.IGNORECASE)
    assert flaskr_found


@when(u'she signs up with username "{username}" and email "{email}" and password "{password}" and confirm password with "{password1}"')
def register(context, username, email, password, password1):
    context.browser.get(context.server_address + "/register")
    uname = context.browser.find_element_by_name('username')
    email0= context.browser.find_element_by_name('email')
    passwd = context.browser.find_element_by_name('password')
    passwd1 = context.browser.find_element_by_name('cfm_password')
    login_button = context.browser.find_element_by_name('btn_register')
    uname.clear();
    email0.clear();
    passwd.clear();
    passwd1.clear();
    uname.send_keys(username)
    email0.send_keys(email)
    time.sleep(0.6)
    passwd.send_keys(password)
    passwd1.send_keys(password1)
    time.sleep(1)
    login_button.click()


@then(u'she should see a message of "Passwords do not match"')
def see_register_failure4(context):
    time.sleep(0.4)
    flaskr_found = re.search("Passwords do not match", context.browser.page_source, re.IGNORECASE)
    assert flaskr_found


@then(u'she should see a message of Username or password invalid')
def see_register_failure3(context):
    time.sleep(0.4)
    flaskr_found = re.search("Invalid password. Passwords must contain at least 8 characters, and at least one capital letter and number", context.browser.page_source, re.IGNORECASE)
    assert flaskr_found


@then(u'she should see a message of "User already registered"')
def see_register_failure1(context):
    time.sleep(0.4)
    flaskr_found = re.search("User already registered", context.browser.page_source, re.IGNORECASE)
    assert flaskr_found


@then(u'she should see a message confirming successful registration')
def see_register_success(context):
    time.sleep(0.4)
    flaskr_found = re.search("You were successfully registered and have been logged in", context.browser.page_source, re.IGNORECASE)
    assert flaskr_found


@When(u'she clicks on the Register link')
def register_page(context):
    register_found = context.browser.find_element_by_link_text("Sign up")
    register_found.click()

@then(u'she turns to register page')
def register_page(context):
    pass
