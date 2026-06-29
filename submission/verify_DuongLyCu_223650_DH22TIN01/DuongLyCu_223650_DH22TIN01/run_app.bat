@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Chua tim thay moi truong ao .venv.
    echo Hay lam theo README_HUONG_DAN_CHAY.md de cai dat.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" "src\4_main_desktop_app.py"
pause
