from behave import given, when, then, use_step_matcher, Given, When
from hamcrest import assert_that, equal_to
import re
from login_utils import *
import time


@when(u'a user visits the login page')
def visit_login(context):
    context.browser.get(context.server_address + "/login")


@then(u'she should see the username field')
def see_username_field(context):
    flaskr_found = re.search("Enter a Username or Email", context.browser.page_source, re.IGNORECASE)
    assert flaskr_found


@then(u'she should see the password field')
def see_password_field(context):
    flaskr_found = re.search("Enter a Password", context.browser.page_source, re.IGNORECASE)
    assert flaskr_found


@then(u'she should see the login button')
def see_login_button(context):
    flaskr_found = re.search("Login", context.browser.page_source, re.IGNORECASE)
    assert flaskr_found


@when(u'she logs in with username "{username}" and password "{password}"')
def login(context, username, password):
    context.browser.get(context.server_address + "/login")
    uname = context.browser.find_element_by_name('username')
    passwd = context.browser.find_element_by_name('password')
    login_button = context.browser.find_element_by_name('btn_login')
    uname.clear();
    passwd.clear();
    uname.send_keys(username)
    passwd.send_keys(password)
    login_button.click()


@then(u'she should see a message of login success')
def see_login_success(context):
    flaskr_found = re.search("Login Success!", context.browser.page_source, re.IGNORECASE)
    assert flaskr_found


@then(u'she should see a message of "user not registered"')
def see_login_failure_not_registered(context):
    flaskr_found = re.search("User not registered", context.browser.page_source, re.IGNORECASE)
    assert flaskr_found

@then(u'she should see a message of "Incorrect username or password"')
def see_login_failure(context):
    flaskr_found = re.search("Incorrect username or password", context.browser.page_source, re.IGNORECASE)
    assert flaskr_found

@given(u'a user visits the login page')
def login_page(context):
    context.browser.get(context.server_address + "/login")


@given(u'she sees the Logout link')
def see_logout_link(context):
    flaskr_found = re.search("Log out", context.browser.page_source, re.IGNORECASE)
    assert flaskr_found


@when(u'she clicks on the Logout link')
def click_logout_link(context):
    logout_found = context.browser.find_element_by_link_text("log out")
    logout_found.click()


@then(u'she returns to the site')
def visit_site(context):
    pass


@then(u'she sees a message telling her she has logged out')
def see_logout_success(context):
    flaskr_found = re.search("You were logged out", context.browser.page_source, re.IGNORECASE)
    assert flaskr_found


@given(u'she is logged out')
def click_logout_link(context):
    logout_found = context.browser.find_element_by_link_text("log out")
    if logout_found:
        logout_found.click()
    pass
