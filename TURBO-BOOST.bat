:: Nexus Turbo: Quick Launch
:: This script is designed to quickly launch the Turbo Boost script.

@echo off
set "PYTHON_EXE=python"
set "SCRIPT_PATH=%~dp0PROJECT\skills\nexus-system-control\scripts\turbo_boost.py"

echo ................................................
echo .           NEXUS TURBO: QUICK LAUNCH          .
echo ................................................
echo.

%PYTHON_EXE% "%~dp0ARCHIVIST.py"

echo ................................................
echo .         STARTING NEO4J GRAPH SERVER          .
echo ................................................
cd /d "%~dp0PROJECT"
docker-compose up -d neo4j postgres
cd /d "%~dp0"
echo.

%PYTHON_EXE% "%SCRIPT_PATH%"

echo.
echo Operation completed. Press any key to close...
pause > nul
