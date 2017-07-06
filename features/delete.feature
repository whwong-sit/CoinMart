# Created by stn at 2017/5/29
Feature: Delete a watchlist

  Scenario: delete watchlist namely admin
    When she logs in and clicks My Lists
    And she would see delete bottom behind admin link and clicks delete
    Then she would see delete watch list Success!

  Scenario: Logout
     Given a user visits the login page
     When she logs in
     And she clicks on the Logout link
     Then she sees a message telling her she has logged out