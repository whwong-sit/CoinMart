# Created by stn at 2017/5/29
Feature: delete a pair of currency in watchlist "admin" and delete watchlist namely admin

  Scenario: Logout
     Given a user visits the login page
     When she logs in
     And she clicks on the Logout link
     Then she sees a message telling her she has logged out