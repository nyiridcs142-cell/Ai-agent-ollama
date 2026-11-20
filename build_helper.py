"""
Build helper: packages the PyArmor-obfuscated folder with PyInstaller as one EXE.
The _pyarmor_dist/ folder contains obfuscated ai-agent.py and the pyarmor runtime.
"""
import os
import sys
import subprocess
import shutil

HERE          = os.path.dirname(os.path.abspath(__file__))
ARMORED_DIR   = os.path.join(HERE, "_pyarmor_dist")
ARMORED_MAIN  = os.path.join(ARMORED_DIR, "ai-agent.py")
SPEC_OUT      = os.path.join(HERE, "_armored.spec")

# Importok es adatok (ugyanaz mint az eredeti spec)
try:
    from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_all
except ImportError:
    print("[ERROR] PyInstaller was not found.")
    sys.exit(1)

# CustomTkinter data
ctk_datas, ctk_binaries, ctk_hiddenimports = collect_all("customtkinter")
try:
    dd_datas, dd_binaries, dd_hidden = collect_all("darkdetect")
except Exception:
    dd_datas, dd_binaries, dd_hidden = [], [], []
req_datas = collect_data_files("certifi")

# Project data
extra_datas = []
for name, dest in (
    ("skills",   "skills"),
    ("memory",   "memory"),
):
    p = os.path.join(HERE, name)
    if os.path.isdir(p):
        extra_datas.append((p, dest))

for name in ("mcp.json", "OLVASSEL.md"):
    p = os.path.join(HERE, name)
    if os.path.isfile(p):
        extra_datas.append((p, "."))

# PyArmor runtime folder
pyarmor_rt = os.path.join(ARMORED_DIR, "pyarmor_runtime0")
if os.path.isdir(pyarmor_rt):
    extra_datas.append((pyarmor_rt, "pyarmor_runtime0"))

# Hidden imports
hidden = list(set(
    ctk_hiddenimports + dd_hidden + [
        "tkinter", "tkinter.ttk", "tkinter.filedialog",
        "tkinter.messagebox", "tkinter.simpledialog",
        "tkinter.font", "_tkinter",
        "customtkinter",
        *collect_submodules("customtkinter"),
        "requests", "requests.adapters", "requests.auth",
        "requests.cookies", "requests.exceptions", "requests.models",
        "requests.sessions", "requests.utils",
        "urllib3", "urllib3.util", "urllib3.util.retry",
        "urllib3.poolmanager", "urllib3.connectionpool",
        "charset_normalizer", "certifi", "idna",
        "json", "queue", "threading", "hashlib",
        "importlib", "importlib.util", "importlib.machinery",
        "shutil", "subprocess", "re", "atexit",
        "encodings", "encodings.utf_8", "encodings.cp1250",
        "encodings.cp1252", "encodings.latin_1", "encodings.ascii",
    ]
))

excludes = [
    "matplotlib", "numpy", "pandas", "scipy",
    "PIL", "Pillow", "PyQt5", "PyQt6", "wx", "gi",
    "notebook", "IPython", "jupyter",
    "test", "unittest", "doctest", "pydoc_data",
    "email.mime", "xml.etree", "pygments",
]

# Spec content
all_datas    = ctk_datas + dd_datas + req_datas + extra_datas
all_binaries = ctk_binaries + dd_binaries

spec_lines = [
    "# Auto-generalt spec - ne szerkeszd kezzel",
    f"import sys",
    f"",
    f"a = Analysis(",
    f"    [r'{ARMORED_MAIN}'],",
    f"    pathex=[r'{ARMORED_DIR}', r'{HERE}'],",
    f"    binaries={repr(all_binaries)},",
    f"    datas={repr(all_datas)},",
    f"    hiddenimports={repr(hidden)},",
    f"    hookspath=[],",
    f"    hooksconfig={{}},",
    f"    runtime_hooks=[],",
    f"    excludes={repr(excludes)},",
    f"    noarchive=False,",
    f"    optimize=1,",
    f")",
    f"",
    f"pyz = PYZ(a.pure)",
    f"",
    f"exe = EXE(",
    f"    pyz,",
    f"    a.scripts,",
    f"    a.binaries,",
    f"    a.datas,",
    f"    [],",
    f"    name='AI-Agent',",
    f"    debug=False,",
    f"    bootloader_ignore_signals=False,",
    f"    strip=False,",
    f"    upx=True,",
    f"    upx_exclude=['vcruntime140.dll','python313.dll','tcl86t.dll','tk86t.dll'],",
    f"    runtime_tmpdir=None,",
    f"    console=False,",
    f"    disable_windowed_traceback=False,",
    f"    argv_emulation=False,",
    f"    target_arch=None,",
    f"    codesign_identity=None,",
    f"    entitlements_file=None,",
    f")",
]

spec_content = "\n".join(spec_lines)
with open(SPEC_OUT, "w", encoding="utf-8") as f:
    f.write(spec_content)

print(f"[OK] Spec file generated: {SPEC_OUT}")

# Run PyInstaller
result = subprocess.run(
    [sys.executable, "-m", "PyInstaller", SPEC_OUT, "--noconfirm",
     "--distpath", os.path.join(HERE, "dist"),
     "--workpath", os.path.join(HERE, "build")],
    cwd=HERE,
)

sys.exit(result.returncode)
