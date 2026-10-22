from appium.webdriver.common.appiumby import AppiumBy

from features.pages.base_page import BasePage


class CatalogPage(BasePage):
    BACKPACK_NAME = "Sauce Labs Backpack"

    def __init__(self, driver, timeout, app_package):
        super().__init__(driver, timeout)
        self.catalog_title = (
            AppiumBy.ID,
            f"{app_package}:id/productTV",
        )
        self.backpack_title = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            "new UiSelector()"
            f'.resourceId("{app_package}:id/titleTV")'
            f'.text("{self.BACKPACK_NAME}")',
        )
        self.backpack_image = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            "new UiSelector()"
            f'.resourceId("{app_package}:id/titleTV")'
            f'.text("{self.BACKPACK_NAME}")'
            f'.fromParent(new UiSelector().resourceId("{app_package}:id/productIV"))',
        )
        self.add_to_cart_button = (
            AppiumBy.ID,
            f"{app_package}:id/cartBt",
        )
        self.cart_button = (AppiumBy.ACCESSIBILITY_ID, "View cart")

    def wait_until_loaded(self):
        self.wait_for_visible(self.catalog_title)

    def is_catalog_visible(self):
        return self.is_visible(self.catalog_title)

    def is_backpack_visible(self):
        return self.is_visible(self.backpack_title)

    def add_backpack_to_cart(self):
        self.wait_for_clickable(self.backpack_image).click()
        self.wait_for_clickable(self.add_to_cart_button).click()

    def open_cart(self):
        self.wait_for_clickable(self.cart_button).click()
