Feature: Product Catalog and Shopping Cart

  Background: Application is available
    Given the application is open

  Scenario: TC-01 View the product catalog
    When I view the product catalog
    Then the available products should be visible

  Scenario: TC-02 Add a backpack to the cart
    When I add the backpack to the cart
    Then the backpack should be in the cart
