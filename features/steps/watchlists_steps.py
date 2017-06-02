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
    cryptocurrency_found = re.search("Cryptocurrency :", context.browser.page_source, re.IGNORECASE)
    currency_found = re.search("Currency :", context.browser.page_source, re.IGNORECASE)
    value_found = re.search("Value :", context.browser.page_source, re.IGNORECASE)
    time_stamp_found = re.search("Timestamp :", context.browser.page_source, re.IGNORECASE)
    old_value_found = re.search("Last Value :", context.browser.page_source, re.IGNORECASE)
    old_time_stamp_found = re.search("Last Timestamp :", context.browser.page_source, re.IGNORECASE)
    watchlist_found = (cryptocurrency_found and currency_found and value_found and time_stamp_found and old_value_found and old_time_stamp_found)
    assert watchlist_found
