from appium.webdriver.common.appiumby import AppiumBy

from features.pages.base_page import BasePage


class CartPage(BasePage):
    BACKPACK_NAME = "Sauce Labs Backpack"

    def __init__(self, driver, timeout, app_package):
        super().__init__(driver, timeout)
        self.backpack_item = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            "new UiSelector()"
            f'.resourceId("{app_package}:id/titleTV")'
            f'.text("{self.BACKPACK_NAME}")',
        )

    def is_backpack_visible(self):
        return self.is_visible(self.backpack_item)
