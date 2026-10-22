import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppiumSettings:
    server_url: str
    udid: str
    device_name: str
    adb_path: str
    app_package: str
    app_activity: str
    wait_timeout: int
    adb_exec_timeout: int

    @classmethod
    def from_environment(cls):
        wait_timeout = int(os.getenv("APPIUM_WAIT_TIMEOUT", "30"))
        if wait_timeout < 1:
            raise ValueError("APPIUM_WAIT_TIMEOUT must be greater than zero")

        adb_exec_timeout = int(os.getenv("APPIUM_ADB_EXEC_TIMEOUT", "60000"))
        if adb_exec_timeout < 1:
            raise ValueError("APPIUM_ADB_EXEC_TIMEOUT must be greater than zero")

        return cls(
            server_url=os.getenv(
                "APPIUM_SERVER_URL",
                "http://127.0.0.1:4723",
            ),
            udid=os.getenv("ANDROID_UDID", "emulator-5554"),
            device_name=os.getenv("ANDROID_DEVICE_NAME", "Android Emulator"),
            adb_path=os.getenv("ADB_PATH", "adb"),
            app_package=os.getenv(
                "APP_PACKAGE",
                "com.saucelabs.mydemoapp.android",
            ),
            app_activity=os.getenv(
                "APP_ACTIVITY",
                "com.saucelabs.mydemoapp.android.view.activities.SplashActivity",
            ),
            wait_timeout=wait_timeout,
            adb_exec_timeout=adb_exec_timeout,
        )
