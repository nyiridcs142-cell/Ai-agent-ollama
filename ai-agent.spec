# -*- mode: python ; coding: utf-8 -*-
#
# PyInstaller specification for AI Agent v2.1.
# The application is packaged as a standalone executable or macOS app bundle.
#
# Windows native build: Nuitka build.bat
# Windows quick build: pyinstaller ai-agent.spec
# macOS app build: ./build-macos.sh build
#
# Output: dist\AI-Agent.exe on Windows or dist/AI-Agent.app on macOS.

import os, sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_all

HERE = os.path.dirname(os.path.abspath(SPEC))

# ---- CustomTkinter themes, images, and fonts --------------------------------
ctk_datas, ctk_binaries, ctk_hiddenimports = collect_all("customtkinter")

# ---- Darkdetect dependency for CustomTkinter --------------------------------
try:
    dd_datas, dd_binaries, dd_hidden = collect_all("darkdetect")
except Exception:
    dd_datas, dd_binaries, dd_hidden = [], [], []

# ---- Requests and urllib3 data files (CA certificates) ----------------------
req_datas = collect_data_files("certifi")

# ---- Project resources ------------------------------------------------------
extra_datas = []

skills_dir = os.path.join(HERE, "skills")
if os.path.isdir(skills_dir):
    extra_datas.append((skills_dir, "skills"))

memory_dir = os.path.join(HERE, "memory")
if os.path.isdir(memory_dir):
    extra_datas.append((memory_dir, "memory"))

mcp_json = os.path.join(HERE, "mcp.json")
if os.path.isfile(mcp_json):
    extra_datas.append((mcp_json, "."))

readme = os.path.join(HERE, "OLVASSEL.md")
if os.path.isfile(readme):
    extra_datas.append((readme, "."))

# ---- Hidden imports ---------------------------------------------------------
hidden = list(set(
    ctk_hiddenimports + dd_hidden + [
        "tkinter", "tkinter.ttk", "tkinter.filedialog",
        "tkinter.messagebox", "tkinter.simpledialog",
        "tkinter.font", "tkinter.colorchooser", "_tkinter",
        "customtkinter", *collect_submodules("customtkinter"),
        "requests", "requests.adapters", "requests.auth",
        "requests.cookies", "requests.exceptions", "requests.models",
        "requests.sessions", "requests.structures", "requests.utils",
        "urllib3", "urllib3.util", "urllib3.util.retry",
        "urllib3.util.timeout", "urllib3.poolmanager",
        "urllib3.connectionpool", "urllib3.contrib",
        "charset_normalizer", "charset_normalizer.md", "certifi", "idna", "idna.core",
        "json", "queue", "threading", "hashlib", "importlib",
        "importlib.util", "importlib.machinery", "shutil", "subprocess", "re", "atexit",
        "time", "os", "sys", "io",
        "encodings", "encodings.utf_8", "encodings.utf_16",
        "encodings.cp1250", "encodings.cp1252", "encodings.latin_1",
        "encodings.ascii",
    ]
))

# ---- Analysis --------------------------------------------------------------
a = Analysis(
    ["ai-agent.py"],
    pathex=[HERE],
    binaries=ctk_binaries + dd_binaries,
    datas=ctk_datas + dd_datas + req_datas + extra_datas,
    hiddenimports=hidden,
    hookspath=[], hooksconfig={}, runtime_hooks=[],
    excludes=[
        "matplotlib", "numpy", "pandas", "scipy", "PIL", "Pillow",
        "PyQt5", "PyQt6", "wx", "gi", "notebook", "IPython", "jupyter",
        "test", "unittest", "doctest", "pydoc_data", "email.mime",
        "xml.etree", "pygments",
    ],
    noarchive=False,
    optimize=1,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="AI-Agent",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[
        "vcruntime140.dll", "python313.dll", "tcl86t.dll", "tk86t.dll",
    ],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(HERE, "icon.ico") if sys.platform == "win32" and os.path.isfile(os.path.join(HERE, "icon.ico")) else None,
)

if sys.platform == "darwin":
    app = BUNDLE(
        exe,
        name="AI-Agent.app",
        icon=None,
        bundle_identifier="com.aiagent.desktop",
    )
