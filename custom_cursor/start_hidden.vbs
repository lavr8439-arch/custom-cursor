Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pyw """ & CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName) & "\apply_saved.py""", 0, False
