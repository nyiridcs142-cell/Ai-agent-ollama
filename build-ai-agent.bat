@echo off
chcp 65001 >nul
title AI Agent - EXE Build

echo.
echo ============================================================
echo   AI Agent v2.1 - EXE Build
echo ============================================================
echo.
echo   [1] Quick build - PyInstaller
echo   [2] Native build - Nuitka
echo.
set /p CHOICE="Choice (1 or 2, Enter = 1): "
if "%CHOICE%"=="" set CHOICE=1

echo.
echo [ICON] Generating icon.ico from image.png...
python -c "from PIL import Image; img=Image.open('image.png').convert('RGBA'); img.save('icon.ico', format='ICO', sizes=[(256,256),(128,128),(64,64),(48,48),(32,32),(16,16)])" 2>&1
if not exist "icon.ico" (
    echo [WARNING] Icon generation failed; building without an icon.
) else (
    echo [OK] icon.ico created.
)

if "%CHOICE%"=="2" goto NUITKA

:PYINSTALLER
echo [PyInstaller build]
python --version >nul 2>&1
if %errorlevel% neq 0 ( echo [ERROR] Python was not found! & pause & exit /b 1 )
pyinstaller --version >nul 2>&1
if %errorlevel% neq 0 ( pip install pyinstaller )

if exist "dist\AI-Agent.exe" del /q "dist\AI-Agent.exe"
if exist "dist\AI-Agent" rmdir /s /q "dist\AI-Agent"
if exist "build\ai-agent" rmdir /s /q "build\ai-agent"

echo Building...
pyinstaller ai-agent.spec --noconfirm 2>&1
if exist "dist\AI-Agent.exe" (
    echo [DONE] dist\AI-Agent.exe
    explorer dist
) else (
    echo [ERROR] The EXE could not be created.
)
pause
exit /b 0

:NUITKA
echo [Nuitka build]
python -c "import nuitka" >nul 2>&1
if %errorlevel% neq 0 ( pip install nuitka )
python -m nuitka --onefile --windows-disable-console --enable-plugin=tk-inter --include-data-dir=skills=skills --output-dir=dist --output-filename=AI-Agent.exe ai-agent.py
if exist "dist\AI-Agent.exe" (
    echo [DONE] dist\AI-Agent.exe
    explorer dist
) else (
    echo [ERROR] The EXE could not be created.
)
pause