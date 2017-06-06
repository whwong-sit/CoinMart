# Created by Hema at 5/19/2017
Feature: Dashboard Page

  Scenario: No Watchlists Initially
    Given a user visits the site
    Then she should see Coin mart
    Then she should not see any watchlists

  Scenario: See Watchlists
    Given a user visits the site
    When a user visits the login page
    And she logs in with username "admin" and password "default"
    Then she should see the her list of watchlists
