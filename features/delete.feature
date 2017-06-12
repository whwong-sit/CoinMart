# Created by stn at 2017/5/29
Feature: delete a pair of currency in watchlist "admin" and delete watchlist namely admin


  Scenario: delete watchlist pair in watchlist admin(bitcoin with EUR)
    Given a user visits the watchlist site
    Then she would see a button namely bitcoin EUR and click it
    And she would see delete success

  Scenario: delete watchlist namely admin
    When she logs in and clicks My Lists
    And she would see delete bottom behind admin link and clicks delete
    Then she would see delete watch list Success!

  Scenario: Logout
     Given a user visits the login page
     When she logs in
     And she clicks on the Logout link
     Then she sees a message telling her she has logged out