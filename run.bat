@echo off
setlocal

cd /d "%~dp0"

set "PYTHON_EXE="

if exist "D:\ProgramData\anaconda3\python.exe" set "PYTHON_EXE=D:\ProgramData\anaconda3\python.exe"

if not defined PYTHON_EXE for /f "delims=" %%I in ('where python 2^>nul') do if not defined PYTHON_EXE set "PYTHON_EXE=%%I"

if not defined PYTHON_EXE (
  echo [ERROR] Python executable was not found.
  pause
  exit /b 1
)

echo [INFO] Using Python: %PYTHON_EXE%
"%PYTHON_EXE%" generate_site.py

if errorlevel 1 (
  echo [ERROR] Site generation failed.
  pause
  exit /b 1
)

echo [DONE] Generated site files in output_html\index.html
pause