from behave import given, when, then, use_step_matcher, Given, When
from hamcrest import assert_that, equal_to
import re
from login_utils import *
import time


@then(u'she would see a button namely bitcoin EUR and click it')
def visit_login(context):
    delete = context.browser.find_element_by_id('delete_bitcoin_EUR')
    delete.click()


@then(u'she would delete success')
def see_username_field(context):
    delete_found = re.search("delete Success!", context.browser.page_source, re.IGNORECASE)
    assert delete_found