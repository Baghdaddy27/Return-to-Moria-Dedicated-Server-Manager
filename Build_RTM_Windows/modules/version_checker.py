import requests
import json
import os
import datetime
import webbrowser
from PyQt5.QtWidgets import QMessageBox

def check_for_update_gui(parent=None, log=None):
    def _log(msg):
        if log:
            log(msg)
        else:
            print(msg)

    _log("📡 Checking for updates...")

    now = datetime.datetime.now()
    settings_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "settings.json"))

    try:
        with open(settings_path, 'r') as f:
            settings = json.load(f)
    except Exception as e:
        _log(f"⚠️ Failed to load settings.json: {e}")
        return

    current_version = settings.get("current_version", "0.0.0")
    ignore_version = settings.get("ignore_version", "")
    remind_until = settings.get("remind_later_until", "")
    version_url = "https://raw.githubusercontent.com/Baghdaddy27/RTM-Dedicated-Server-Manager/main/Build_RTM_Windows/version.txt"

    try:
        response = requests.get(version_url, timeout=5)
        if response.status_code != 200:
            _log(f"⚠️ Failed to fetch version file: {response.status_code}")
            return

        latest_version = response.text.strip()

        if latest_version == current_version:
            _log(f"✅ You are running the latest version ({current_version}).")
            return

        if latest_version == ignore_version:
            _log(f"🔕 Version {latest_version} is ignored.")
            return

        _log(f"⬆️ New version available: {latest_version} (current: {current_version})")

        if parent:
            msg = QMessageBox(parent)
            msg.setWindowTitle("Update Available")
            msg.setText("A newer version of RTM server is available.")
            download_btn = msg.addButton("Download", QMessageBox.AcceptRole)
            remind_btn = msg.addButton("Remind me later", QMessageBox.RejectRole)
            ignore_btn = msg.addButton("Ignore", QMessageBox.DestructiveRole)
            msg.exec_()

            if msg.clickedButton() == download_btn:
                webbrowser.open("https://github.com/Baghdaddy27/RTM-Dedicated-Server-Manager/releases")
            elif msg.clickedButton() == remind_btn:
                settings["remind_later_until"] = (now + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
            elif msg.clickedButton() == ignore_btn:
                settings["ignore_version"] = latest_version

            with open(settings_path, 'w') as f:
                json.dump(settings, f, indent=4)

    except Exception as e:
        _log(f"🛑 Update check failed: {e}")
