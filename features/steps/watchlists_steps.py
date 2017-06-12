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


@then(u'she should see her list of watchlists')
def see_watchlists(context):
    context.browser.get(context.server_address + "/")
    watchlist_found = re.search("My lists", context.browser.page_source, re.IGNORECASE)
    assert watchlist_found

@then(u'she should see her list of watchlists with current value')
def see_watchlists_current_value(context):
    context.browser.get(context.server_address + "/")
    currentvalue_found = re.search("Current Value :", context.browser.page_source, re.IGNORECASE)
    assert currentvalue_found

@then(u'she should see her list of watchlists with historical value')
def see_watchlists_historical_value(context):
    context.browser.get(context.server_address + "/")
    historicalvalue_found = re.search("Historical Value :", context.browser.page_source, re.IGNORECASE)
    assert historicalvalue_found
