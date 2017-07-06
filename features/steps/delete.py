from behave import given, when, then, use_step_matcher, Given, When
from hamcrest import assert_that, equal_to
import re
from login_utils import *
import time
from behave import *

then
@given(u'a user visits the watchlist page')
def watchlist_site(context):
    pass

@then(u'she would see a delete button')
def visit_login(context):
    delete_btn_found = re.search("delete", context.browser.page_source, re.IGNORECASE)
    assert delete_btn_found

@when(u'she would see delete bottom behind admin link and clicks delete')
def delete_admin(context):
    context.browser.get(context.server_address + "/deletewatchlist?name=delete_admin")

@then(u'she would see delete success')
def delete_success(context):
    delete_found = re.search("delete Success!", context.browser.page_source, re.IGNORECASE)
    assert delete_found

@then(u'she would see delete watch list Success!')
def delete_watchlist_Success(context):
    delete_found = re.search("delete watch list Success!", context.browser.page_source, re.IGNORECASE)
    assert delete_found