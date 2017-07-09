from behave import given, when, then, use_step_matcher
from hamcrest import assert_that, equal_to
import re
from login_utils import *
from behave import *



@when(u'she logs in and clicks My Lists')
def see_add(context):
    my_lists = context.browser.find_element_by_id("My lists")
    my_lists.click()
    assert my_lists


@then(u'she would see a add button and click it')
def see(context):
    add_btn = context.browser.find_element_by_id('test')
    add_btn.click()
    assert add_btn

@then(u'she would see "Enter a watchlist name"')
def see_addwatchlist(context):
    new_found = re.search("Enter a watchlist name", context.browser.page_source, re.IGNORECASE)
    assert new_found

@then(u'she create a new watch list namely "{admin}"')
def create_addwatchlist(context,admin):
    uname = context.browser.find_element_by_name('watchlistname')
    login_button = context.browser.find_element_by_name('btn_confirm')
    uname.clear();
    uname.send_keys(admin)
    login_button.click()

@then(u'she should see a message of add watch list Success!')
def add_successful(context):
    msg_found = re.search("add watch list Success!", context.browser.page_source, re.IGNORECASE)
    assert msg_found

@given (u'a user visits the new watchlist page')
def add_page(context):
    list_found = context.browser.find_element_by_id("My lists")
    list_found.click()
    assert list_found


@given(u'she should see the title of "admin"')
def newWatchlist_found(context):
    admin_title_found = re.search("admin", context.browser.page_source, re.IGNORECASE)
    assert admin_title_found


@then(u'she should see the Cryptocurrency')
def currency_visit(context):
    context.browser.get(context.server_address + "/addpair?name=admin&id=22")
    cry_currency_found = re.search("Cryptocurrency", context.browser.page_source, re.IGNORECASE)
    assert cry_currency_found

@then(u'she should see the Currency')
def currency_visit(context):
    context.browser.get(context.server_address + "/addpair?name=admin&id=22")
    currency_found = re.search("Currency", context.browser.page_source, re.IGNORECASE)
    assert currency_found


@then(u'she choose to add bitcoin and EUR as a new watchlist')
def choose_currency(context):
    cryptocurrency = context.browser.find_element_by_id('0')
    cryptocurrency.click()
    choose_cryptocurrency = context.browser.find_element_by_id('bitcoin')
    choose_cryptocurrency.click()
    currency = context.browser.find_element_by_id('1')
    currency.click()
    choose_currency = context.browser.find_element_by_id('EUR')
    choose_currency.click()
    confirm_button = context.browser.find_element_by_id('add')
    confirm_button.click()

@then(u'she choose to add ripple and EUR as a new watchlist')
def choose_currency(context):
    cryptocurrency = context.browser.find_element_by_id('0')
    cryptocurrency.click()
    choose_cryptocurrency = context.browser.find_element_by_id('ripple')
    choose_cryptocurrency.click()
    currency = context.browser.find_element_by_id('1')
    currency.click()
    choose_currency = context.browser.find_element_by_id('EUR')
    choose_currency.click()
    confirm_button = context.browser.find_element_by_id('add')
    confirm_button.click()

@then(u'she returns to the dashboard and New pair added')
def seenew_watchlist(context):
    currency_found = re.search("New pair added", context.browser.page_source, re.IGNORECASE)
    assert currency_found

@then(u'she would see the information at bottom of the table')
def seenew_watchlist(context):
    currency_found = re.search("ripple", context.browser.page_source, re.IGNORECASE)
    assert currency_found
