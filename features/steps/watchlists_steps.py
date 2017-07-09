# coding=utf-8
from behave import given, when, then, use_step_matcher
from hamcrest import assert_that, equal_to
import re
from login_utils import *
from behave import *


@then(u'she should not see any watchlists')
def see_no_watchlists(context):
    context.browser.get(context.server_address + "/")
    watchlist_found = re.search("Cryptocurrency :", context.browser.page_source, re.IGNORECASE)
    if watchlist_found == '':
        pass


@then(u'she should see the her list of watchlists')
def see_watchlists(context):
    context.browser.get(context.server_address + "/")
    watchlist_found = re.search("My lists", context.browser.page_source, re.IGNORECASE)
    assert watchlist_found
