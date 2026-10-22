
# Mobile Test Automation with Behave and Appium

BDD test suite for Sauce Labs My Demo App on Android. Gherkin scenarios live in
`features/`, lifecycle hooks are in `features/environment.py`, and app
interactions are implemented in Page Objects.

## Project Structure

```text
features/
├── pages/                 # Screen locators and actions
├── steps/                 # Gherkin bindings; no UI locators
├── support/               # Configuration and driver creation
├── catalogo.feature       # Catalog and cart scenarios
└── environment.py         # Appium setup and teardown
evidencias/                # Reference UI hierarchy XML
artifacts/                 # Runtime screenshots/XML captured on failure
requirements.txt           # Direct Python dependencies
```

## Requirements

- Python 3.9 or later.
- Node.js `^20.19.0`, `^22.12.0`, or `>=24.0.0`, and npm `>=10` for Appium 3.
- A JDK and Android SDK with Android Platform and Platform-Tools installed.
  Set `JAVA_HOME` and `ANDROID_HOME`.
- A running emulator or connected device, with the app installed
  (`com.saucelabs.mydemoapp.android`).
- Appium Server 3 with the `uiautomator2` driver installed.

Create a virtual environment and install the Python dependencies:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Install Appium Server and its Android driver separately from the Python
environment:

```sh
npm install --global appium@3
appium driver install uiautomator2
```

Check the driver prerequisites:

```sh
appium driver doctor uiautomator2
```

Optional warnings about `bundletool`, `ffmpeg`, or GStreamer do not block this
suite. They are needed for Android App Bundle installation, screen recording, or
screen streaming, none of which these scenarios use.

Start the Appium server in a separate terminal before running the suite:

```sh
appium --address 127.0.0.1 --port 4723
```

On macOS, configure the Android SDK and JDK (adjust `ANDROID_HOME` if the SDK is
installed elsewhere):

```sh
export ANDROID_HOME="$HOME/Library/Android/sdk"
export JAVA_HOME="$(/usr/libexec/java_home)"
export PATH="$ANDROID_HOME/platform-tools:$PATH"
```

Run `adb devices` and confirm the emulator/device is listed with the `device`
state. If `adb` is not on `PATH`, set `ADB_PATH` to the executable. On Linux or
CI, set `ANDROID_HOME` and `JAVA_HOME` to the runner-specific paths.

If Python was built against LibreSSL, urllib3 2 may emit `NotOpenSSLWarning`.
The local configuration connects to Appium over HTTP, and this warning did not
block the tests. For HTTPS services or remote Appium, use a Python installation
linked against OpenSSL 1.1.1 or later. Do not downgrade urllib3: Selenium
requires urllib3 2.x.

## Configuration

All settings have local defaults and can be overridden with environment
variables in CI:

| Variable | Default | Description |
| --- | --- | --- |
| `APPIUM_SERVER_URL` | `http://127.0.0.1:4723` | Appium server URL |
| `ANDROID_UDID` | `emulator-5554` | Device identifier from `adb devices` |
| `ANDROID_DEVICE_NAME` | `Android Emulator` | Device name sent to Appium |
| `ADB_PATH` | `adb` | Path to the ADB executable |
| `APP_PACKAGE` | `com.saucelabs.mydemoapp.android` | Android app package |
| `APP_ACTIVITY` | `com.saucelabs.mydemoapp.android.view.activities.SplashActivity` | Launch activity |
| `APPIUM_WAIT_TIMEOUT` | `30` | Maximum explicit wait, in seconds |
| `APPIUM_ADB_EXEC_TIMEOUT` | `60000` | ADB command timeout, in milliseconds |

Before each scenario, the hook clears app data with `adb shell pm clear` and
launches the installed app. `evidencias/window.xml` is a reference hierarchy for
inspecting locators; it is not used at runtime. If setup or a step fails, a
screenshot and current XML hierarchy are saved under `artifacts/`. Evidence
capture errors are logged without replacing the original test failure.

## Running the Tests

With the emulator available and Appium listening at the configured URL:

```sh
python -m behave
```

To check feature and step-binding discovery without connecting to a device:

```sh
python -m behave --dry-run
```

For CI, provision the Android SDK and emulator, install the app and UiAutomator2
driver, start Appium, and set the environment variables required by the runner.
This project does not assume a specific CI provider.
