# Created by stn at 2017/5/29
Feature: delete page

  Scenario: Login Success
    Given a user visits the site
    When a user visits the login page
    And she logs in with username "admin" and password "default"
    Then she should see a message of login success

  Scenario: delete watchlist(bitcoin with EUR)
    When she logs in and clicks My Lists
    Then she would see a button namely bitcoin EUR and click it
    And she would delete success

  Scenario: Logout
     Given a user visits the login page
     When she logs in
     And she clicks on the Logout link
     Then she sees a message telling her she has logged out