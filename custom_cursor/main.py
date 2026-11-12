import ctypes
import os
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

try:
    from PIL import Image
except ImportError:
    Image = None

APP_DIR = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "CustomCursor"
CURSOR_PATH = APP_DIR / "custom_cursor.cur"
REG_PATH = r"Control Panel\Cursors"

# Windows cursor role values; use same custom cursor for all common roles.
CURSOR_ROLES = [
    "Arrow", "Help", "AppStarting", "Wait", "Crosshair", "IBeam",
    "NWPen", "No", "SizeNS", "SizeWE", "SizeNWSE", "SizeNESW",
    "SizeAll", "UpArrow", "Hand"
]

def apply_cursor(cur_path):
    import winreg
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE) as key:
        for role in CURSOR_ROLES:
            winreg.SetValueEx(key, role, 0, winreg.REG_SZ, str(cur_path))
    # Notify Windows that the cursor scheme changed.
    SPI_SETCURSORS = 0x0057
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETCURSORS, 0, None, 0x0002)

def png_to_cur(image_path, output_path):
    if Image is None:
        raise RuntimeError("Pillow is missing. Install it with: py -m pip install Pillow")
    im = Image.open(image_path).convert("RGBA")
    # Windows cursors commonly support up to 256x256; preserve aspect ratio.
    im.thumbnail((256, 256), Image.Resampling.LANCZOS)
    # Cursor hotspot defaults to top-left (0,0). ICO container is used as CUR-compatible image.
    # Pillow's CUR support is not universal; write a single-frame .cur file directly.
    import struct
    w, h = im.size
    rgba = im.tobytes()
    # CUR uses a DIB: XOR bitmap (BGRA, bottom-up) + AND mask (1bpp, bottom-up).
    row_bytes = ((w * 32 + 31) // 32) * 4
    xor = bytearray()
    for y in range(h - 1, -1, -1):
        for x in range(w):
            r, g, b, a = im.getpixel((x, y))
            xor.extend((b, g, r, a))
        while len(xor) % row_bytes:
            xor.append(0)
    mask_row = ((w + 31) // 32) * 4
    and_mask = bytearray()
    for y in range(h - 1, -1, -1):
        row = bytearray(mask_row)
        for x in range(w):
            if im.getpixel((x, y))[3] < 128:
                row[x // 8] |= 0x80 >> (x % 8)
        and_mask.extend(row)
    header = struct.pack("<IIIHHIIIIII", 40, w, h * 2, 1, 32, 0,
                         len(xor) + len(and_mask), 0, 0, 0, 0)
    dib = header + xor + and_mask
    # CUR directory entry; hotspot at (0,0)
    width_byte = 0 if w == 256 else w
    height_byte = 0 if h == 256 else h
    directory = struct.pack("<HHH", 0, 2, 1)
    entry = struct.pack("<BBBBHHII", width_byte, height_byte, 0, 0,
                        0, 0, len(dib), 22)
    output_path.write_bytes(directory + entry + dib)

def main():
    if sys.platform != "win32":
        messagebox.showerror("Custom Cursor", "This tool works on Windows only.")
        return
    root = tk.Tk()
    root.title("Custom Cursor")
    root.geometry("430x220")
    root.resizable(False, False)
    root.attributes("-topmost", True)

    tk.Label(root, text="Custom Cursor for Windows", font=("Segoe UI", 14, "bold")).pack(pady=(16, 6))
    tk.Label(root, text="Choose a PNG/JPG image, convert it to a cursor, and apply it.").pack(pady=4)

    status = tk.StringVar(value="No custom cursor selected yet.")
    tk.Label(root, textvariable=status, wraplength=390).pack(pady=8)

    def choose_and_apply():
        path = filedialog.askopenfilename(
            title="Choose cursor image",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.webp *.bmp"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            APP_DIR.mkdir(parents=True, exist_ok=True)
            png_to_cur(Path(path), CURSOR_PATH)
            apply_cursor(CURSOR_PATH)
            # Keep a copy of the source image for future reapplication.
            import shutil
            shutil.copy2(path, APP_DIR / ("source" + Path(path).suffix.lower()))
            status.set(f"Applied: {Path(path).name}\nSaved cursor: {CURSOR_PATH}")
            messagebox.showinfo("Custom Cursor", "Cursor applied. It will be reapplied at Windows sign-in if startup is enabled.")
        except Exception as e:
            messagebox.showerror("Could not apply cursor", str(e))

    def reapply():
        try:
            if CURSOR_PATH.exists():
                apply_cursor(CURSOR_PATH)
                status.set("Saved cursor reapplied.")
            else:
                messagebox.showwarning("Custom Cursor", "Choose an image first.")
        except Exception as e:
            messagebox.showerror("Could not apply cursor", str(e))

    tk.Button(root, text="Choose image and apply", command=choose_and_apply, width=26).pack(pady=4)
    tk.Button(root, text="Reapply saved cursor", command=reapply, width=26).pack(pady=4)
    root.mainloop()

if __name__ == "__main__":
    main()
