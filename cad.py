import os
import subprocess
import winreg
import webview

APP_NAME = "GSRP CAD"

STORAGE_PATH = os.path.join(
    os.environ["LOCALAPPDATA"],
    APP_NAME,
    "WebViewData"
)

os.makedirs(STORAGE_PATH, exist_ok=True)


def webview2_installed():
    registry_paths = [
        (
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients"
        ),
        (
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\EdgeUpdate\Clients"
        )
    ]

    for root, path in registry_paths:
        try:
            key = winreg.OpenKey(root, path)

            for i in range(winreg.QueryInfoKey(key)[0]):
                subkey_name = winreg.EnumKey(key, i)

                try:
                    subkey = winreg.OpenKey(key, subkey_name)
                    name, _ = winreg.QueryValueEx(subkey, "name")

                    if "WebView2 Runtime" in name:
                        return True

                except OSError:
                    pass

        except OSError:
            pass

    return False


if not webview2_installed():
    installer = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "MicrosoftEdgeWebview2Setup.exe"
    )

    subprocess.run([
        installer,
        "/silent",
        "/install"
    ], check=True)


webview.create_window(
    "GSRP CAD Interface",
    "https://cad.gsrp25.com/",
    width=1400,
    height=900
)

webview.start(
    private_mode=False,
    storage_path=STORAGE_PATH
)