from behave import given, when, then

from features.pages.cart_page import CartPage


@given("the application is open")
def step_app_abierta(context):
    assert context.driver.current_package == context.settings.app_package, (
        "The application is not open"
    )


@when("I view the product catalog")
def step_consultar_catalogo(context):
    assert context.catalog_page.is_catalog_visible(), (
        "The Products title is not displayed"
    )


@then("the available products should be visible")
def step_ver_productos(context):
    assert context.catalog_page.is_backpack_visible(), (
        "The Sauce Labs Backpack product was not found"
    )


@when("I add the backpack to the cart")
def step_agregar_mochila(context):
    context.catalog_page.add_backpack_to_cart()


@then("the backpack should be in the cart")
def step_verificar_carrito(context):
    context.catalog_page.open_cart()
    context.cart_page = CartPage(
        context.driver,
        context.settings.wait_timeout,
        context.settings.app_package,
    )

    assert context.cart_page.is_backpack_visible(), (
        "The backpack does not appear in the cart"
    )

