import os
import ctypes
from pathlib import Path
import winreg

CURSOR_PATH = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "CustomCursor" / "custom_cursor.cur"
REG_PATH = r"Control Panel\Cursors"
ROLES = ["Arrow", "Help", "AppStarting", "Wait", "Crosshair", "IBeam", "NWPen",
         "No", "SizeNS", "SizeWE", "SizeNWSE", "SizeNESW", "SizeAll", "UpArrow", "Hand"]

def main():
    if not CURSOR_PATH.exists():
        return
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE) as key:
        for role in ROLES:
            winreg.SetValueEx(key, role, 0, winreg.REG_SZ, str(CURSOR_PATH))
    ctypes.windll.user32.SystemParametersInfoW(0x0057, 0, None, 0x0002)

if __name__ == "__main__":
    main()
