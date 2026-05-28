# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules


project_root = Path.cwd()


def data_file(source: str, target: str):
    return (str(project_root / source), target)


datas = [
    data_file("models/ann_best.keras", "models"),
    data_file("models/scaler.pkl", "models"),
    data_file("assets/sounds/alarm.wav", "assets/sounds"),
    data_file("src/3_database_setup.py", "src"),
    data_file("src/12_temporal_risk_index.py", "src"),
]

hiddenimports = [
    "customtkinter",
    "PIL._tkinter_finder",
    "joblib",
    "sklearn",
    "sklearn.neighbors._typedefs",
    "sklearn.neighbors._quad_tree",
    "sklearn.tree._utils",
    "mediapipe",
    "tensorflow",
    "matplotlib.backends.backend_tkagg",
]

for package_name in ["customtkinter", "mediapipe"]:
    package_datas, package_binaries, package_hiddenimports = collect_all(package_name)
    datas += package_datas
    hiddenimports += package_hiddenimports

hiddenimports += collect_submodules("sklearn")
datas += collect_data_files("tensorflow", include_py_files=False)


a = Analysis(
    [str(project_root / "src" / "4_main_desktop_app.py")],
    pathex=[str(project_root), str(project_root / "src")],
    binaries=[],
    datas=datas,
    hiddenimports=sorted(set(hiddenimports)),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "notebook",
        "jupyter",
        "IPython",
        "pytest",
        "tests",
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="PostureDetectionApp",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="PostureDetectionApp",
)
