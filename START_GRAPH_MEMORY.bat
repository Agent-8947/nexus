@echo off
echo =======================================================
echo 🧠 NEXUS DEEP GRAPH MEMORY (Neo4j) INITIALIZER
echo =======================================================
echo.
echo Checking if Docker is running...
docker info >nul 2>&1
if "%ERRORLEVEL%"=="1" (
    echo [ERROR] Docker is not running. Please start Docker Desktop first.
    echo Press any key to exit...
    pause >nul
    exit /b
)

echo [OK] Docker is running.
echo Starting Neo4j Graph Database...
echo.

cd /d "%~dp0PROJECT"
docker-compose up -d neo4j

echo.
echo =======================================================
echo ✅ GRAPH MEMORY ONLINE
echo The MCP Neo4j Server will now successfully connect.
echo You can view the graph UI at: http://localhost:7474
echo Credentials: neo4j / nexus_graph_db
echo =======================================================
pause
