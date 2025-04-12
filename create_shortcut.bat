@echo off
setlocal

REM Get the current directory where the batch file is located
set "SCRIPT_DIR=%~dp0"

REM Set the path to the executable
set "EXE_PATH=%SCRIPT_DIR%dist\GitPy.exe"

REM Set the path to the desktop
set "DESKTOP_PATH=%USERPROFILE%\Desktop"

REM Create the shortcut using PowerShell
powershell -ExecutionPolicy Bypass -Command "$WS = New-Object -ComObject WScript.Shell; $SC = $WS.CreateShortcut('%DESKTOP_PATH%\GitPy.lnk'); $SC.TargetPath = '%EXE_PATH%'; $SC.WorkingDirectory = '%SCRIPT_DIR%dist'; $SC.IconLocation = '%EXE_PATH%,0'; $SC.Save()"

echo Desktop shortcut created successfully!
pause