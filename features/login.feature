Feature: Login Page

  Scenario: Login
    Given a user visits the site
    When a user visits the login page
    Then she should see the username field
    And she should see the password field
    And she should see the login button

  Scenario: Login Success
    Given a user visits the site
    When a user visits the login page
    And she logs in with username "admin" and password "default"
    Then she should see a message of login success

  Scenario: Register and Login Email Success
    When a user visits the register page
    And she signs up with username "jiminy" and email "jiminy@cricket.com" and password "123456aA" and confirm password with "123456aA"
    Then she should see a message confirming successful registration
    When a user visits the login page
    And she logs in with username "jiminy@cricket.com" and password "123456aA"
    Then she should see a message of login success

  Scenario: Login User not found
    Given a user visits the site
    And she is logged out
    When a user visits the login page
    And she logs in with username "baduser" and password "badpasswd"
    Then she should see a message of "user not registered"

  Scenario: Login Incorrect Login
    Given a user visits the site
    When a user visits the login page
    And she logs in with username "admin" and password "badpasswd"
    Then she should see a message of "user not registered"

  Scenario: Logout
     Given a user visits the login page
     When she logs in
     And she clicks on the Logout link
     Then she sees a message telling her she has logged out

