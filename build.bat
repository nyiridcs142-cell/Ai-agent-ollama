@echo off
chcp 65001 >nul
title AI Agent - EXE Build

echo.
echo ============================================================
echo   AI Agent v2.1 - EXE Build
echo ============================================================
echo.
echo   [1] Quick build - PyInstaller (not obfuscated)
echo   [2] Native build - Nuitka (C compilation)
echo.
set /p CHOICE="Choice (1 or 2, Enter = 1): "
if "%CHOICE%"=="" set CHOICE=1

echo.
echo [ICON] Generating icon.ico from image.png...
python -c "from PIL import Image; img=Image.open('image.png').convert('RGBA'); img.save('icon.ico', format='ICO', sizes=[(256,256),(128,128),(64,64),(48,48),(32,32),(16,16)])" 2>&1
if not exist "icon.ico" (
    echo [WARNING] Icon generation failed; building without an icon.
    set ICON_FLAG=
    set NUITKA_ICON=
) else (
    echo [OK] icon.ico created.
    set ICON_FLAG=--icon=icon.ico
    set NUITKA_ICON=--windows-icon-from-ico=icon.ico
)

if "%CHOICE%"=="2" goto NUITKA

:PYINSTALLER
echo.
echo [PyInstaller build]
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 ( echo [ERROR] Python was not found! & pause & exit /b 1 )

pyinstaller --version >nul 2>&1
if %errorlevel% neq 0 ( pip install pyinstaller )

if exist "dist\AI-Agent.exe" del /q "dist\AI-Agent.exe"
if exist "dist\AI-Agent" rmdir /s /q "dist\AI-Agent"
if exist "build\ai-agent" rmdir /s /q "build\ai-agent"

echo Building... (1-3 minutes)
pyinstaller ai-agent.spec --noconfirm %ICON_FLAG% 2>&1

if exist "dist\AI-Agent.exe" (
    echo.
    echo ============================================================
    echo   DONE: dist\AI-Agent.exe
    echo ============================================================
    explorer dist
) else (
    echo [ERROR] The EXE could not be created.
)
pause
exit /b 0

:NUITKA
echo.
echo [Nuitka build - the first build downloads the C compiler and may take 5-20 minutes]
echo.

python -c "import nuitka" >nul 2>&1
if %errorlevel% neq 0 ( pip install nuitka )

if exist "dist\AI-Agent.exe" del /q "dist\AI-Agent.exe"
if exist "ai-agent.build" rmdir /s /q "ai-agent.build"
if exist "ai-agent.onefile-build" rmdir /s /q "ai-agent.onefile-build"

echo For compiler prompts, type Y and press Enter.
echo.

python -m nuitka ^
    --onefile ^
    --windows-disable-console ^
    --enable-plugin=tk-inter ^
    %NUITKA_ICON% ^
    --include-data-dir=skills=skills ^
    --nofollow-import-to=matplotlib ^
    --nofollow-import-to=numpy ^
    --nofollow-import-to=pandas ^
    --nofollow-import-to=PyQt5 ^
    --nofollow-import-to=PyQt6 ^
    --output-dir=dist ^
    --output-filename=AI-Agent.exe ^
    ai-agent.py

if exist "dist\AI-Agent.exe" (
    echo.
    echo ============================================================
    echo   DONE: dist\AI-Agent.exe
    echo ============================================================
    if exist "ai-agent.build" rmdir /s /q "ai-agent.build"
    if exist "ai-agent.onefile-build" rmdir /s /q "ai-agent.onefile-build"
    explorer dist
) else (
    echo [ERROR] The EXE could not be created.
)
pause
