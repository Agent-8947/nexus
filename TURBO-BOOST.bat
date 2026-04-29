:: NEXUS TURBO-BOOST v2.0 — Fast Mode (Neo4j/Postgres BYPASSED)
:: Restore docker services manually via START_GRAPH_MEMORY.bat if needed.

@echo off
set "PYTHON_EXE=python"
set "SCRIPT_PATH=%~dp0PROJECT\skills\nexus-system-control\scripts\turbo_boost.py"

echo ================================================
echo   NEXUS TURBO-BOOST v2.0 — FAST LAUNCH
echo ================================================
echo.

%PYTHON_EXE% "%~dp0ARCHIVIST.py"

echo.
echo [INFO] Neo4j/Postgres are BYPASSED (Docker offline).
echo [INFO] Run START_GRAPH_MEMORY.bat manually to activate graph services.
echo.

if exist "%SCRIPT_PATH%" (
    %PYTHON_EXE% "%SCRIPT_PATH%"
)

echo.
echo [DONE] NEXUS ready. Press any key to close...
pause > nul
