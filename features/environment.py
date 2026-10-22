
import logging
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from appium.webdriver.common.appiumby import AppiumBy
from behave.model import Status
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    WebDriverException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from features.pages.catalog_page import CatalogPage
from features.support.config import AppiumSettings
from features.support.driver_factory import create_android_driver


LOGGER = logging.getLogger(__name__)


def before_scenario(context, scenario):
    context.driver = None
    context.scenario_name = scenario.name

    try:
        settings = AppiumSettings.from_environment()
        context.settings = settings
        _reset_app_data(settings)

        context.driver = create_android_driver(settings)
        context.catalog_page = CatalogPage(
            context.driver,
            settings.wait_timeout,
            settings.app_package,
        )

        _wait_for_app_startup(
            context.driver,
            context.catalog_page.catalog_title,
            settings.wait_timeout,
        )

        context.catalog_page.wait_until_loaded()
        LOGGER.info("Application started for %s", scenario.name)
    except Exception:
        _capture_diagnostics(context, scenario.name, "setup")
        _close_driver(context)
        raise


def _wait_for_app_startup(driver, catalog_locator, timeout):
    button_locator = (AppiumBy.ID, "android:id/button1")

    def startup_state(current_driver):
        if current_driver.find_elements(*button_locator):
            return "compatibility_dialog"
        if current_driver.find_elements(*catalog_locator):
            return "catalog"
        return False

    state = WebDriverWait(driver, timeout).until(startup_state)
    if state == "catalog":
        return

    def click_compatibility_button(current_driver):
        try:
            button = current_driver.find_element(*button_locator)
            if button.is_displayed() and button.is_enabled():
                button.click()
                return True
        except (NoSuchElementException, StaleElementReferenceException):
            if current_driver.find_elements(*catalog_locator):
                return True
        return False

    WebDriverWait(driver, timeout).until(click_compatibility_button)
    LOGGER.info("Dismissed the compatibility warning")


def _reset_app_data(settings):
    try:
        result = subprocess.run(
            [
                settings.adb_path,
                "-s",
                settings.udid,
                "shell",
                "pm",
                "clear",
                settings.app_package,
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=settings.adb_exec_timeout / 1000,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise RuntimeError(f"Could not run ADB: {error}") from error

    if result.returncode != 0 or "Success" not in result.stdout:
        details = " ".join(
            value.strip() for value in (result.stdout, result.stderr) if value
        )
        raise RuntimeError(f"Could not clear app data: {details}")


def after_step(context, step):
    if step.status in (Status.failed, Status.error):
        _capture_diagnostics(
            context,
            getattr(context, "scenario_name", "scenario"),
            step.name,
        )


def after_scenario(context, scenario):
    _close_driver(context)


def _close_driver(context):
    driver = getattr(context, "driver", None)
    if driver is None:
        return

    try:
        driver.quit()
    except Exception:
        LOGGER.exception("Could not close the Appium session")
    finally:
        context.driver = None


def _capture_diagnostics(context, scenario_name, step_name):
    try:
        driver = getattr(context, "driver", None)
        if driver is None:
            return

        scenario_slug = re.sub(r"[^A-Za-z0-9_-]+", "_", scenario_name).strip("_")
        step_slug = re.sub(r"[^A-Za-z0-9_-]+", "_", step_name).strip("_")
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        artifact_dir = Path("artifacts")
        artifact_dir.mkdir(parents=True, exist_ok=True)
        artifact_name = f"{timestamp}_{scenario_slug}_{step_slug}"

        try:
            saved = driver.save_screenshot(
                str(artifact_dir / f"{artifact_name}.png")
            )
            if saved:
                LOGGER.info("Failure screenshot saved: %s", artifact_name)
            else:
                LOGGER.warning("Appium did not save the screenshot: %s", artifact_name)
        except Exception:
            LOGGER.exception("Could not save the failure screenshot")

        try:
            (artifact_dir / f"{artifact_name}.xml").write_text(
                driver.page_source,
                encoding="utf-8",
            )
            LOGGER.info("Failure XML hierarchy saved: %s", artifact_name)
        except Exception:
            LOGGER.exception("Could not save the failure XML hierarchy")
    except Exception:
        LOGGER.exception("Could not save failure artifacts")

