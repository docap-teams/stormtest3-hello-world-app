Feature: micro service

  Scenario: Hello world!
    Given micro is setup
     When we call the api without a parameter
     Then micro will present Hello World!

  Scenario Outline: Hello name
    Given micro is setup
    When we call the api with parameter "<name>"
    Then micro will present Hello "<name>"

  Examples: users
    | name  |
    | Roy   |
    | Simon |
    | Eddie |
