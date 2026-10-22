from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver, timeout):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def wait_for_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def is_visible(self, locator):
        try:
            self.wait_for_visible(locator)
            return True
        except TimeoutException:
            return False
