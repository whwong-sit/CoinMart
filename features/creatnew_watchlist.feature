# Created by stn at 2017/5/29
Feature: Create_new_watchlist page and some pair objects into this watch list

  Scenario: Login Success
    Given a user visits the site
    When a user visits the login page
    And she logs in with username "admin" and password "default"
    Then she should see a message of login success

  Scenario:  create watchlist page
    When she logs in and clicks My Lists
    Then she would see a add button and click it
    And she would see "Enter a watchlist name"
    And she create a new watch list namely "admin"
    Then she should see a message of add watch list Success!

  Scenario: see the watchlist's ("admin") table
    Given a user visits the new watchlist page
    And she should see the title of "admin"
    Then she should see the cryptocurrency
    And she should see the Currency
    And she choose to add bitcoin and EUR as a new watchlist
    Then she returns to the dashboard and New pair added

  Scenario: add new watchlist and should be add into the table
    Then she choose to add ripple and EUR as a new watchlist
    Then she returns to the dashboard and New pair added
    And she would see the information at bottom of the table




