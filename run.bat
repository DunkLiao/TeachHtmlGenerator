@echo off
setlocal

cd /d "%~dp0"

set "PYTHON_EXE="
set "PREFERRED_PYTHON=D:\ProgramData\anaconda3\python.exe"

if exist "%PREFERRED_PYTHON%" set "PYTHON_EXE=%PREFERRED_PYTHON%"

if not defined PYTHON_EXE (
  for /f "delims=" %%I in ('where python 2^>nul') do (
    if not defined PYTHON_EXE (
      echo %%I | findstr /i "\\WindowsApps\\python.exe" >nul
      if errorlevel 1 set "PYTHON_EXE=%%I"
    )
  )
)

if not defined PYTHON_EXE (
  echo [ERROR] Python executable was not found.
  echo [HINT] Install Python, or update PREFERRED_PYTHON in run.bat.
  pause
  exit /b 1
)

echo [INFO] Using Python: %PYTHON_EXE%
echo [INFO] Theme is configured in theme_options.py

"%PYTHON_EXE%" -c "from theme_options import get_selected_theme; print('[INFO] Selected theme: ' + get_selected_theme().name)"
if errorlevel 1 (
  echo [ERROR] Theme configuration is invalid.
  echo [HINT] Open theme_options.py and set THEME_KEY to one of the available theme keys.
  pause
  exit /b 1
)

"%PYTHON_EXE%" -c "import markdown_it, mdit_py_plugins"
if errorlevel 1 (
  echo [ERROR] Required Python packages are missing.
  echo [HINT] Run: "%PYTHON_EXE%" -m pip install -r requirements.txt
  pause
  exit /b 1
)

"%PYTHON_EXE%" generate_site.py

if errorlevel 1 (
  echo [ERROR] Site generation failed.
  pause
  exit /b 1
)

echo [DONE] Generated site files in output_html\index.html
pause
