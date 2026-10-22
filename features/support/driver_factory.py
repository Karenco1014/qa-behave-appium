from appium import webdriver
from appium.options.android import UiAutomator2Options


def create_android_driver(settings):
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = settings.device_name
    options.udid = settings.udid
    options.app_package = settings.app_package
    options.app_activity = settings.app_activity
    options.no_reset = True
    options.set_capability("appium:adbExecTimeout", settings.adb_exec_timeout)

    return webdriver.Remote(
        command_executor=settings.server_url,
        options=options,
    )
