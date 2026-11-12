# Custom Cursor (Windows)

A small GUI tool that accepts an image, converts it to a Windows `.cur` file, applies it to common cursor roles, and can reapply it at sign-in without showing CMD.

## Setup
1. Install Python 3 for Windows.
2. In PowerShell in this folder, run:
   `py -m pip install -r requirements.txt`
3. Run `pyw main.py`.
4. Click **Choose image and apply** and select a PNG/JPG/WebP/BMP image.
   Transparent PNGs work best. The image is resized to fit within 256×256.
5. The cursor hotspot is set to the top-left corner. A cursor image with the pointer tip at the top-left works best.

## Auto-start without CMD
1. First apply your chosen image once.
2. Press `Win + R`, type `shell:startup`, press Enter.
3. Create a shortcut to `start_hidden.vbs` inside the Startup folder.
4. Sign out/in or restart Windows to test.

The startup helper only reapplies the saved cursor and exits. It does not open a console or a visible window.
The tool edits the current Windows user's cursor scheme. If you want to restore the default cursor, open Windows Settings > Bluetooth & devices > Mouse > Additional mouse settings > Pointers, and choose the Windows default scheme.

## Notes
- This tool is for Windows. Some cursor roles/apps may continue using their own cursor.
- Applying a system cursor requires no administrator rights, but organizational policies may block registry changes.
