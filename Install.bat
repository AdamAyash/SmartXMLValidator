@echo off
echo ======================================
echo Smart XML Validator - Auto Installer
echo ======================================
echo.

python --version >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo Python already installed.
) ELSE (
    echo Python not found. Downloading Python...

    powershell -Command "Invoke-WebRequest https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe -OutFile python-installer.exe"

    echo Installing Python silently...
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

    echo Waiting for installation...
    timeout /t 10 >nul
)

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing lxml...
python -m pip install lxml

echo.
echo ======================================
echo Installation Complete!
echo ======================================
pause