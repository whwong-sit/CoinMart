from behave import given, when, then, use_step_matcher
from hamcrest import assert_that, equal_to
import re
from login_utils import *
from behave import *

@given(u'a user visits the site')
def visit(context):
    context.browser.get(context.home)


@then(u'she should see Coin Mart')
def see(context):
    flaskr_found = re.search("Coin Mart", context.browser.page_source, re.IGNORECASE)
    assert flaskr_found


@given(u'she is not logged in')
def is_not_logged_in(context):
    # can't really test this except if one sees the Login link
    pass

@then(u'she should see the Login link')
def see_login(context):
    login_found = re.search("log in", context.browser.page_source, re.IGNORECASE)
    assert login_found


@when(u'she logs in')
def logs_in(context):
    login(context)

@when(u'she returns to the site')
def return_visit(context):
    context.browser.get(context.home)


@then(u'she should see the Logout link')
def step_impl(context):
    logout_found = re.search("log out", context.browser.page_source, re.IGNORECASE)
    assert logout_found


@then(u'she should see the Register link')
def step_impl(context):
    signup_found = re.search("sign up", context.browser.page_source, re.IGNORECASE)
    assert signup_found
