# Created by stn at 2017/5/29
Feature: Create_new_watchlist page

  Scenario: Login Success
    Given a user visits the site
    When a user visits the login page
    And she logs in with username "admin" and password "default"
    Then she should see a message of login success

  Scenario: enter create watchlist page
    When she logs in and clicks My Lists
    Then she would see a add button and click it
    And she would enter the new watchlist page


  Scenario: create a new watchlist
    Given a user visits the new watchlist page
    And she should see the title of New Watchlist
    Then she should see the cryptocurrency
    And she should see the Currency
    And she choose to add bitcoin and EUR as a new watchlist
    Then she returns to the dashboard and see New watchlist added

  Scenario: add new watchlist and should be add into the table
    When a user visits the new watchlist page
    Then she choose to add ripple and EUR as a new watchlist
    Then she returns to the dashboard and see New watchlist added
    And she would see the information at bottom of the table

  Scenario: Logout
     Given a user visits the login page
     When she logs in
     And she clicks on the Logout link
     Then she sees a message telling her she has logged out


